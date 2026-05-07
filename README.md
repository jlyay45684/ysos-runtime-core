# AI Runtime Orchestrator

Minimal FastAPI scaffold for demoing an AI runtime workflow orchestrator.

## What It Includes

- FastAPI app with generated Swagger docs
- Modular API, models, config, and runtime packages
- In-memory demo workflow execution
- Planner, validator, and executor runtime phases
- Execution state tracking and timestamps
- JSON runtime logging for workflow and step execution
- Validation retry handling before execution
- Workflow execution summary and trace in API responses
- Example request and response schemas in Swagger
- Dockerfile for containerized runs
- Small dependency surface

## Project Structure

```text
app/
  api/
    routes.py
  core/
    config.py
    logging.py
  models/
    workflow.py
  runtime/
    orchestrator.py
    planner.py
    steps.py
    validator.py
  main.py
Dockerfile
requirements.txt
```

## Run Locally

```bash
python -m venv venv
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open Swagger docs at:

```text
http://localhost:8000/docs
```

Set runtime options with environment variables:

```bash
AIO_LOG_LEVEL=DEBUG uvicorn app.main:app --reload
```

## Run With Docker

```bash
docker build -t ai-runtime-orchestrator .
docker run --rm -p 8000:8000 ai-runtime-orchestrator
```

Swagger docs are available in the container at:

```text
http://localhost:8000/docs
```

## Example Request

```bash
curl -X POST http://localhost:8000/api/workflows/run \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_name": "demo_runtime",
    "steps": [
      {
        "name": "draft_response",
        "type": "prompt",
        "input": "Write a concise project summary."
      },
      {
        "name": "summarize",
        "type": "summarize",
        "input": "The runtime accepts workflow steps and executes them in order."
      }
    ]
}'
```

The response includes the generated plan, validation attempts, execution state, per-step timestamps, runtime events, and step outputs.

## Response Shape

```json
{
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
    "failed_steps": 0
  },
  "summary": {
    "requested_steps": 2,
    "planned_steps": 2,
    "completed_steps": 2,
    "failed_steps": 0,
    "validation_attempts": 1,
    "validation_passed": true,
    "duration_ms": 15.2
  },
  "plan": {
    "step_count": 2,
    "steps": []
  },
  "validation": {
    "status": "completed",
    "attempts": 1,
    "issues": [],
    "attempt_history": []
  },
  "results": [],
  "trace": {
    "event_count": 7,
    "events": []
  }
}
```
