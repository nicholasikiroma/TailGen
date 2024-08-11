import typer
from typing import Optional
from pathlib import Path
from time import sleep

from tailgen import __app_name__, __version__, VALID_FRAMEWORKS, DELAY_DURATION
from tailgen.flask_app import _create_flask_project, _install_and_configure_tailwindcss
from tailgen.fastapi_app import (
    _create_fastapi_project,
    _install_and_configure_tailwindcss_fastapi,
)
from tailgen.helpers import (
    _create_git_ignore,
    _create_readme,
    _create_venv,
    _git_init,
    _init_project_directory,
    setup_complete,
)

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
    framework: str = typer.Option(
        "flask",
        "--framework",
        "-f",
        help="Web framework to use (flask/fastapi)",
        callback=_valid_framework,
    ),
    output_dir: str = typer.Option(
        ".",
        "--output-dir",
        "-o",
        help="Directory where the project will be initialized",
    ),
) -> None:
    """Initialize a new Flask or FastAPI project with Tailwind CSS integration."""

    project_name: str = typer.prompt(
        "Provide a project name\n(Name of the project to initialize. Press enter to use default.)",
        default="new_project",
    )
    sleep(DELAY_DURATION)

    typer.secho(
        f"Initializing {framework} project named {project_name} with the latest Tailwind CSS version.",
        fg=typer.colors.GREEN,
    )

    sleep(DELAY_DURATION)
    typer.secho(f"Creating project directory", fg=typer.colors.GREEN)
    if output_dir:
        project_path = Path(output_dir).expanduser().resolve()
    else:
        project_name = Path.cwd()

    project_dir_path = _init_project_directory(project_path, project_name)

    sleep(DELAY_DURATION)
    typer.secho(f"Create virtual environment", fg=typer.colors.GREEN)

    _create_venv(project_dir_path)
    sleep(DELAY_DURATION)

    typer.secho(f"Creating .gitignore file", fg=typer.colors.GREEN)
    _create_git_ignore(project_dir_path)
    sleep(DELAY_DURATION)

    typer.secho(f"Creating README.md file", fg=typer.colors.GREEN)
    _create_readme(project_dir_path)
    sleep(DELAY_DURATION)

    typer.secho("Initializing Git", fg=typer.colors.GREEN)
    _git_init(project_dir_path)
    sleep(DELAY_DURATION)

    if framework == "flask":
        _create_flask_project(project_dir_path)
        _install_and_configure_tailwindcss(project_dir_path)

    elif framework == "fastapi":
        _create_fastapi_project(project_dir_path)
        _install_and_configure_tailwindcss_fastapi(project_dir_path)

    else:
        raise ValueError("Invalid framework selected.")
    sleep(DELAY_DURATION)
    setup_complete(framework)
