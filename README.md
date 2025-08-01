# PDF Summary AI

A full-stack web application that processes PDF documents and generates AI-powered summaries using OpenAI's GPT-4o model. The application extracts text, tables, and images from PDF files and creates comprehensive summaries with support for multi-modal content analysis.

## Features

- **PDF Processing**: Upload and validate PDF files with configurable size and page limits
- **Multi-modal Analysis**: Extracts text, tables, and images from PDF documents
- **AI-Powered Summaries**: Uses OpenAI GPT-4o to generate intelligent summaries
- **Document History**: Store and retrieve document summaries with full-text search
- **REST API**: Clean API endpoints for document management
- **React Frontend**: Modern web interface for document upload and management
- **Docker Support**: Containerized deployment with Docker Compose
- **Comprehensive Testing**: Unit and integration tests with pytest

## Architecture

```
├── backend/              # FastAPI Python backend
│   ├── app/
│   │   ├── main.py      # FastAPI application
│   │   ├── models.py    # Pydantic data models
│   │   ├── routes/      # API endpoints
│   │   └── services/    # Business logic (PDF, OpenAI, Database)
│   └── requirements.txt
├── frontend/            # React TypeScript frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   └── services/    # API client
│   └── package.json
├── tests/              # Test suite
└── docker-compose.yml  # Docker configuration
```

## Prerequisites

- Python 3.9+
- Node.js 16+
- OpenAI API key
- Docker (optional, for containerized deployment)

## Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_PATH=./data/documents.db

# Optional - API Configuration
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

## Quick Start

### Option 1: Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd PDF-Summary-AI
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   
   # Create .env file with your OpenAI API key
   echo "OPENAI_API_KEY=your_key_here" > .env
   echo "DATABASE_PATH=./data/documents.db" >> .env
   
   # Start the backend server
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Frontend Setup** (in a new terminal)
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Option 2: Docker Deployment

1. **Create environment file**
   ```bash
   cd backend
   cp .env.example .env  # Edit with your OpenAI API key
   ```

2. **Start with Docker Compose**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### Health Check
```bash
GET /health
```
**Response:**
```json
{
  "status": "healthy",
  "service": "pdf-summary-ai"
}
```

#### Root Endpoint
```bash
GET /
```
**Response:**
```json
{
  "message": "PDF Summary AI Backend",
  "version": "1.0.0",
  "status": "running"
}
```

#### Upload PDF Document
```bash
POST /api/documents/upload
Content-Type: multipart/form-data
```
**Parameters:**
- `file`: PDF file (max 50MB, max 100 pages by default)

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/api/documents/upload" \
  -F "file=@document.pdf"
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Document processed successfully",
  "data": {
    "id": "uuid-string",
    "filename": "document.pdf",
    "summary": "AI-generated summary of the document...",
    "upload_date": "2023-01-01T00:00:00",
    "file_size": 1024,
    "page_count": 5
  }
}
```

**Error Responses:**
- `400`: Invalid file format, file too large, or processing error
- `500`: Internal server error

#### Get Document History
```bash
GET /api/documents/history
```
**Response:**
```json
{
  "success": true,
  "message": "Found 3 documents",
  "data": {
    "documents": [
      {
        "id": "uuid-string",
        "filename": "document.pdf",
        "summary": "Truncated summary (first 200 chars)...",
        "upload_date": "2023-01-01T00:00:00",
        "file_size": 1024,
        "page_count": 5
      }
    ]
  }
}
```

#### Get Document by ID
```bash
GET /api/documents/{doc_id}
```
**Parameters:**
- `doc_id`: Document UUID

**Example:**
```bash
curl "http://localhost:8000/api/documents/uuid-string"
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Document found",
  "data": {
    "id": "uuid-string",
    "filename": "document.pdf",
    "summary": "Full AI-generated summary...",
    "upload_date": "2023-01-01T00:00:00",
    "file_size": 1024,
    "page_count": 5
  }
}
```

**Error Responses:**
- `404`: Document not found
- `500`: Internal server error

## Docker Usage

### Development with Docker

1. **Build and run all services:**
   ```bash
   docker-compose up --build
   ```

2. **Run in background:**
   ```bash
   docker-compose up -d
   ```

3. **View logs:**
   ```bash
   docker-compose logs -f
   ```

4. **Stop services:**
   ```bash
   docker-compose down
   ```

### Production Deployment

1. **Create production environment file:**
   ```bash
   cp backend/.env.example backend/.env
   # Edit .env with production values
   ```

2. **Build production images:**
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml build
   ```

3. **Deploy:**
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   ```

### Individual Container Commands

**Backend only:**
```bash
cd backend
docker build -t pdf-summary-backend .
docker run -p 8000:8000 --env-file .env pdf-summary-backend
```

**Frontend only:**
```bash
cd frontend
docker build -t pdf-summary-frontend .
docker run -p 3000:3000 pdf-summary-frontend
```

### Environment Variables in Docker

When using Docker, ensure your `backend/.env` file contains:

```bash
# Required for Docker
DATABASE_PATH=/app/data/documents.db
CORS_ORIGINS=http://localhost:3000

# Your OpenAI API key
OPENAI_API_KEY=your_actual_api_key_here
```

### Volume Mounting

For persistent data storage in development:

```bash
docker-compose up -v $(pwd)/backend/data:/app/data
```

## Testing

### Running Tests

1. **Install test dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   pip install pytest pytest-asyncio httpx
   ```

2. **Run all tests:**
   ```bash
   pytest
   ```

3. **Run with coverage:**
   ```bash
   pytest --cov=app tests/
   ```

4. **Run specific test files:**
   ```bash
   pytest tests/test_pdf_service.py
   pytest tests/test_database_service.py
   pytest tests/test_api_endpoints.py
   ```

### Test Structure

```
tests/
├── conftest.py              # Test fixtures and setup
├── test_database_service.py # Database layer tests
├── test_pdf_service.py      # PDF processing tests
├── test_openai_service.py   # OpenAI integration tests
├── test_api_endpoints.py    # API endpoint tests
└── fixtures/                # Test PDF files
    ├── dummy.pdf
    └── sample.pdf
```

### Test Categories

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **API Tests**: Test HTTP endpoints and responses
- **Security Tests**: Verify error message sanitization

## Development

### Code Quality

The project follows these quality standards:

- **Error Handling**: Comprehensive error handling with sanitized error messages
- **Input Validation**: PDF file validation with configurable limits  
- **Security**: No sensitive information exposed in error responses
- **Configuration**: Environment-based configuration for flexibility
- **Testing**: Comprehensive test suite with pytest

### Project Structure

```
backend/app/
├── main.py              # FastAPI application setup
├── models.py            # Pydantic data models
├── routes/
│   └── documents.py     # Document API endpoints
└── services/
    ├── database_service.py  # SQLite database operations
    ├── pdf_service.py       # PDF processing with pdfplumber
    └── openai_service.py    # OpenAI API integration
```

### Adding New Features

1. **Create/modify models** in `models.py`
2. **Add business logic** in appropriate service file
3. **Create API endpoints** in `routes/`
4. **Write tests** in `tests/`
5. **Update documentation** in README.md

## Troubleshooting

### Common Issues

1. **OpenAI API Key Error:**
   ```
   ValueError: OpenAI API key not found
   ```
   **Solution:** Ensure `OPENAI_API_KEY` is set in your `.env` file

2. **Database Path Error:**
   ```
   ValueError: DATABASE_PATH environment variable is required
   ```
   **Solution:** Set `DATABASE_PATH` in your `.env` file

3. **PDF Processing Error:**
   ```
   Invalid PDF file format
   ```
   **Solution:** Ensure uploaded file is a valid PDF with proper signature

4. **CORS Error in Frontend:**
   **Solution:** Check `CORS_ORIGINS` environment variable includes your frontend URL

### Logs and Debugging

- **Backend logs:** Check console output or container logs
- **API Documentation:** Visit http://localhost:8000/docs for interactive API docs
- **Health Check:** Visit http://localhost:8000/health to verify backend status

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

For support and questions:
- Create an issue in the GitHub repository
- Check the troubleshooting section above
- Review the API documentation at `/docs` endpoint