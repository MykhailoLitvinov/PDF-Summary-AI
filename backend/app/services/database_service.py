import logging
import os
import sqlite3
from datetime import datetime
from typing import List, Optional

from app.models import DocumentSummary, DocumentHistory

logger = logging.getLogger(__name__)


class DatabaseService:
    def __init__(self):
        self.db_path = os.getenv("DATABASE_PATH")
        # Create the folder if it doesn't exist
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        """Initialize the database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS documents (
                        id TEXT PRIMARY KEY,
                        filename TEXT NOT NULL,
                        summary TEXT NOT NULL,
                        upload_date TEXT NOT NULL,
                        file_size INTEGER NOT NULL,
                        page_count INTEGER NOT NULL
                    )
                """
                )
                conn.commit()
                logger.info("Database initialized")
        except Exception as e:
            logger.error(f"Database initialization error: {str(e)}")
            raise

    def save_document_summary(self, document: DocumentSummary) -> bool:
        """Save document summary to the database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO documents (id, filename, summary, upload_date, file_size, page_count)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (
                        document.id,
                        document.filename,
                        document.summary,
                        document.upload_date.isoformat(),
                        document.file_size,
                        document.page_count,
                    ),
                )
                conn.commit()
                logger.info(f"Document {document.filename} saved to the database")
                return True
        except Exception as e:
            logger.error(f"Database save error: {str(e)}")
            return False

    def get_last_5_documents(self) -> List[DocumentHistory]:
        """Retrieve the last 5 documents"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT id, filename, summary, upload_date, file_size, page_count
                    FROM documents
                    ORDER BY upload_date DESC
                    LIMIT 5
                """
                )

                rows = cursor.fetchall()
                documents = []

                for row in rows:
                    doc = DocumentHistory(
                        id=row[0],
                        filename=row[1],
                        summary=row[2],
                        upload_date=datetime.fromisoformat(row[3]),
                        file_size=row[4],
                        page_count=row[5],
                    )
                    documents.append(doc)

                logger.info(f"Retrieved {len(documents)} documents from history")
                return documents

        except Exception as e:
            logger.error(f"Error retrieving document history: {str(e)}")
            return []

    def get_document_by_id(self, doc_id: str) -> Optional[DocumentHistory]:
        """Retrieve a document by its ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT id, filename, summary, upload_date, file_size, page_count
                    FROM documents
                    WHERE id = ?
                """,
                    (doc_id,),
                )

                row = cursor.fetchone()
                if row:
                    return DocumentHistory(
                        id=row[0],
                        filename=row[1],
                        summary=row[2],
                        upload_date=datetime.fromisoformat(row[3]),
                        file_size=row[4],
                        page_count=row[5],
                    )

        except Exception as e:
            logger.error(f"Error retrieving document: {str(e)}")
