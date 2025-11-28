from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.db.models import Session
from app.rag.vector_store import vector_store
import uuid

router = APIRouter()

@router.post("/", response_model=dict)
async def create_session(db: AsyncSession = Depends(get_db)):
    print("[BACKEND] Creating new session...", flush=True)
    new_session = Session(session_id=str(uuid.uuid4()))
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    print(f"[BACKEND] Session created: {new_session.session_id}", flush=True)
    return {"session_id": new_session.session_id, "created_at": new_session.created_at}

@router.get("/{session_id}", response_model=dict)
async def get_session(session_id: str, db: AsyncSession = Depends(get_db)):
    print(f"[BACKEND] Retrieving session: {session_id}", flush=True)
    result = await db.execute(select(Session).where(Session.session_id == session_id))
    session = result.scalars().first()
    if not session:
        print(f"[BACKEND] Session not found: {session_id}", flush=True)
        raise HTTPException(status_code=404, detail="Session not found")
    print(f"[BACKEND] Session found: {session_id}", flush=True)
    return {"session_id": session.session_id, "created_at": session.created_at}

@router.delete("/{session_id}")
async def delete_session(session_id: str, db: AsyncSession = Depends(get_db)):
    print(f"[BACKEND] Deleting session: {session_id}", flush=True)
    result = await db.execute(select(Session).where(Session.session_id == session_id))
    session = result.scalars().first()
    if not session:
        print(f"[BACKEND] Session not found for deletion: {session_id}", flush=True)
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Delete from SQL DB
    await db.delete(session)
    await db.commit()
    
    # Delete from Vector DB
    try:
        vector_store.delete_session_documents(session_id)
        print(f"[BACKEND] Vector data deleted for session: {session_id}", flush=True)
    except Exception as e:
        print(f"[BACKEND] Error deleting vector data for session {session_id}: {e}", flush=True)
        # We don't raise here to ensure the SQL delete persists
        
    return {"message": "Session deleted successfully"}
