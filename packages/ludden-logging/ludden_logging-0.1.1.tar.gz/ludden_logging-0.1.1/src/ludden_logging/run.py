import os
from pathlib import Path
from typing import Optional

from rich.console import Console

from ludden_logging import console

class Run:
    """Class to track the number of runs of a module, stored in both a file and an environment variable."""

    def __init__(self, project_name: Optional[str] = None, run_file: Optional[Path] = None, console: Console = console, verbose: bool = False) -> None:
        """Initialize the Run class and load the run count.

        Args:
            project_name (Optional[str], optional): The name of the project for setting up the environment variable.
            run_file (Optional[Path], optional): The file where the run count is stored. Defaults to 'logs/run.txt'.
        """
        self.project_name = project_name or self.get_project_name()
        self.verbose: bool = verbose
        if verbose:
            console.log(f"Project name: {self.project_name}")
        self.env_var_name = f"{self.project_name.upper()}_RUN_COUNT"

        # Default log file location
        self.run_file = run_file or Path("logs/run.txt")
        self.run_file.parent.mkdir(parents=True, exist_ok=True)  # Ensure the log directory exists

        self.run = self.load_run_count()

    def load_run_count(self) -> int:
        """Load the current run count from the run file and set it to an environment variable.

        Returns:
            int: The current run count.
        """
        if self.run_file.exists():
            try:
                # Load from the file
                with open(self.run_file, 'r', encoding='utf-8') as file:
                    run_count = int(file.read().strip())
            except (ValueError, FileNotFoundError):
                run_count = 0
        else:
            # File doesn't exist, initialize it and notify the user
            run_count = 0
            print(f"Run file '{self.run_file}' does not exist. Creating it with an initial count of 0.")
            self.save_run_count(run_count)

        # Set the run count in the environment variable
        os.environ[self.env_var_name] = str(run_count)

        return run_count

    def increment_run_count(self) -> None:
        """Increment the run count, save it to both the run file and the environment variable."""
        self.run += 1
        self.save_run_count(self.run)

    def reset_run_count(self) -> None:
        """Reset the run count to 0 and save it to both the run file and the environment variable."""
        self.run = 0
        self.save_run_count(self.run)

    def save_run_count(self, run_count: int) -> None:
        """Save the run count to the run file and set it in the environment variable.

        Args:
            run_count (int): The run count to be saved.
        """
        # Save to the file
        with open(self.run_file, 'w', encoding='utf-8') as file:
            file.write(str(run_count))

        # Set the run count in the environment variable
        os.environ[self.env_var_name] = str(run_count)
        if self.verbose:
            console.line(2)
            console.print(
                f"[b i #af00ff]Run count updated to [b not italic #0099ff]{run_count}[/]. \
Stored in [b not italic #ff9900]{self.run_file}[/] and environment variable [b not italic #cccccc]{self.env_var_name}.[/][/]")

    def get_project_name(self) -> str:
        """Get the project name from the pyproject.toml file."""
        try:
            with open("pyproject.toml", 'r', encoding='utf-8') as file:
                for line in file:
                    if "name" in line:
                        return line.split(' = ')[1].strip().strip('"')
        except FileNotFoundError:
            print("No 'pyproject.toml' file found. Using a default project name.")
            return "default_project"

        return Path(__file__).parent.name


# Example usage:
if __name__ == "__main__":
    # project_name = "ludden-logging"  # This could be dynamically determined, e.g., from config
    run_tracker = Run(verbose=True)

    console.print(f"Current run count: {run_tracker.run}")

    # Increment the run count
    run_tracker.increment_run_count()
    console.print(f"Run count after incrementing: {run_tracker.run}")

    # The run count is now also available in the environment
    console.print(f"Environment variable '{run_tracker.env_var_name}': {os.getenv(run_tracker.env_var_name)}")
