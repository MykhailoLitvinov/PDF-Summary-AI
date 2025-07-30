from fastapi import APIRouter, UploadFile


router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.post("/upload")
async def upload_pdf(file: UploadFile):
    # 1. Validate pdf file
    # 2. Parse pdf file
    # 3. Generate summary
    # 4. Save to db
    # 5. Return response
    pass


@router.get("/history")
async def get_history():
    # Get last 5 processed pdf files
    pass
