# Entrypoint

import os

import click
import uvicorn

from settings.settings import settings


@click.command()
@click.option(
    "--env",
    type=click.Choice(["local", "dev", "prod"], case_sensitive=False),
    default="local",
)
@click.option(
    "--debug",
    type=click.BOOL,
    is_flag=True,
    default=False,
)
def main(env: str, debug: bool):
    os.environ["ENV"] = env
    os.environ["DEBUG"] = str(debug)
    uvicorn.run(
        app="api.main_router:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=True,
        workers=1,
    )


if __name__ == "__main__":
    main()
