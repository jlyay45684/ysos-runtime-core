from app.models.workflow import PlannedStep, WorkflowPlan, WorkflowRequest


def build_plan(request: WorkflowRequest) -> WorkflowPlan:
    steps = [
        PlannedStep(
            order=index,
            name=step.name.strip(),
            type=step.type,
            input=step.input.strip(),
        )
        for index, step in enumerate(request.steps, start=1)
    ]
    return WorkflowPlan(step_count=len(steps), steps=steps)
