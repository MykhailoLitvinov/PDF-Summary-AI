import logging

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.models import DocumentSummary, APIResponse
from app.services import PDFService, OpenAIService, DatabaseService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/documents", tags=["documents"])

# Initialize services
pdf_service = PDFService()
openai_service = OpenAIService()
db_service = DatabaseService()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload and process a PDF file"""
    try:
        # Read file content
        file_content = await file.read()

        logger.info(f"Received file: {file.filename}, size: {len(file_content)} bytes")

        # Validate the PDF
        is_valid, validation_message = pdf_service.validate_pdf(file_content, file.filename)
        if not is_valid:
            raise HTTPException(status_code=400, detail=validation_message)

        # Extract text from the PDF
        logger.info("Extracting text from PDF...")
        extracted_data = pdf_service.extract_pdf_content(file_content)

        if not extracted_data["text"].strip():
            raise HTTPException(
                status_code=400,
                detail="Failed to extract text from the PDF file.",
            )

        # Generate summary using OpenAI
        logger.info("Generating summary with OpenAI...")

        summary = openai_service.generate_summary(extracted_data["text"], extracted_data["images"])

        # Create document object
        document = DocumentSummary(
            filename=file.filename,
            summary=summary,
            file_size=len(file_content),
            page_count=extracted_data["page_count"],
        )

        # Save to the database
        if not db_service.save_document_summary(document):
            logger.warning("Failed to save to the database, but returning result anyway")

        logger.info(f"Document {file.filename} processed successfully")

        return APIResponse(
            success=True,
            message="Document processed successfully",
            data={
                "id": document.id,
                "filename": document.filename,
                "summary": document.summary,
                "upload_date": document.upload_date.isoformat(),
                "file_size": document.file_size,
                "page_count": document.page_count,
            },
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error processing file {file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing file")


@router.get("/history")
async def get_history():
    """Retrieve the history of the last 5 documents"""
    try:
        documents = db_service.get_last_5_documents()

        return APIResponse(
            success=True,
            message=f"Found {len(documents)} documents",
            data={
                "documents": [
                    {
                        "id": doc.id,
                        "filename": doc.filename,
                        "summary": doc.summary[:200] + "..." if len(doc.summary) > 200 else doc.summary,
                        "upload_date": doc.upload_date.isoformat(),
                        "file_size": doc.file_size,
                        "page_count": doc.page_count,
                    }
                    for doc in documents
                ]
            },
        )

    except Exception as e:
        logger.error(f"Error retrieving document history: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving history")


@router.get("/{doc_id}")
async def get_document(doc_id: str):
    """Retrieve the full document by ID"""
    try:
        document = db_service.get_document_by_id(doc_id)

        if not document:
            raise HTTPException(status_code=404, detail="Document not found")

        return APIResponse(
            success=True,
            message="Document found",
            data={
                "id": document.id,
                "filename": document.filename,
                "summary": document.summary,
                "upload_date": document.upload_date.isoformat(),
                "file_size": document.file_size,
                "page_count": document.page_count,
            },
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error retrieving document {doc_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving document")
