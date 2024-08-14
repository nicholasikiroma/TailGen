from pathlib import Path
import subprocess
import sys
import os
from collections import namedtuple

import typer
from rich import print
from rich.panel import Panel
from rich.console import Console
from rich.text import Text

console = Console()


def setup_complete(framework: str):
    title_text = Text("🎉 Setup Complete!", justify="center")
    message_text = Text(
        f"\nYour TailwindCSS setup with {framework} is ready to go! 🚀\n",
        justify="center",
        style="white",
    )
    next_steps = f"""
    Next steps:
    1. Run command: `npx tailwindcss -i ./static/src/input.css -o ./static/dist/css/output.css --watch` to build CSS from templates. 
    2. Activate virtual environment
    3. Start the development server and see the magic.
    4. Customize your TailwindCSS config to suit your needs.
    5. Build something awesome!
    """

    panel = Panel.fit(
        message_text + next_steps,
        title=title_text,
        border_style="bright_magenta",
        padding=(1, 10),
    )
    console.print(panel)


def _init_project_directory(project_path: Path, project_name: str) -> Path:
    """Create project directory"""
    project_dir = project_path / project_name
    project_dir.mkdir(parents=True, exist_ok=True)
    return project_dir


def _create_venv(project_dir_path: Path) -> None:
    """Creates virtual environment"""
    try:
        venv_dir = project_dir_path / "venv"
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)

        # Determine the path to the Python executable in the virtual environment
        if os.name == "nt":  # Windows
            python_executable = venv_dir / "Scripts" / "python"
        else:  # POSIX (Linux, macOS, etc.)
            python_executable = venv_dir / "bin" / "python"

        # Ensure pip is installed in the virtual environment
        subprocess.run([str(python_executable), "-m", "ensurepip"], check=True)

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


def _create_git_ignore(project_dir: Path) -> None:
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


def _git_init(project_dir: Path) -> None:
    """Initialize project as git repo"""
    try:
        # Ensure project_dir is a string path compatible with the OS
        result = subprocess.run(
            ["git", "init", str(project_dir)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            check=True,  # Raises CalledProcessError if git init fails
        )

        # Optionally, print the output for debugging purposes
        typer.secho(result.stdout, fg=typer.colors.GREEN)

    except subprocess.CalledProcessError as e:
        typer.secho(
            f"Failed to initialize git repository: {e.stderr}", fg=typer.colors.RED
        )
    except Exception as e:
        typer.secho(f"Unexpected error: {e}", fg=typer.colors.RED)


def _create_readme(project_dir: Path) -> None:
    """Create default readme file for project"""
    try:
        with open(project_dir / "README.md", "w") as f:
            f.write(
                """# Project Title

Simple overview of use/purpose.

## Description

An in-depth paragraph about your project and overview of use.

## Getting Started

### Dependencies

* Describe any prerequisites, libraries, OS version, etc., needed before installing program.
* ex. Windows 10

### Installing

* How/where to download your program
* Any modifications needed to be made to files/folders

### Executing program

* How to run the program
* Step-by-step bullets
```
code blocks for commands
```

## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

Contributors names and contact info

ex. Dominique Pizzie  
ex. [@DomPizzie](https://twitter.com/dompizzie)

## Version History

* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
"""
            )

    except Exception as e:
        typer.secho(f"Failed to create readme file: {e}", fg=typer.colors.RED)
