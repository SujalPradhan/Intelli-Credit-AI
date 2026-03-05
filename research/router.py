from fastapi import APIRouter
from research.schemas import ResearchRequest, ResearchResponse
from research.service import perform_research

router = APIRouter(prefix="/research", tags=["Research"])

@router.post("/", response_model=ResearchResponse)
async def trigger_research(request: ResearchRequest):
    """
    Endpoint to handle external intelligence gathering.
    """
    # TODO: Handle research orchestration via service
    return await perform_research(request)
