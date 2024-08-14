from pathlib import Path
import re
import subprocess
from sys import platform
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
    pip_executable = (
        "Scripts/pip.exe"
        if platform.startswith("win32") or platform.startswith("cygwin")
        else "bin/pip"
    )
    install_process = subprocess.Popen(
        [str(venv_dir / pip_executable), "install", "flask"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    typer.secho(
        "Safely installing Flask and other python dependencies to virtual environment...",
        fg=typer.colors.GREEN,
    )

    while install_process.poll() is None:
        output = install_process.stdout.readline().strip()
        if output:
            typer.secho(output, fg=typer.colors.BRIGHT_MAGENTA)
    sleep(DELAY_DURATION)
    errors = install_process.stderr.read().strip()

    if errors:
        # Regular expression to match any notice that starts with "[notice]"
        pip_notice_pattern = r"\[notice\].*?(\n|$)"

        # Find all pip notices
        if re.search(pip_notice_pattern, errors, re.IGNORECASE):
            typer.secho(
                "Notice: pip is outdated. Consider updating.", fg=typer.colors.RED
            )

        # Remove all pip notices from the error message
        errors = re.sub(pip_notice_pattern, "", errors, flags=re.IGNORECASE).strip()

        # If there are still errors after removing the pip notice, raise an exception
        if errors:
            error_message = f"Error installing Flask: {errors}"
            raise RuntimeError(error_message)

    sleep(DELAY_DURATION)
    typer.secho("Flask installed successfully.", fg=typer.colors.GREEN)
    sleep(DELAY_DURATION)
    typer.secho("Creating base Flask application...", fg=typer.colors.GREEN)
    source = Path(package_path.flask) / "app.txt"
    destination = Path(project_dir) / "app.py"
    try:
        shutil.copyfile(source, destination)
    except Exception as e:
        raise Exception(f"Failed to create base Flask file: {str(e)}")
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
        raise Exception(f"Failed to create base Flask file: {str(e)}")
    sleep(DELAY_DURATION)
    typer.secho("Completed Flask setup", fg=typer.colors.GREEN)


def _install_and_configure_tailwindcss(project_dir: Path) -> None:
    """Install and configure Tailwind CSS"""

    with Progress() as progress:
        task = progress.add_task("[blue]Installing Tailwind CSS...", total=1)

        install_process = subprocess.Popen(
            [
                "npm",
                "install",
                "tailwindcss",
                "--prefix",
                project_dir.as_posix(),
                "--save-dev",
            ],
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
        raise Exception(f"Failed to create base Flask file: {str(e)}")

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
