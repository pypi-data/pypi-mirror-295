import os
import shutil
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel

console = Console()

# Define the path to the template directory you want to copy
TEMPLATE_ROOT_DIR = Path(__file__).parent
TEMPLATE_DIR = TEMPLATE_ROOT_DIR / "init_files"


@click.command()
def init():
    """Initialize a new FastAPI project by creating an app directory and copying template files."""
    project_root_dir = Path(os.getcwd())
    app_dir = project_root_dir / "app"
    env_file_path = project_root_dir / ".env"
    static_file_dir = project_root_dir / "static"
    favicon_ico_file_path = project_root_dir / "favicon.ico"
    original_favicon_ico_file_path = TEMPLATE_ROOT_DIR / "favicon.ico"

    # Debug output
    console.print(f"TEMPLATE_DIR: {TEMPLATE_DIR}", style="cyan")
    console.print(f"APP_DIR: {app_dir}", style="cyan")
    console.print(f"ENV_FILE_PATH: {env_file_path}", style="cyan")

    if TEMPLATE_DIR.exists():
        console.print(Panel(f"Template directory exists: {TEMPLATE_DIR}", style="green"), style="bold green")
    else:
        console.print(Panel(f"Template directory does not exist: {TEMPLATE_DIR}", style="red"), style="bold red")
        return

    if app_dir.exists():
        console.print(Panel(f"Directory 'app' already exists in {os.getcwd()}. Copying template files...", style="yellow"), style="bold yellow")
    else:
        console.print(Panel(f"Creating 'app' directory in {os.getcwd()}...", style="blue"), style="bold blue")
        app_dir.mkdir(parents=True)

    # Copy all files and directories from TEMPLATE_DIR to the 'app' directory
    try:
        shutil.copytree(TEMPLATE_DIR, app_dir, dirs_exist_ok=True)
        console.print(Panel(f"Template files copied to '{app_dir}'.", style="green"), style="bold green")
    except Exception as e:
        console.print(Panel(f"Error copying files: {e}", style="red"), style="bold red")
        return

    # Check if .env file exists and update or create it
    if env_file_path.exists():
        with open(env_file_path, "r") as f:
            lines = f.readlines()

        # Check if FA_ENVIRONMENT is already set
        fa_environment_set = any(line.startswith("FA_ENVIRONMENT=") for line in lines)

        if fa_environment_set:
            console.print(Panel(f"Updating existing .env file with FA_ENVIRONMENT.", style="yellow"), style="bold yellow")
            new_lines = []
            for line in lines:
                if line.startswith("FA_ENVIRONMENT="):
                    new_lines.append("FA_ENVIRONMENT='dev' # dev, prod, local\n")
                else:
                    new_lines.append(line)
            # Write updated content
            with open(env_file_path, "w") as f:
                f.writelines(new_lines)
        else:
            console.print(Panel(f"Adding FA_ENVIRONMENT to existing .env file.", style="yellow"), style="bold yellow")
            with open(env_file_path, "a") as f:
                f.write("\nFA_ENVIRONMENT='dev' # dev, prod, local\n")
    else:
        console.print(Panel(f".env file does not exist. Creating and adding FA_ENVIRONMENT.", style="blue"), style="bold blue")
        with open(env_file_path, "w") as f:
            f.write("FA_ENVIRONMENT='dev' # dev, prod, local\n")

    console.print(Panel(f".env file setup complete.", style="green"), style="bold green")

    if not static_file_dir.exists():
        console.print(Panel(f"Creating 'static' directory in {os.getcwd()}...", style="blue"), style="bold blue")
        static_file_dir.mkdir(parents=True)
        
    # Check if the file exists in the config directory
    if not favicon_ico_file_path.exists():
        try:
            shutil.copy(str(original_favicon_ico_file_path), str(static_file_dir))
            # console.print(Panel(f"Moved {favicon_ico_file_path} to {static_file_dir}.", style="green"), style="bold green")
        except Exception as e:
            console.print(Panel(f"Error moving file: {e}", style="red"), style="bold red")

    console.print(Panel(f"static directory setup complete.", style="green"), style="bold green")
