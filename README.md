# Markdown Converter Microservice

A simple localhost API that converts PDF files, HTML pages, and DOCX documents into Markdown using Microsoft's markitdown library (PDF/HTML) and Pandoc (DOCX with tracked changes).

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Install Pandoc (required for DOCX support):

```bash
brew install pandoc  # macOS
```

For other platforms, download from https://pandoc.org/installing.html.

## Usage

Start the server:
```bash
source venv/bin/activate
python app.py
```

The API runs on `http://127.0.0.1:5000`

## API Endpoints

### POST /convert
Convert a PDF, HTML, or DOCX file to Markdown.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: file upload with key 'file'
- Supported formats: .pdf, .html, .htm, .docx

**Example with curl:**
```bash
curl -X POST -F "file=@document.docx" http://127.0.0.1:5000/convert
```

**Response:**
```json
{
  "markdown": "# Document content in markdown with ~~tracked deletions~~ preserved...",
  "filename": "document.docx"
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
