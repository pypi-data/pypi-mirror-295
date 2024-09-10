import logging

from pa_api.commands.utils import set_default_logger

from .commands import cli

set_default_logger()
logging.getLogger().setLevel(logging.INFO)

if __name__ == "__main__":
    cli()
