# flake8: noqa E501
import os

import typer
import shutil
import subprocess
from pathlib import Path

app = typer.Typer(
    name="scaffold", help="Scaffold new Django apps", no_args_is_help=True
)


TEMPLATE_DIR = Path(__file__).resolve().parent


@app.command()
def startapp(
    app_name: str,
    destination: str = "apps",
    override: bool = False,
    template_url: str = None,
):
    """
    Create a new Django app using a custom template.
    :param app_name: Name of the new Django app.
    :param destination: Destination directory for the new app.
    :param override: Override the check for manage.py in the current working directory.
    """
    # Check if 'manage.py' exists in the current working directory
    if not Path("manage.py").exists() and not override:
        typer.echo(
            "Error: 'manage.py' not found. Please run this command from the Django project root directory."  # noqa
        )
        raise typer.Exit(code=1)
    Path.cwd() / "temp_template"
    # move the new app to the destination directory
    app_temp_path = Path.cwd() / app_name
    app_final_path = Path.cwd() / destination / app_name

    # Check if the final app directory already exists
    if app_final_path.exists():
        typer.echo(f"Error: The app directory '{app_final_path}' already exists.")
        raise typer.Exit(code=1)

    try:
        # Path where the new app will be created
        new_app_path = Path.cwd() / destination

        temp_template_url = (
            template_url or "https://cdn.advantch.com/template/app_template.zip"
        )

        # check no dir exists with the same name
        if Path(app_name).exists():
            typer.echo(
                f"Error: Directory with name '{app_name}' already exists. please choose a different name."  # noqa
            )
            raise typer.Exit(code=1)

        # Run the Django startapp command with the temporary template
        commands = [
            "docker",
            "compose",
            "run",
            "--rm",
            "django",
            "python",
            "manage.py",
            "startapp",
            app_name,
            "--template",
            str(temp_template_url),
        ]
        subprocess.run(commands, check=True)

        # Ensure the destination directory exists
        # use shutil to make an empty directory
        os.makedirs(new_app_path, exist_ok=True)

        shutil.move(app_temp_path, app_final_path)

        typer.echo(f"Successfully created new app: {app_name} at {new_app_path}")

        typer.echo("Remember to run `vanty dev-api update` when you add new endpoints")

    except Exception as e:
        typer.echo(f"Error: {e}")
