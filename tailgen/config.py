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
    """Creates and activates a virtual environment based on OS"""
    try:
        venv_dir = project_dir_path / "venv"
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)

    except subprocess.CalledProcessError:
        raise Exception("Failed to create environment")


def _create_flask_project(project_dir: Path) -> None:
    """Create Flask Project"""
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


def _install_and_configure_tailwindcss(project_dir: Path) -> None:
    """Install and configure Tailwind CSS"""
    install_process = subprocess.Popen(
        ["npm", "install", "-D", "tailwindcss"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    typer.secho("Installing Tailwind CSS...", fg=typer.colors.GREEN)

    while install_process.poll() is None:
        output = install_process.stdout.readline().strip()
        if output:
            typer.secho(output, fg=typer.colors.BLUE)

    errors = install_process.stderr.read().strip()
    if errors:
        raise RuntimeError(f"Error install Tailwind CSS: {errors}", fg=typer.colors.RED)

    typer.secho("Tailwind CSS installed successfully.", fg=typer.colors.GREEN)
    typer.secho("Creating Tailwind config file...", fg=typer.colors.GREEN)
    with open(project_dir / "tailwind.config.js", "w") as f:
        f.write(
            """/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/src/**/*.js"
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
"""
        )
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
    typer.secho("Completed tailwind config", fg=typer.colors.GREEN)
