from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from ingestion.router import router as ingestion_router
from research.router import router as research_router
from recommendation.router import router as recommendation_router

app = FastAPI(
    title="Intelli-Credit AI",
    description="AI-powered credit decisioning system",
    version="0.1.0"
)

# Register routers
app.include_router(ingestion_router)
app.include_router(research_router)
app.include_router(recommendation_router)

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def root():
    return FileResponse("frontend/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)