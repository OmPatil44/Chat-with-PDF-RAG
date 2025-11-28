from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import List, Dict, Any

from app.db.session import get_db
from app.db.models import ChatHistory, Session
from app.rag.rag_chain import get_rag_chain

router = APIRouter()

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    response: str
    sources: List[Dict[str, Any]] = []

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    print(f"[BACKEND] Received chat request for session: {request.session_id}", flush=True)
    # 1. Verify Session
    result = await db.execute(select(Session).where(Session.session_id == request.session_id))
    session = result.scalars().first()
    if not session:
        print(f"[BACKEND] Session not found: {request.session_id}", flush=True)
        raise HTTPException(status_code=404, detail="Session not found")

    # 2. Retrieve Chat History (Last 5 turns)
    print("[BACKEND] Retrieving chat history...", flush=True)
    # We need to fetch the last 10 messages (5 user + 5 assistant)
    history_result = await db.execute(
        select(ChatHistory)
        .where(ChatHistory.session_id == request.session_id)
        .order_by(ChatHistory.timestamp.desc())
        .limit(10)
    )
    history_items = history_result.scalars().all()
    # Reverse to get chronological order
    history_items = history_items[::-1]
    print(f"[BACKEND] Retrieved {len(history_items)} history items.", flush=True)
    
    # Format for LangChain
    chat_history = []
    from langchain_core.messages import HumanMessage, AIMessage
    for item in history_items:
        if item.role == "user":
            chat_history.append(HumanMessage(content=item.content))
        else:
            chat_history.append(AIMessage(content=item.content))

    # 3. Run RAG Chain
    print("[BACKEND] Initializing RAG chain...", flush=True)
    rag_chain = get_rag_chain(request.session_id)
    
    try:
        print(f"[BACKEND] Invoking RAG chain with input: {request.message[:50]}...", flush=True)
        response = rag_chain.invoke({
            "input": request.message,
            "chat_history": chat_history
        })
        ai_message = response["answer"]
        print("[BACKEND] RAG chain response received.", flush=True)
        
        # Extract sources if available
        # The retrieval chain returns 'context' which is a list of documents
        sources = []
        if "context" in response:
            print(f"[BACKEND] Found {len(response['context'])} context documents.", flush=True)
            for doc in response["context"]:
                # Clean up page content to remove excessive newlines
                clean_content = doc.page_content[:200].replace("\n", " ").strip() + "..."
                sources.append({
                    "source": doc.metadata.get("source", "unknown"),
                    "page_content": clean_content
                })
        
    except Exception as e:
        print(f"[BACKEND] RAG Chain Error: {str(e)}", flush=True)
        raise HTTPException(status_code=500, detail=f"RAG Chain Error: {str(e)}")

    # 4. Save History (User + AI)
    print("[BACKEND] Saving chat history...", flush=True)
    user_msg = ChatHistory(
        session_id=request.session_id,
        role="user",
        content=request.message
    )
    ai_msg = ChatHistory(
        session_id=request.session_id,
        role="assistant",
        content=ai_message
    )
    
    db.add(user_msg)
    db.add(ai_msg)
    await db.commit()
    print("[BACKEND] Chat history saved.", flush=True)

    return ChatResponse(response=ai_message, sources=sources)
