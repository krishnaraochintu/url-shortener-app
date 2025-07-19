# URL Shortener

A simple URL shortener built with Flask. Users submit long URLs and receive short codes. The app redirects short codes to original URLs and shows a paginated list of all stored links on the main page. Supports in-memory (default) or SQLite storage, switchable via environment variable.

## Features

- Shorten long URLs
- Redirect short codes to original URLs
- Paginated list of all stored links on the main page
- In-memory or SQLite storage (switchable via environment variable)


## How to Use

1. Open your browser and go to `http://<your-server-ip>:5000/` (replace `<your-server-ip>` with your server's IP or `localhost` for local use).
2. Submit a long URL in the form to receive a short code.
3. All stored links are displayed on the main page, with pagination (10 links per page). Use "Next" and "Previous" to navigate.
4. Click a short code link to be redirected to the original URL.
5. You can also visit `/list` to see all stored links (without pagination).


## Local Development & Production (Terminal)

1. Activate your Python virtual environment:
   ```bash
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. For development, run:
   ```bash
   python app.py
   ```
   Or for SQLite:
   ```bash
   USE_SQLITE=true python app.py
   ```
4. For production, run with gunicorn (SQLite recommended):
   ```bash
   USE_SQLITE=true gunicorn --bind 0.0.0.0:5000 app:app
   ```
App is now available at `http://<server-ip>:5000/`.



## Production (Container)

1. Build your Docker image (Dockerfile example):
   - Use `python:3.10-slim` as base
   - Copy project files
   - Install dependencies: `pip install -r requirements.txt`
   - Expose port 5000
   - Entrypoint:
     ```bash
     USE_SQLITE=true gunicorn --bind 0.0.0.0:5000 app:app
     ```
2. Run with persistent SQLite storage:
   ```bash
   docker run -v urlshortener-data:/app/urls.db -p 5000:5000 <image>
   ```
3. Pass environment variables as needed.

See Docker documentation for more details.

---
