# Task Manager API

A layered FastAPI project that stores tasks in memory. Each running application
instance has its own tasks, and restarting it clears them.

## Run locally

Use Python 3.10 or newer. From the project directory in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Open [Swagger UI](http://127.0.0.1:8000/docs).

## Try the endpoints

Run these PowerShell examples in order in a second terminal. POST generates an
ID and sets the initial status to `pending`. The description defaults to an
empty string.

```powershell
$api = 'http://127.0.0.1:8000'

# Create a task (201)
$task = Invoke-RestMethod "$api/tasks" -Method Post -ContentType 'application/json' -Body '{"title":"Study FastAPI","description":"Try the Swagger UI"}'

# List all tasks (200)
Invoke-RestMethod "$api/tasks"

# Get one task (200)
Invoke-RestMethod "$api/tasks/$($task.id)"

# Update part of a task (200)
Invoke-RestMethod "$api/tasks/$($task.id)" -Method Patch -ContentType 'application/json' -Body '{"status":"completed"}'

# Delete a task (200)
Invoke-RestMethod "$api/tasks/$($task.id)" -Method Delete
```

PATCH accepts any combination of `title`, `description`, and `status` and
preserves omitted fields. The allowed statuses are `pending` and `completed`.
Send an empty string to clear the description. Missing tasks return 404, and
invalid input, including a whitespace-only title, returns 422.

## Run the tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Follow one request

The router maps each endpoint to a controller. The controller passes validated
request data from the schemas to the service. The service applies task rules
and uses the in-memory repository to store domain tasks.
