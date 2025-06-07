# Flask + Pyodide + HTMX + PyCardano

A demonstration of running a Python Flask app entirely in the browser using WebAssembly (Pyodide) with HTMX for frontend interactions and PyCardano for Cardano blockchain functionality.

## How It Works

- **Python in the Browser**: Uses Pyodide to run Python and Flask directly in the browser
- **Service Worker**: Intercepts HTMX requests and redirects them to the in-browser Flask app
- **HTMX**: Handles UI updates without writing custom JavaScript
- **PyCardano**: Provides Cardano blockchain functionality (address generation)

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

Generate HTML report:

```bash
pytest tests/ --html=test-report.html --self-contained-html
```

## Running the App

You must serve the files from a web server (Service Worker won't work with file:// URLs):

```bash
python -m http.server
```

Or with uv:

```bash
uv run python -m http.server
```

Then open your browser to `http://localhost:8000`.

## Project Structure

- `index.html` - Main entry point with Pyodide initialization
- `main.py` - Flask application code
- `sw.js` - Service Worker that routes requests to the Flask app
- `static/` - CSS and other static assets
- `requirements.txt` - Python dependencies

## Why This Exists

This project demonstrates how to create a completely client-side web application using Python technologies that would normally require a server. Benefits include:

- Zero backend infrastructure required
- Can be hosted on any static file hosting
- User data stays in the browser
- Familiar Flask development experience
