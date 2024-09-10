import click

@click.command()
def test_command():
    """Test command to verify CLI setup."""
    click.echo("Test command executed.")
