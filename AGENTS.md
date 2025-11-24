# Repository Guidelines

## Project Structure & Module Organization
- `app.py` hosts the Flask microservice with `/convert` and `/health` endpoints and the HTML pre-processing helper.
- `requirements.txt` tracks runtime dependencies (`flask`, `markitdown`); update it whenever libraries change. Pandoc is an external binary dependency used for DOCX conversion—note it in release notes when bumping system requirements.
- Use a local `venv/` for development; keep it out of version control. Place any future tests under `tests/` and shared fixtures in `tests/fixtures/`.

## Build, Test, and Development Commands
- `python3 -m venv venv && source venv/bin/activate` prepares the isolated environment.
- `pip install -r requirements.txt` syncs dependencies.
- `python app.py` starts the service at `http://127.0.0.1:5000`; keep `debug=True` only for local work.
- `brew install pandoc` (or platform equivalent) must be run once locally before DOCX conversions work.
- `curl -X POST -F "file=@sample.docx" http://127.0.0.1:5000/convert` is the quickest smoke test for DOCX conversions; swap in HTML/PDF samples as needed.

## Coding Style & Naming Conventions
- Target Python 3.11+, format with 4-space indentation, and follow PEP 8 naming (`snake_case` functions, `PascalCase` classes, UPPER_CASE constants).
- Keep Flask routes thin; push parsing or conversion logic into helper functions with docstrings and type hints for new code.
- Avoid persistent temp files—reuse the `tempfile` pattern established in `app.py`. When wiring external tools (Pandoc), capture stderr for troubleshooting and bubble up actionable errors.

## Testing Guidelines
- Add automated coverage with `pytest`; initialize a `tests/` package mirroring the module layout (e.g., `tests/test_convert.py`).
- Use `flask.testing.FlaskClient` fixtures to exercise endpoints and assert HTTP status codes, markdown payloads, and docx/pdf/html handling (including strikethrough preservation for tracked changes produced by Pandoc).
- When adding converters, include regression tests for edge cases (invalid file types, malformed HTML, corrupted DOCX, mixed track changes) and target ≥80% coverage on touched modules.

## Commit & Pull Request Guidelines
- Follow present-tense, descriptive commit messages (`Add HTML preprocessing`, `Improve error response`). Keep related changes in one commit.
- Reference linked issues in the commit body when applicable and prefer squashed history before merging.
- PRs should describe the motivation, list functional changes, call out new dependencies, and attach command outputs or screenshots for API changes.

## Security & Operations Notes
- Validate and sanitize all uploaded files; never trust client-provided filenames. The current workflow writes to a temporary path—preserve that pattern.
- Regenerate or invalidate the `venv` when upgrading dependencies, and review changelogs for `markitdown` and `flask` before deployment.
