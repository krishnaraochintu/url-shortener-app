# Flask URL Shortener

A simple URL shortener built with Flask. Users submit long URLs and receive short codes. The app redirects short codes to original URLs and shows a paginated list of all stored links on the main page. Supports in-memory (default) or SQLite storage, switchable via environment variable.

## Features

- Shorten long URLs
- Redirect short codes to original URLs
- Paginated list of all stored links on the main page
- In-memory or SQLite storage (switchable via environment variable)
- Accessible on all network interfaces (`0.0.0.0`)


## Local Development

1. Create and activate a Python virtual environment (recommended):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install flask
   ```

3. Run the app (default: in-memory storage):

   ```bash
   python app.py
   ```

   Or to use SQLite storage:

   ```bash
   USE_SQLITE=true python app.py
   ```

The app will be available at `http://localhost:5000/`.

## Usage

- Open your browser and go to `http://<your-server-ip>:5000/` (replace `<your-server-ip>` with your server's IP or `localhost` for local use).
- Submit a long URL in the form to receive a short code.
- All stored links are displayed on the main page, with pagination (10 links per page). Use "Next" and "Previous" to navigate.
- Click a short code link to be redirected to the original URL.
- You can also visit `/list` to see all stored links (without pagination).

## Storage Selection

- By default, the app uses in-memory storage (data lost on restart).
- To use persistent SQLite storage, set the environment variable `USE_SQLITE=true` before running the app.
  - Example: `USE_SQLITE=true python app.py`

## Network Access

- The app listens on all network interfaces (`0.0.0.0`).
- Access from any device on your network using your server's IP address and port 5000.



## Production Deployment

For production, use a WSGI server such as gunicorn. Example:

```bash
source .venv/bin/activate
pip install gunicorn
USE_SQLITE=true gunicorn --bind 0.0.0.0:5000 app:app
```

- This runs the app with SQLite storage, accessible on all interfaces.
- Adjust `USE_SQLITE` as needed for your storage preference.
- You can use other WSGI servers (e.g., uWSGI) or deploy behind a reverse proxy (e.g., nginx).
- For best security and performance, use a reverse proxy (like nginx) in front of gunicorn.


### Important for SQLite mode

The app now automatically initializes the SQLite table (`urls`) on startup, whether you run with Flask or gunicorn. You do not need to run the app manually to create the table.

If you see an error like `sqlite3.OperationalError: no such table: urls`, ensure your container or environment has write access to the database file location.




## Containerization

To build and run the app in a container:

1. Use a Python base image (e.g., `python:3.10-slim`).
2. Copy your project files into the container.
3. Install dependencies with:
   ```bash
   pip install -r requirements.txt
   ```
   (Make sure `flask` and `gunicorn` are listed in `requirements.txt`.)
4. Set the working directory appropriately (e.g., `/app`).
5. Expose port 5000.
6. Set the entrypoint to run gunicorn:
   ```bash
   USE_SQLITE=true gunicorn --bind 0.0.0.0:5000 app:app
   ```
7. For persistent SQLite storage, mount a Docker volume to `/app/urls.db` (or the path you use for `DB_PATH`). Example:
   ```bash
   docker run -v urlshortener-data:/app/urls.db ...
   ```
8. Pass environment variables (like `USE_SQLITE`) as needed.

Refer to Docker documentation for details on building and running containers and volumes.

---
