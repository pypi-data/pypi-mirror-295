from invoke import task

@task(default=True)
def api(ctx):
    """Starts the FastAPI application using uvicorn."""
    ctx.run("python -m api.main")