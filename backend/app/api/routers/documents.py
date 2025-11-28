from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from app.rag.ingestion import ingest_document

router = APIRouter()

@router.post("/upload", response_model=dict)
async def upload_document(
    session_id: str = Form(...),
    file: UploadFile = File(...)
):
    print(f"[BACKEND] Received upload request for file: {file.filename} in session: {session_id}", flush=True)
    try:
        # Ingest the document
        print("[BACKEND] Starting ingestion pipeline...", flush=True)
        await ingest_document(file, session_id)
        print("[BACKEND] Ingestion pipeline completed successfully.", flush=True)
        
        return {
            "message": "Document uploaded and ingested successfully",
            "filename": file.filename,
            "session_id": session_id
        }
    except Exception as e:
        print(f"[BACKEND] Error during document upload: {str(e)}", flush=True)
        raise HTTPException(status_code=500, detail=str(e))
