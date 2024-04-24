import typer
from typing import Optional
from tailgen import __app_name__, __version__, VALID_FRAMEWORKS
from .config import (
    _init_project_directory,
    _create_and_activate_venv,
    _create_flask_project,
)
from pathlib import Path

app = typer.Typer()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


def _valid_framework(value: str):
    if value.lower() not in VALID_FRAMEWORKS:
        raise typer.BadParameter(
            f"Framework must be either 'flask' or 'fastapi', not {value}."
        )
    return value.lower()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return


@app.command()
def init(
    project_name: str = typer.prompt(
        "What is the project name?\n(Name of the project to initialize. Press enter to use 'new_project' as default.)",
        default="new_project",
    ),
    framework: str = typer.Option(
        "flask",
        "--framework",
        "-f",
        help="Web framework to use (flask/fastapi)",
        callback=_valid_framework,
    ),
    tailwind_version: str = typer.Option(
        "2.2.19",
        "--tailwind-version",
        help="Tailwind CSS version to use. If not provided, the latest Tailwind CSS version is used.",
    ),
    output_dir: str = typer.Option(
        ".",
        "--output-dir",
        "-o",
        help="Directory where the project will be initialized",
    ),
) -> None:
    """Initialize a new Flask or FastAPI project with Tailwind CSS integration."""
    typer.secho(
        f"Initializing {framework} project named {project_name} with Tailwind CSS {tailwind_version}",
        fg=typer.colors.GREEN,
    )
    typer.secho(f"Creating project directory", fg=typer.colors.GREEN)
    if output_dir:
        project_path = Path(output_dir).expanduser().resolve()
    else:
        project_name = Path.cwd()

    project_dir_path = _init_project_directory(project_path, project_name)

    typer.secho(f"Create and activate virtual environment", fg=typer.colors.GREEN)
    # To-do: Create and activate virtual environment
    _create_and_activate_venv(project_dir_path)

    if framework == "flask":
        _create_flask_project(project_dir_path)

    elif framework == "fastapi":
        raise NotImplementedError("Implementation is in progress")

    else:
        raise ValueError("Invalid framework selected.")
