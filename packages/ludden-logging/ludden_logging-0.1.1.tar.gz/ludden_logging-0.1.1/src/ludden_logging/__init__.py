from pathlib import Path
from typing import Optional

from dotenv import dotenv_values
from rich.console import Console
from rich.traceback import install as tr_install

from ludden_logging.run import Run
from ludden_logging.log import Log

__all__ = [
    "log",
    "console"
]

console = Console()
tr_install(console=console)

log = Log(Run())
