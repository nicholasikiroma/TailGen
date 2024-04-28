from pathlib import Path
import subprocess
import sys
import os
from collections import namedtuple

import typer


def _init_project_directory(project_path: Path, project_name: str) -> Path:
    """Create project directory"""
    project_dir = project_path / project_name
    project_dir.mkdir(parents=True, exist_ok=True)
    return project_dir


def _create_venv(project_dir_path: Path) -> None:
    """Creates and activates a virtual environment based on OS"""
    try:
        venv_dir = project_dir_path / "venv"
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)

    except subprocess.CalledProcessError:
        raise Exception("Failed to create environment")


def _get_setup_paths():
    SetupPaths = namedtuple("SetupPaths", ["flask", "fastapi"])

    if "__file__" in globals():
        # Running from the source directory
        package_path = os.path.dirname(os.path.abspath(__file__))
        flask_setup_files = os.path.join(package_path, "flask_app", "setup_files")
        fastapi_setup_files = os.path.join(package_path, "fastapi_app", "setup_files")
    else:
        # Running as an installed package
        import pkg_resources

        flask_setup_files = pkg_resources.resource_filename(
            "tailgen.flask_app.setup_files", ""
        )
        fastapi_setup_files = pkg_resources.resource_filename(
            "tailgen.fastapi_app.setup_files", ""
        )

    return SetupPaths(flask=flask_setup_files, fastapi=fastapi_setup_files)


def _create_git_ignore(project_dir: Path):
    """create .gitignore file in project"""
    try:
        with open(project_dir / ".gitignore", "w") as f:
            f.write(
                """.idea
.ipynb_checkpoints
node_modules
.mypy_cache
.vscode
__pycache__
.pytest_cache
htmlcov
dist
site
.coverage
coverage.xml
.netlify
test.db
log.txt
Pipfile.lock
env3.*
env
docs_build
site_build
venv
docs.zip
archive.zip

# vim temporary files
*~
.*.sw?
.cache

# macOS
.DS_Store
"""
            )
    except Exception as e:
        typer.secho(f"Failed to create .gitignore file: {e}")


def _git_init(project_dir: Path):
    """Initialize project as git repo"""
    try:
        subprocess.Popen(
            ["git", "init", project_dir.as_posix()],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
    except Exception as e:
        typer.secho(f"Failed to initialize git repository: {e}", fg=typer.colors.RED)
