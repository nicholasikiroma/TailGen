import os
import sys
import venv


def create_and_activate_venv(venv_dir="venv"):
    """Creates and activates a virtual enviroment based on OS"""
    venv.create(venv_dir, with_pip=True)
    if sys.platform == "win32":
        activate_script = os.path.join(venv_dir, "Scripts", "activate.bat")
        activation_command = f'cmd /k call "{activate_script}"'
    else:
        activate_script = os.path.join(venv_dir, "bin", "activate")
        activation_command = f'bash --rcfile "{activate_script}"'

    os.system(activation_command)


if __name__ == "__main__":
    create_and_activate_venv()
