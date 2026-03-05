from fastapi import APIRouter
from recommendation.schemas import RecommendationRequest, RecommendationResponse
from recommendation.service import generate_recommendation

router = APIRouter(prefix="/recommend", tags=["Recommendation"])

@router.post("/", response_model=RecommendationResponse)
async def get_recommendation(request: RecommendationRequest):
    """
    Endpoint for credit scoring and CAM generation.
    """
    # TODO: Generate scoring and decision logic via service
    return await generate_recommendation(request)
