from pathlib import Path
import subprocess
from time import sleep
import typer
import shutil
from tailgen import DELAY_DURATION
from tailgen.helpers import _get_setup_paths
from rich.progress import Progress

package_path = _get_setup_paths()


def _create_flask_project(project_dir: Path) -> None:
    """Create Flask Project"""
    sleep(DELAY_DURATION)
    venv_dir = project_dir / "venv"
    install_process = subprocess.Popen(
        [str(venv_dir / "bin" / "pip"), "install", "flask"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    typer.secho("Installing Flask...", fg=typer.colors.GREEN)

    while install_process.poll() is None:
        output = install_process.stdout.readline().strip()
        if output:
            typer.secho(output, fg=typer.colors.YELLOW)
    sleep(DELAY_DURATION)
    errors = install_process.stderr.read().strip()
    if errors:
        raise RuntimeError(f"Error install Flask: {errors}", fg=typer.colors.RED)
    sleep(DELAY_DURATION)
    typer.secho("Flask installed successfully.", fg=typer.colors.GREEN)
    sleep(DELAY_DURATION)
    typer.secho("Creating base Flask application...", fg=typer.colors.GREEN)
    source = Path(package_path.flask) / "app.txt"
    destination = Path(project_dir) / "app.py"
    try:
        shutil.copyfile(source, destination)
    except Exception as e:
        raise Exception(f"Failed to create base Flask file: {e}")
    sleep(DELAY_DURATION)
    typer.secho("Creating static and templates directories.", fg=typer.colors.GREEN)
    # create static/ and templates/
    (project_dir / "static").mkdir(exist_ok=True)
    (project_dir / "templates").mkdir(exist_ok=True)

    typer.secho("Creating index HTML file", fg=typer.colors.GREEN)
    source = Path(package_path.flask) / "index.txt"
    destination = Path(project_dir) / "templates" / "index.html"
    try:
        shutil.copyfile(source, destination)
    except Exception as e:
        raise Exception(f"Failed to create base Flask file: {e}")
    sleep(DELAY_DURATION)
    typer.secho("Completed Flask setup", fg=typer.colors.GREEN)


def _install_and_configure_tailwindcss(project_dir: Path) -> None:
    """Install and configure Tailwind CSS"""

    with Progress() as progress:
        task = progress.add_task("[blue]Installing Tailwind CSS...", total=1)

        install_process = subprocess.Popen(
            ["npm", "install", "-D", "tailwindcss"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )

        for line in iter(install_process.stdout.readline, ""):
            progress.update(task, advance=1, color="red")

        # Wait for the installation process to complete
        install_process.communicate()

    typer.secho("Tailwind CSS installed successfully!", fg=typer.colors.GREEN)

    sleep(DELAY_DURATION)

    typer.secho("Creating Tailwind config file...", fg=typer.colors.GREEN)

    source = Path(package_path.flask) / "tailwind_config.txt"
    destination = project_dir / "tailwind.config.js"
    try:
        shutil.copyfile(source, destination)
    except Exception as e:
        raise Exception(f"Failed to create base Flask file: {e}")

    sleep(DELAY_DURATION)

    typer.secho("Creating file for input CSS", fg=typer.colors.GREEN)

    static_dir = project_dir / "static"
    (static_dir / "src").mkdir(exist_ok=True)
    with open(static_dir / "src" / "input.css", "w") as f:
        f.write(
            """@tailwind base;
@tailwind components;
@tailwind utilities;
"""
        )

    sleep(DELAY_DURATION)

    typer.secho("Completed tailwind config", fg=typer.colors.GREEN)
