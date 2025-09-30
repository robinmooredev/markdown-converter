from flask import Flask, request, jsonify
from markitdown import MarkItDown
import tempfile
import os

app = Flask(__name__)
md = MarkItDown()

@app.route('/convert', methods=['POST'])
def convert():
    """
    Convert PDF or HTML file to Markdown.
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

    if ext not in ['.pdf', '.html', '.htm']:
        return jsonify({'error': 'Only PDF and HTML files are supported'}), 400

    try:
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_file:
            file.save(tmp_file.name)
            tmp_path = tmp_file.name

        # Convert to markdown
        result = md.convert(tmp_path)

        # Clean up temporary file
        os.unlink(tmp_path)

        return jsonify({
            'markdown': result.text_content,
            'filename': file.filename
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
