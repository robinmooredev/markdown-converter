from flask import Flask, request, jsonify
from markitdown import MarkItDown
import tempfile
import os
import re
import shutil
import subprocess

app = Flask(__name__)
md = MarkItDown()


def get_debug_mode() -> bool:
    """Return whether Flask debug mode is enabled via environment."""
    return os.getenv("FLASK_DEBUG", "false").strip().lower() in {"1", "true", "yes", "on"}

def preprocess_html(html_content):
    """
    Preprocess HTML to improve markdown conversion.
    Moves leading <br> tags outside of <strong> tags to ensure proper line breaks.
    """
    # Pattern: <strong><br>...<br>Text
    # Move leading <br> tags outside the <strong> tag
    html_content = re.sub(r'<strong>(\s*(?:<br>\s*)+)', r'\1<strong>', html_content, flags=re.IGNORECASE)
    return html_content


def convert_docx_with_pandoc(docx_path):
    """
    Convert DOCX to Markdown using Pandoc to preserve tracked changes.
    """
    pandoc_path = shutil.which("pandoc")
    if pandoc_path is None:
        raise RuntimeError(
            "Pandoc not found on PATH. Install Pandoc to convert DOCX files."
        )

    completed = subprocess.run(
        [
            pandoc_path,
            "--from=docx",
            "--to=gfm",
            "--track-changes=all",
            docx_path,
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    if completed.returncode != 0:
        error_message = completed.stderr.strip() or "Pandoc conversion failed."
        raise RuntimeError(error_message)

    return completed.stdout.strip()

@app.route('/convert', methods=['POST'])
def convert():
    """
    Convert PDF, HTML, or DOCX file to Markdown.
    Expects a file upload with key 'file'.
    Returns markdown text.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Get file extension
    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in ['.pdf', '.html', '.htm', '.docx']:
        return jsonify({'error': 'Only PDF, HTML, and DOCX files are supported'}), 400

    try:
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_file:
            file.save(tmp_file.name)
            tmp_path = tmp_file.name

        if ext == '.docx':
            markdown_text = convert_docx_with_pandoc(tmp_path)
        else:
            # Preprocess HTML files to improve line break handling
            if ext in ['.html', '.htm']:
                with open(tmp_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()

                preprocessed_html = preprocess_html(html_content)

                with open(tmp_path, 'w', encoding='utf-8') as f:
                    f.write(preprocessed_html)

            # Convert to markdown
            result = md.convert(tmp_path)
            markdown_text = result.text_content

        # Clean up temporary file
        os.unlink(tmp_path)

        return jsonify({
            'markdown': markdown_text,
            'filename': file.filename
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    port = int(os.getenv("PORT", "5000"))
    app.run(host='127.0.0.1', port=port, debug=get_debug_mode())
