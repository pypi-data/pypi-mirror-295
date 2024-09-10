from invoke import task


@task
def create(ctx, message):
    """Create a new database migration file with a message."""
    ctx.run(f'alembic revision --autogenerate -m "{message}"')


@task
def upgrade(ctx):
    """Apply all pending database migrations."""
    ctx.run("alembic upgrade head")


@task
def downgrade(ctx):
    """Revert the last applied database migration."""
    ctx.run("alembic downgrade -1")
