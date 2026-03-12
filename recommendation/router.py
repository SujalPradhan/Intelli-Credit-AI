import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from recommendation.cam_generator import CAM_STORAGE_DIR
from recommendation.schemas import RecommendationRequest, RecommendationResponse
from recommendation.service import generate_recommendation

router = APIRouter(prefix="/recommend", tags=["Recommendation"])


@router.post("/", response_model=RecommendationResponse)
async def get_recommendation(request: RecommendationRequest):
    """
    Generate a credit score, decision, and CAM report.

    Pass the full output from **POST /research/analyze** plus the loan
    details (loan_requested, collateral_value, collateral_description)
    directly into this endpoint.

    Returns:
    - **score_breakdown** — Five Cs scores (Character/Capacity/Capital/Collateral/Conditions)
    - **score_explanation** — Per-C reasoning with specific data points cited
    - **decision** — Approval/Rejection with recommended loan amount, rate, tenor, and rationale
    - **cam_report_url** — Link to download the generated CAM Word document
    """
    return await generate_recommendation(request)


@router.get("/cam/{filename}")
async def download_cam(filename: str):
    """
    Download a generated CAM Word document (.docx).

    Use the `cam_report_url` from the POST /recommend/ response to get the filename.
    """
    safe_filename = os.path.basename(filename)
    file_path = os.path.join(CAM_STORAGE_DIR, safe_filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="CAM report not found.")

    return FileResponse(
        path=file_path,
        filename=safe_filename,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


@router.get("/pdf/{filename}")
async def download_cam_pdf(filename: str):
    """
    Download a generated CAM report as PDF.

    Use the `cam_pdf_url` from the POST /recommend/ response to get the filename.
    Returns 404 if PDF conversion was unavailable at generation time.
    """
    safe_filename = os.path.basename(filename)
    file_path = os.path.join(CAM_STORAGE_DIR, safe_filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="CAM PDF not found.")

    return FileResponse(
        path=file_path,
        filename=safe_filename,
        media_type="application/pdf",
    )
