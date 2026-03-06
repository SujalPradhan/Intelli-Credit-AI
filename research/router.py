from fastapi import APIRouter
from research.schemas import ResearchRequest, ResearchResponse
from research.service import perform_research

router = APIRouter(prefix="/research", tags=["Research"])


@router.post("/analyze", response_model=ResearchResponse)
async def analyze_company(request: ResearchRequest):
    """
    Run the full research pipeline for a company.

    Receives company details, performs external intelligence gathering,
    and returns structured insights along with pipeline logs for transparency.
    """
    return await perform_research(request)
