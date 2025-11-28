from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from app.core.config import settings
from app.rag.vector_store import vector_store

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_rag_chain(session_id: str):
    # 1. Setup LLM (OpenRouter)
    llm = ChatOpenAI(
        api_key=settings.OPENROUTER_API_KEY,
        base_url=settings.OPENROUTER_BASE_URL,
        model=settings.LLM_MODEL,
        temperature=0.7
    )
    
    # 2. Setup Retriever with Session Filter
    from langchain_chroma import Chroma
    from app.rag.embeddings import get_embedding_model
    
    # Re-initialize LangChain Chroma wrapper using the persistent client
    vectorstore = Chroma(
        client=vector_store.get_client(),
        collection_name="research_papers",
        embedding_function=get_embedding_model(),
    )
    
    retriever = vectorstore.as_retriever(
        search_kwargs={
            "filter": {"session_id": session_id},
            "k": 5
        }
    )

    # 3. Create Prompt
    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise."
        "\n\n"
        "{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
        ]
    )

    # 4. Create LCEL Chain
    # We want to return {"answer": ..., "context": ...}
    
    # Step A: Retrieve documents
    # Input: {"input": "...", "chat_history": ...}
    # Output: {"input": "...", "chat_history": ..., "context": [docs]}
    retrieval_step = RunnablePassthrough.assign(
        context=(lambda x: x["input"]) | retriever
    )
    
    # Step B: Generate Answer
    # Input: {"input": "...", "chat_history": ..., "context": [docs]}
    # We need to format docs for the prompt
    generation_step = (
        RunnablePassthrough.assign(
            formatted_context=lambda x: format_docs(x["context"])
        )
        | (lambda x: {
            "context": x["formatted_context"],
            "chat_history": x["chat_history"],
            "input": x["input"]
        })
        | prompt
        | llm
        | StrOutputParser()
    )
    
    # Combine
    rag_chain = retrieval_step.assign(answer=generation_step)
    
    return rag_chain
