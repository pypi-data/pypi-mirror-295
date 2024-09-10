from click import Group

from .configure_main import config_main
from .init import init
from .test import test_command

# Create a Click group
fastapi_easystart_cli = Group()

# Register the init_files and config_main commands with the CLI group
fastapi_easystart_cli.add_command(init)
fastapi_easystart_cli.add_command(config_main)
fastapi_easystart_cli.add_command(test_command)

__all__ = ["fastapi_easystart_cli"]
