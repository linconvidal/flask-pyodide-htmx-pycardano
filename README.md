# Flask + Pyodide + HTMX + PyCardano

This project runs a Python Flask app entirely in the browser using Pyodide, with HTMX for UI and PyCardano for Cardano blockchain features.

## Core Concepts

- **In-Browser Python**: Pyodide (Python compiled to WebAssembly) runs Flask directly in the browser.
- **Service Worker for Routing**: A Service Worker intercepts HTMX `fetch` requests and redirects them to the in-browser Flask application. This allows HTMX to work without a traditional server backend.
- **Static Hosting**: The entire application can be served as static files. No server-side execution is needed.
- **Client-Side PyCardano**: Cardano address generation happens in the browser.

## Project Structure

- `index.html`: Main entry point. Loads Pyodide and the Python application.
- `main.py`: The Flask application logic.
- `sw.js`: Service Worker that routes `fetch` requests to the Flask app.
- `static/`: Compiled CSS and other static assets.
- `requirements.txt`: Python dependencies installed by Pyodide.

## Setup

Set up the Python environment:

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

Install the Node.js dependencies for Tailwind CSS:

```bash
npm install
```

## Development

Build CSS in watch mode:

```bash
npm run dev
```

One-time CSS build:

```bash
npm run build
```

## Testing

Run tests:

```bash
pytest tests/ -v
```

Generate an HTML report:

```bash
pytest tests/ --html=test-report.html --self-contained-html
```

## Running the App

Serve the files from a local web server. The Service Worker will not work with `file://` URLs.

```bash
python -m http.server
```

Or with uv:

```bash
uv run python -m http.server
```

Then open your browser to `http://localhost:8000`.
