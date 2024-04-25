from pathlib import Path
import subprocess
import sys
import os
from collections import namedtuple


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
        fastapi_setup_files = os.path.join(package_path, "fastapi", "setup_files")
    else:
        # Running as an installed package
        import pkg_resources

        flask_setup_files = pkg_resources.resource_filename(
            "tailgen.flask.setup_files", ""
        )
        fastapi_setup_files = pkg_resources.resource_filename(
            "tailgen.fastapi.setup_files", ""
        )

    return SetupPaths(flask=flask_setup_files, fastapi=fastapi_setup_files)
