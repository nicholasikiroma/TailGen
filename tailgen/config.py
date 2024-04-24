import os
import sys
import venv
from pathlib import Path


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

    except Exception as e:
        raise
