from fastapi import APIRouter

from app.models.workflow import WorkflowRequest, WorkflowRun
from app.runtime.orchestrator import orchestrator

router = APIRouter(tags=["runtime"])


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.post(
    "/workflows/run",
    response_model=WorkflowRun,
    summary="Execute a workflow",
    description="Runs a demo workflow through planner, validator, and executor runtime phases.",
)
def run_workflow(request: WorkflowRequest) -> WorkflowRun:
    return orchestrator.run(request)
