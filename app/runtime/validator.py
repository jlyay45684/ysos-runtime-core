from app.models.workflow import RunStatus, ValidationAttempt, ValidationIssue, ValidationResult
from app.models.workflow import WorkflowPlan, utc_now


MAX_VALIDATION_ATTEMPTS = 2


def validate_plan(plan: WorkflowPlan) -> ValidationResult:
    started_at = utc_now()
    attempt_history: list[ValidationAttempt] = []
    issues: list[ValidationIssue] = []

    for attempt in range(1, MAX_VALIDATION_ATTEMPTS + 1):
        attempt_started_at = utc_now()
        issues = _find_issues(plan)
        attempt_status = RunStatus.failed if issues else RunStatus.completed
        attempt_history.append(
            ValidationAttempt(
                attempt=attempt,
                status=attempt_status,
                issue_count=len(issues),
                started_at=attempt_started_at,
                completed_at=utc_now(),
            )
        )
        if not issues:
            break

    return ValidationResult(
        status=RunStatus.failed if issues else RunStatus.completed,
        attempts=len(attempt_history),
        issues=issues,
        attempt_history=attempt_history,
        started_at=started_at,
        completed_at=utc_now(),
    )


def _find_issues(plan: WorkflowPlan) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for step in plan.steps:
        if not step.name:
            issues.append(
                ValidationIssue(step_name=f"step_{step.order}", message="Step name is required.")
            )
        if not step.input:
            issues.append(
                ValidationIssue(step_name=step.name or f"step_{step.order}", message="Step input is required.")
            )
    return issues
