import logging

from app.models.workflow import ExecutionState, ExecutionTrace, RunStatus, RuntimeEvent, RuntimePhase
from app.models.workflow import StepResult, WorkflowRequest, WorkflowRun
from app.models.workflow import WorkflowSummary
from app.models.workflow import new_run_id, utc_now
from app.runtime.planner import build_plan
from app.runtime.steps import execute_step
from app.runtime.validator import validate_plan

logger = logging.getLogger(__name__)


class RuntimeOrchestrator:
    def run(self, request: WorkflowRequest) -> WorkflowRun:
        run_id = new_run_id()
        started_at = utc_now()
        events: list[RuntimeEvent] = []
        state = ExecutionState(
            status=RunStatus.planned,
            current_phase=RuntimePhase.planner,
            total_steps=len(request.steps),
        )
        _record_event(
            events,
            RuntimePhase.planner,
            RunStatus.planned,
            "workflow planning started",
            {"run_id": run_id, "workflow_name": request.workflow_name},
        )
        logger.info(
            "workflow run started",
            extra={
                "run_id": run_id,
                "workflow_name": request.workflow_name,
                "step_count": len(request.steps),
            },
        )

        plan = build_plan(request)
        _record_event(
            events,
            RuntimePhase.planner,
            RunStatus.completed,
            "workflow planning completed",
            {"run_id": run_id, "step_count": plan.step_count},
        )

        state.status = RunStatus.validating
        state.current_phase = RuntimePhase.validator
        _record_event(
            events,
            RuntimePhase.validator,
            RunStatus.validating,
            "workflow validation started",
            {"run_id": run_id},
        )
        validation = validate_plan(plan)
        state.validation_attempts = validation.attempts
        for attempt in validation.attempt_history:
            _record_event(
                events,
                RuntimePhase.validator,
                attempt.status,
                "workflow validation attempt completed",
                {
                    "run_id": run_id,
                    "attempt": attempt.attempt,
                    "issue_count": attempt.issue_count,
                },
            )
        _record_event(
            events,
            RuntimePhase.validator,
            validation.status,
            "workflow validation completed",
            {
                "run_id": run_id,
                "attempts": validation.attempts,
                "issue_count": len(validation.issues),
            },
        )

        results: list[StepResult] = []
        if validation.status == RunStatus.failed:
            completed_at = utc_now()
            state.status = RunStatus.failed
            state.current_phase = RuntimePhase.validator
            state.failed_steps = plan.step_count
            logger.warning(
                "workflow validation failed",
                extra={
                    "run_id": run_id,
                    "workflow_name": request.workflow_name,
                    "attempts": validation.attempts,
                    "issue_count": len(validation.issues),
                },
            )
            return WorkflowRun(
                run_id=run_id,
                workflow_name=request.workflow_name,
                runtime_status=RunStatus.failed,
                status=RunStatus.failed,
                started_at=started_at,
                completed_at=completed_at,
                state=state,
                summary=_build_summary(request, state, plan.step_count, validation.attempts, started_at, completed_at),
                plan=plan,
                validation=validation,
                results=results,
                trace=_build_trace(events),
            )

        state.status = RunStatus.running
        state.current_phase = RuntimePhase.executor
        for step in plan.steps:
            step_started_at = utc_now()
            logger.info(
                "executing workflow step",
                extra={
                    "run_id": run_id,
                    "step_name": step.name,
                    "step_type": step.type.value,
                },
            )
            _record_event(
                events,
                RuntimePhase.executor,
                RunStatus.running,
                "workflow step started",
                {"run_id": run_id, "step_name": step.name, "step_order": step.order},
            )
            output = execute_step(step)
            results.append(
                StepResult(
                    name=step.name,
                    type=step.type,
                    started_at=step_started_at,
                    completed_at=utc_now(),
                    output=output,
                )
            )
            state.completed_steps += 1
            _record_event(
                events,
                RuntimePhase.executor,
                RunStatus.completed,
                "workflow step completed",
                {"run_id": run_id, "step_name": step.name, "step_order": step.order},
            )

        completed_at = utc_now()
        state.status = RunStatus.completed
        state.current_phase = RuntimePhase.executor
        logger.info(
            "workflow run completed",
            extra={
                "run_id": run_id,
                "workflow_name": request.workflow_name,
                "step_count": len(results),
            },
        )
        return WorkflowRun(
            run_id=run_id,
            workflow_name=request.workflow_name,
            runtime_status=RunStatus.completed,
            status=RunStatus.completed,
            started_at=started_at,
            completed_at=completed_at,
            state=state,
            summary=_build_summary(request, state, plan.step_count, validation.attempts, started_at, completed_at),
            plan=plan,
            validation=validation,
            results=results,
            trace=_build_trace(events),
        )


def _record_event(
    events: list[RuntimeEvent],
    phase: RuntimePhase,
    status: RunStatus,
    message: str,
    details: dict[str, str | int | float | bool],
) -> None:
    events.append(
        RuntimeEvent(
            timestamp=utc_now(),
            phase=phase,
            status=status,
            message=message,
            details=details,
        )
    )
    logger.info(message, extra=details | {"phase": phase.value, "status": status.value})


def _build_summary(
    request: WorkflowRequest,
    state: ExecutionState,
    planned_steps: int,
    validation_attempts: int,
    started_at,
    completed_at,
) -> WorkflowSummary:
    return WorkflowSummary(
        requested_steps=len(request.steps),
        planned_steps=planned_steps,
        completed_steps=state.completed_steps,
        failed_steps=state.failed_steps,
        validation_attempts=validation_attempts,
        validation_passed=state.status != RunStatus.failed,
        duration_ms=round((completed_at - started_at).total_seconds() * 1000, 3),
    )


def _build_trace(events: list[RuntimeEvent]) -> ExecutionTrace:
    return ExecutionTrace(event_count=len(events), events=events)


orchestrator = RuntimeOrchestrator()
