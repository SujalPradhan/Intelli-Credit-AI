from recommendation.schemas import RecommendationRequest, RecommendationResponse
from recommendation.scorer import compute_five_cs
from recommendation.decision import derive_decision
from recommendation.cam_generator import generate_cam_document


async def generate_recommendation(request: RecommendationRequest) -> RecommendationResponse:
    # Step 1: Score the Five Cs of Credit
    score, score_explanation = compute_five_cs(request)

    # Step 2: Derive credit decision (loan amount, rate, approval/rejection + reason)
    decision = derive_decision(request, score)

    # Step 3: Generate CAM Word document via Gemini + python-docx, then convert to PDF
    docx_filename, pdf_filename = await generate_cam_document(request, score, score_explanation, decision)

    return RecommendationResponse(
        company_name=request.company_name,
        score_breakdown=score,
        score_explanation=score_explanation,
        decision=decision,
        cam_report_url=f"/recommend/cam/{docx_filename}",
        cam_pdf_url=f"/recommend/pdf/{pdf_filename}" if pdf_filename else None,
    )
