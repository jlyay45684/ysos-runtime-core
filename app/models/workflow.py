from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class StepType(str, Enum):
    prompt = "prompt"
    tool = "tool"
    summarize = "summarize"


class RunStatus(str, Enum):
    planned = "planned"
    validating = "validating"
    running = "running"
    completed = "completed"
    failed = "failed"


class RuntimePhase(str, Enum):
    planner = "planner"
    validator = "validator"
    executor = "executor"


class WorkflowStep(BaseModel):
    name: str = Field(..., examples=["draft_response"])
    type: StepType = Field(..., examples=[StepType.prompt])
    input: str = Field(..., examples=["Write a concise project summary."])


class WorkflowRequest(BaseModel):
    workflow_name: str = Field(..., examples=["demo_runtime"])
    steps: list[WorkflowStep] = Field(..., min_length=1)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "workflow_name": "demo_runtime",
                "steps": [
                    {
                        "name": "plan_response",
                        "type": "prompt",
                        "input": "Draft a concise runtime plan.",
                    },
                    {
                        "name": "summarize_output",
                        "type": "summarize",
                        "input": "The runtime should expose execution state and trace details.",
                    },
                ],
            }
        }
    )


class PlannedStep(BaseModel):
    order: int
    name: str
    type: StepType
    input: str


class WorkflowPlan(BaseModel):
    step_count: int
    steps: list[PlannedStep]


class ValidationIssue(BaseModel):
    step_name: str
    message: str


class ValidationAttempt(BaseModel):
    attempt: int
    status: RunStatus
    issue_count: int
    started_at: datetime
    completed_at: datetime


class ValidationResult(BaseModel):
    status: RunStatus
    attempts: int
    issues: list[ValidationIssue] = Field(default_factory=list)
    attempt_history: list[ValidationAttempt] = Field(default_factory=list)
    started_at: datetime
    completed_at: datetime


class ExecutionState(BaseModel):
    status: RunStatus
    current_phase: RuntimePhase | None = None
    validation_attempts: int = 0
    total_steps: int = 0
    completed_steps: int = 0
    failed_steps: int = 0


class RuntimeEvent(BaseModel):
    timestamp: datetime
    phase: RuntimePhase
    status: RunStatus
    message: str
    details: dict[str, str | int | float | bool] = Field(default_factory=dict)


class ExecutionTrace(BaseModel):
    event_count: int
    events: list[RuntimeEvent]


class StepResult(BaseModel):
    name: str
    type: StepType
    status: RunStatus = RunStatus.completed
    started_at: datetime
    completed_at: datetime
    attempt: int = 1
    output: str


class WorkflowSummary(BaseModel):
    requested_steps: int
    planned_steps: int
    completed_steps: int
    failed_steps: int
    validation_attempts: int
    validation_passed: bool
    duration_ms: float


class WorkflowRun(BaseModel):
    run_id: str
    workflow_name: str
    runtime_status: RunStatus
    status: RunStatus
    started_at: datetime
    completed_at: datetime
    state: ExecutionState
    summary: WorkflowSummary
    plan: WorkflowPlan
    validation: ValidationResult
    results: list[StepResult]
    trace: ExecutionTrace

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "run_id": "f3d6a785-6e7a-41f0-8b55-0e9bfb15f3c2",
                "workflow_name": "demo_runtime",
                "runtime_status": "completed",
                "status": "completed",
                "started_at": "2026-05-07T03:00:00Z",
                "completed_at": "2026-05-07T03:00:00.015Z",
                "state": {
                    "status": "completed",
                    "current_phase": "executor",
                    "validation_attempts": 1,
                    "total_steps": 2,
                    "completed_steps": 2,
                    "failed_steps": 0,
                },
                "summary": {
                    "requested_steps": 2,
                    "planned_steps": 2,
                    "completed_steps": 2,
                    "failed_steps": 0,
                    "validation_attempts": 1,
                    "validation_passed": True,
                    "duration_ms": 15.2,
                },
                "plan": {
                    "step_count": 2,
                    "steps": [
                        {
                            "order": 1,
                            "name": "plan_response",
                            "type": "prompt",
                            "input": "Draft a concise runtime plan.",
                        },
                        {
                            "order": 2,
                            "name": "summarize_output",
                            "type": "summarize",
                            "input": "The runtime should expose execution state and trace details.",
                        },
                    ],
                },
                "validation": {
                    "status": "completed",
                    "attempts": 1,
                    "issues": [],
                    "attempt_history": [
                        {
                            "attempt": 1,
                            "status": "completed",
                            "issue_count": 0,
                            "started_at": "2026-05-07T03:00:00.002Z",
                            "completed_at": "2026-05-07T03:00:00.003Z",
                        }
                    ],
                    "started_at": "2026-05-07T03:00:00.002Z",
                    "completed_at": "2026-05-07T03:00:00.003Z",
                },
                "results": [
                    {
                        "name": "plan_response",
                        "type": "prompt",
                        "status": "completed",
                        "started_at": "2026-05-07T03:00:00.004Z",
                        "completed_at": "2026-05-07T03:00:00.010Z",
                        "attempt": 1,
                        "output": "Simulated model response for: Draft a concise runtime plan.",
                    }
                ],
                "trace": {
                    "event_count": 6,
                    "events": [
                        {
                            "timestamp": "2026-05-07T03:00:00Z",
                            "phase": "planner",
                            "status": "planned",
                            "message": "workflow planning started",
                            "details": {"workflow_name": "demo_runtime"},
                        }
                    ],
                },
            }
        }
    )


def new_run_id() -> str:
    return str(uuid4())


def utc_now() -> datetime:
    return datetime.now(timezone.utc)
