from pathlib import Path
from typing import Optional

from dotenv import dotenv_values
from rich.console import Console
from rich.traceback import install as tr_install

console = Console()
tr_install(console=console)
