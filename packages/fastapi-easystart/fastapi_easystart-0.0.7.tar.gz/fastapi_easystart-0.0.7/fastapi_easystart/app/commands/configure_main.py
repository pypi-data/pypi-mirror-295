import os
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()


@click.command()
def config_main():
    """Configure the main.py file by copying content from main.txt in the config directory."""
    # Define paths
    config_dir = Path(__file__).parent  # Path to the config directory
    main_txt_path = config_dir / "main.txt"  # Path to the main.txt file
    project_root_dir = Path(os.getcwd())  # Path to the root directory
    main_py_path = project_root_dir / "main.py"  # Path to the main.py file in the root directory

    # Debug output
    console.print(f"Config Directory: {config_dir}", style="cyan")
    console.print(f"main.txt Path: {main_txt_path}", style="cyan")
    console.print(f"Root Directory: {project_root_dir}", style="cyan")
    console.print(f"main.py Path: {main_py_path}", style="cyan")

    # Check if the main.txt file exists
    if main_txt_path.exists():
        # Check if main.py already exists in the root directory
        if main_py_path.exists():
            # Ask the user whether to override or merge the file
            action = Prompt.ask(
                "main.py already exists in the root directory. Do you want to (O)verride or (M)erge the file?",
                choices=["O", "M"],
                default="O"
            )
            if action.upper() == "O":
                try:
                    # Copy content from main.txt to main.py
                    with open(main_txt_path, "r") as src_file:
                        new_content = src_file.read()

                    with open(main_py_path, "w") as dest_file:
                        dest_file.write(new_content)

                    console.print(Panel("Configured the existing main.py file with the new content (overridden).", style="green"), style="bold green")
                except Exception as e:
                    console.print(Panel(f"Error configuring file: {e}", style="red"), style="bold red")
            elif action.upper() == "M":
                # Read existing content
                with open(main_py_path, "r") as f:
                    existing_content = f.read()

                # Read new content
                with open(main_txt_path, "r") as f:
                    new_content = f.read()

                # Merge the content
                merged_content = f"# Merged content from the new configuration\n\n{new_content}\n\n# Existing content\n{existing_content}"

                # Write merged content to the file
                try:
                    with open(main_py_path, "w") as f:
                        f.write(merged_content)
                    console.print(Panel("Configured the existing main.py file with the merged content.", style="green"), style="bold green")
                except Exception as e:
                    console.print(Panel(f"Error merging content: {e}", style="red"), style="bold red")
        else:
            try:
                # Create main.py in the root directory with content from main.txt
                with open(main_txt_path, "r") as src_file:
                    new_content = src_file.read()

                with open(main_py_path, "w") as dest_file:
                    dest_file.write(new_content)

                console.print(Panel("Created main.py in the root directory with the new content.", style="green"), style="bold green")
            except Exception as e:
                console.print(Panel(f"Error creating file: {e}", style="red"), style="bold red")
    else:
        console.print(Panel("The main.txt configuration does not exist in the config directory.", style="red"), style="bold red")
