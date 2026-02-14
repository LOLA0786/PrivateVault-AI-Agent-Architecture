from app.ai.orchestrator import run_pipeline


def execute_ai(request):
    return run_pipeline(
        input_text=request.input_text,
        tenant_id=request.tenant_id,
        user_id=request.user_id
    )
