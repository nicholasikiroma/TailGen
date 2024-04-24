import os
import subprocess
import sys
import venv
from pathlib import Path
import typer


def _init_project_directory(project_path: Path, project_name: str) -> Path:
    """Create project directory"""
    project_dir = project_path / project_name
    project_dir.mkdir(parents=True, exist_ok=True)
    return project_dir


def _create_and_activate_venv(project_dir_path: Path) -> None:
    """Creates and activates a virtual enviroment based on OS"""
    try:

        venv_dir = project_dir_path / "venv"
        venv.create(venv_dir, with_pip=True)
        if sys.platform == "win32":
            activate_script = os.path.join(venv_dir, "Scripts", "activate.bat")
            activation_command = f'cmd /k call "{activate_script}"'
        else:
            activate_script = os.path.join(venv_dir, "bin", "activate")
            activation_command = f'bash --rcfile "{activate_script}"'

        os.system(activation_command)

    except Exception:
        raise Exception("Failed to create virtual environment")


def _create_flask_project(project_dir: Path) -> None:
    """Create Flask Project"""
    install_process = subprocess.Popen(
        ["pip", "install", "flask"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )

    typer.secho("Installing Python...", fg=typer.colors.GREEN)

    while install_process.poll() is None:
        output = install_process.stdout.readline().strip()
        if output:
            typer.secho(output, fg=typer.colors.YELLOW)

    errors = install_process.stderr.read().strip()
    if errors:
        raise RuntimeError(f"Error install Flask: {errors}", fg=typer.colors.RED)

    typer.secho("Flask installed successfully.", fg=typer.colors.GREEN)

    typer.secho("Creating base Flask application...", fg=typer.colors.GREEN)

    with open(project_dir / "app.py", "w") as f:
        f.write(
            """from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)

"""
        )
    typer.secho("Creating static and templates directories.", fg=typer.colors.GREEN)
    # create static/ and templates/
    (project_dir / "static").mkdir(exist_ok=True)
    (project_dir / "templates").mkdir(exist_ok=True)

    typer.secho("Creating index HTML file", fg=typer.colors.GREEN)
    with open(project_dir / "templates" / "index.html", "w") as f:
        f.write(
            """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TailGen Template</title>
    <link rel="stylesheet" href="{{url_for('static',filename='dist/css/output.css')}}">
</head>
<body>
    <h1 class="text-blue-600">Created with TailGen</h1>
</body>
</html>
"""
        )

    typer.secho("Completed Flask setup", fg=typer.colors.GREEN)
