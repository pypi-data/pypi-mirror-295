from typing import Annotated

import typer

from gptcomet.config_manager import ConfigManager, get_config_manager
from gptcomet.const import GPTCOMET_PRE
from gptcomet.log import logger, set_debug
from gptcomet.utils import console


def entry(
    provider: Annotated[str, typer.Argument(..., help="Name of the provider.")],
    debug: Annotated[
        bool, typer.Option("--debug", "-d", help="Print debug information.")
    ] = False,
    local: Annotated[
        bool, typer.Option("--local", help="Use local configuration file.")
    ] = False,
):
    cfg: ConfigManager = get_config_manager(local=local)
    if debug:
        set_debug()
        logger.debug(f"Using Config path: {cfg.current_config_path}")
    cfg.add_provider(provider)
    cfg.save_config()
    console.print(f"{GPTCOMET_PRE} Added provider {provider} to config.")
