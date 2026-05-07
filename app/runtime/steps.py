from app.models.workflow import PlannedStep, StepType


def execute_step(step: PlannedStep) -> str:
    handlers = {
        StepType.prompt: _run_prompt_step,
        StepType.tool: _run_tool_step,
        StepType.summarize: _run_summary_step,
    }
    return handlers[step.type](step.input)


def _run_prompt_step(step_input: str) -> str:
    return f"Simulated model response for: {step_input}"


def _run_tool_step(step_input: str) -> str:
    return f"Simulated tool execution with input: {step_input}"


def _run_summary_step(step_input: str) -> str:
    return f"Summary: {step_input[:120]}"
