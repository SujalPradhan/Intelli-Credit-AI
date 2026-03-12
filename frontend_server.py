"""
frontend_server.py
------------------
Extends the existing FastAPI app (without modifying any backend files) to:
  1. Enable CORS so the browser can call the API from any origin.
  2. Mount the `frontend/` directory as static files at /ui.

Run with:
    python frontend_server.py

Then open your browser at:
    http://localhost:8000/ui/

The full REST API is still available at the same base URL:
    http://localhost:8000/docs         ← Swagger UI
    http://localhost:8000/ingest/document
    http://localhost:8000/research/analyze
    http://localhost:8000/recommend/
"""

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import the already-configured FastAPI app (all routers are registered inside main.py)
from main import app

# ── CORS ──────────────────────────────────────────────────────────────────────
# Allows the browser to call the API when the HTML is opened from a different
# origin (e.g. file:// or a different port).  "*" is safe for a local dev tool.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Static files ──────────────────────────────────────────────────────────────
# Mount the frontend directory AFTER all API routers so API routes take priority.
# html=True serves index.html for any sub-path that has no matching file.
app.mount("/ui", StaticFiles(directory="frontend", html=True), name="frontend")


if __name__ == "__main__":
    print()
    print("┌──────────────────────────────────────────────────────────┐")
    print("│           Intelli-Credit AI  —  Frontend Server          │")
    print("├──────────────────────────────────────────────────────────┤")
    print("│  Dashboard  →  http://localhost:8000/ui/                 │")
    print("│  API Docs   →  http://localhost:8000/docs                │")
    print("└──────────────────────────────────────────────────────────┘")
    print()
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
