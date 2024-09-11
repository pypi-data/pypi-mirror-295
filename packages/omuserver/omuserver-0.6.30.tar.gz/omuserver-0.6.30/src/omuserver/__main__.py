import io
import sys
import tracemalloc
from pathlib import Path

import click
from loguru import logger
from omu.address import Address

from omuserver.config import Config
from omuserver.migration import migrate
from omuserver.server.omuserver import OmuServer
from omuserver.version import VERSION


def setup_logging():
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8")
    if isinstance(sys.stderr, io.TextIOWrapper):
        sys.stderr.reconfigure(encoding="utf-8")
    logger.add(
        "logs/{time:YYYY-MM-DD}.log",
        rotation="1 day",
        colorize=False,
        format=(
            "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | "
            "{name}:{function}:{line} - {message}"
        ),
    )


@click.command()
@click.option("--debug", is_flag=True)
@click.option("--token", type=str, default=None)
@click.option("--token-file", type=click.Path(), default=None)
@click.option("--port", type=int, default=26423)
@click.option("--extra-trusted-origin", type=str, multiple=True)
def main(
    debug: bool,
    token: str | None,
    token_file: str | None,
    port: int,
    extra_trusted_origin: list[str],
):
    config = Config()
    config.address = Address(
        host=None,
        port=int(port),
        secure=False,
    )

    if token:
        config.dashboard_token = token
    elif token_file:
        config.dashboard_token = Path(token_file).read_text(encoding="utf-8").strip()
    else:
        config.dashboard_token = None

    config.extra_trusted_origins = list(extra_trusted_origin)
    if config.extra_trusted_origins:
        logger.info(f"Extra trusted hosts: {config.extra_trusted_origins}")

    if debug:
        logger.warning("Debug mode enabled")
        tracemalloc.start()

    server = OmuServer(config=config)

    migrate(server)

    logger.info(f"Starting omuserver v{VERSION} on {config.address.to_url()}")
    server.run()


if __name__ == "__main__":
    setup_logging()
    try:
        main()
    except Exception as e:
        logger.opt(exception=e).error("Error running server")
        sys.exit(1)
