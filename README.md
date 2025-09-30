# Markdown Converter Microservice

A simple localhost API that converts PDF files and HTML pages into Markdown using Microsoft's markitdown library.

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

Start the server:
```bash
source venv/bin/activate
python app.py
```

The API runs on `http://127.0.0.1:5000`

## API Endpoints

### POST /convert
Convert a PDF or HTML file to Markdown.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: file upload with key 'file'
- Supported formats: .pdf, .html, .htm

**Example with curl:**
```bash
curl -X POST -F "file=@document.pdf" http://127.0.0.1:5000/convert
```

**Response:**
```json
{
  "markdown": "# Document content in markdown...",
  "filename": "document.pdf"
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## Error Responses

- 400: No file provided or invalid file type
- 500: Conversion error
