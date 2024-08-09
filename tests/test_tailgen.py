# tests/test_cli.py
import pytest
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
from pathlib import Path
from tailgen import __app_name__, __version__, cli

runner = CliRunner()


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout


def mock_user_input(prompt: str) -> str:
    return "new_project"


def test_init_command_flask():
    with patch(
        "tailgen.cli._init_project_directory", return_value=Path("/tmp/test_project")
    ) as mock_init_dir, patch("tailgen.cli._create_venv") as mock_create_venv, patch(
        "tailgen.cli._create_git_ignore"
    ) as mock_create_git_ignore, patch(
        "tailgen.cli._create_readme"
    ) as mock_create_readme, patch(
        "tailgen.cli._git_init"
    ) as mock_git_init, patch(
        "tailgen.cli._create_flask_project"
    ) as mock_create_flask, patch(
        "tailgen.cli._install_and_configure_tailwindcss"
    ) as mock_install_tailwind, patch(
        "tailgen.cli.sleep", return_value=None
    ), patch(
        "tailgen.cli.input", side_effect=mock_user_input
    ):
        # Test initialization with default framework (Flask)
        result = runner.invoke(cli.app, ["init"])
        assert result.exit_code == 0
        assert "Provide a project name" in result.stdout
        assert (
            "Initializing flask project named new_project with Tailwind CSS 2.2.19"
            in result.stdout
        )
        assert "Creating project directory" in result.stdout
        mock_init_dir.assert_called_once_with(
            Path("/home/puppetmaster/Desktop/projects/TailGen"), "new_project"
        )
        mock_create_venv.assert_called_once_with(Path("/tmp/test_project"))
        mock_create_git_ignore.assert_called_once_with(Path("/tmp/test_project"))
        mock_create_readme.assert_called_once_with(Path("/tmp/test_project"))
        mock_git_init.assert_called_once_with(Path("/tmp/test_project"))
        mock_create_flask.assert_called_once_with(Path("/tmp/test_project"))
        mock_install_tailwind.assert_called_once_with(Path("/tmp/test_project"))


def test_init_command_fastapi():
    with patch(
        "tailgen.cli._init_project_directory",
        return_value=Path("/tmp/test_project_fastapi"),
    ) as mock_init_dir, patch("tailgen.cli._create_venv") as mock_create_venv, patch(
        "tailgen.cli._create_git_ignore"
    ) as mock_create_git_ignore, patch(
        "tailgen.cli._create_readme"
    ) as mock_create_readme, patch(
        "tailgen.cli._git_init"
    ) as mock_git_init, patch(
        "tailgen.cli._create_fastapi_project"
    ) as mock_create_fastapi, patch(
        "tailgen.cli._install_and_configure_tailwindcss_fastapi"
    ) as mock_install_tailwind_fastapi, patch(
        "tailgen.cli.sleep", return_value=None
    ), patch(
        "tailgen.cli.input", side_effect=mock_user_input
    ):
        # Test initialization with custom framework (FastAPI)
        result = runner.invoke(cli.app, ["init", "--framework", "fastapi"])
        assert result.exit_code == 0
        assert (
            "Initializing fastapi project named new_project with Tailwind CSS 2.2.19"
            in result.stdout
        )
        assert "Creating project directory" in result.stdout
        mock_init_dir.assert_called_once_with(
            Path("/home/puppetmaster/Desktop/projects/TailGen"), "new_project"
        )
        mock_create_venv.assert_called_once_with(Path("/tmp/test_project_fastapi"))
        mock_create_git_ignore.assert_called_once_with(
            Path("/tmp/test_project_fastapi")
        )
        mock_create_readme.assert_called_once_with(Path("/tmp/test_project_fastapi"))
        mock_git_init.assert_called_once_with(Path("/tmp/test_project_fastapi"))
        mock_create_fastapi.assert_called_once_with(Path("/tmp/test_project_fastapi"))
        mock_install_tailwind_fastapi.assert_called_once_with(
            Path("/tmp/test_project_fastapi")
        )


def test_init_command_flask_with_output_dir():
    with patch(
        "tailgen.cli._init_project_directory", return_value=Path("/tmp/test_project")
    ) as mock_init_dir, patch("tailgen.cli._create_venv") as mock_create_venv, patch(
        "tailgen.cli._create_git_ignore"
    ) as mock_create_git_ignore, patch(
        "tailgen.cli._create_readme"
    ) as mock_create_readme, patch(
        "tailgen.cli._git_init"
    ) as mock_git_init, patch(
        "tailgen.cli._create_flask_project"
    ) as mock_create_flask, patch(
        "tailgen.cli._install_and_configure_tailwindcss"
    ) as mock_install_tailwind, patch(
        "tailgen.cli.sleep", return_value=None
    ), patch(
        "builtins.input", lambda _: "new_project"
    ):
        # Test initialization with output directory and default framework (Flask)
        result = runner.invoke(cli.app, ["init", "--output-dir", "/tmp/test_project"])
        assert result.exit_code == 0
        assert "Creating project directory" in result.stdout
        assert "new_project" in result.stdout  # Ensuring the mock project name is used
        mock_init_dir.assert_called_once_with(Path("/tmp/test_project"), "new_project")
        mock_create_venv.assert_called_once_with(Path("/tmp/test_project"))
        mock_create_git_ignore.assert_called_once_with(Path("/tmp/test_project"))
        mock_create_readme.assert_called_once_with(Path("/tmp/test_project"))
        mock_git_init.assert_called_once_with(Path("/tmp/test_project"))
        mock_create_flask.assert_called_once_with(Path("/tmp/test_project"))
        mock_install_tailwind.assert_called_once_with(Path("/tmp/test_project"))


def test_init_command_fastapi_with_output_dir():
    with patch(
        "tailgen.cli._init_project_directory",
        return_value=Path("/tmp/test_project_fastapi"),
    ) as mock_init_dir, patch("tailgen.cli._create_venv") as mock_create_venv, patch(
        "tailgen.cli._create_git_ignore"
    ) as mock_create_git_ignore, patch(
        "tailgen.cli._create_readme"
    ) as mock_create_readme, patch(
        "tailgen.cli._git_init"
    ) as mock_git_init, patch(
        "tailgen.cli._create_fastapi_project"
    ) as mock_create_fastapi, patch(
        "tailgen.cli._install_and_configure_tailwindcss_fastapi"
    ) as mock_install_tailwind_fastapi, patch(
        "tailgen.cli.sleep", return_value=None
    ), patch(
        "builtins.input", lambda _: "new_project"
    ):
        # Test initialization with output directory and custom framework (FastAPI)
        result = runner.invoke(
            cli.app,
            [
                "init",
                "--framework",
                "fastapi",
                "--output-dir",
                "/tmp/test_project_fastapi",
            ],
        )
        assert result.exit_code == 0
        assert "Creating project directory" in result.stdout
        assert "new_project" in result.stdout  # Ensuring the mock project name is used
        mock_init_dir.assert_called_once_with(
            Path("/tmp/test_project_fastapi"), "new_project"
        )
        mock_create_venv.assert_called_once_with(Path("/tmp/test_project_fastapi"))
        mock_create_git_ignore.assert_called_once_with(
            Path("/tmp/test_project_fastapi")
        )
        mock_create_readme.assert_called_once_with(Path("/tmp/test_project_fastapi"))
        mock_git_init.assert_called_once_with(Path("/tmp/test_project_fastapi"))
        mock_create_fastapi.assert_called_once_with(Path("/tmp/test_project_fastapi"))
        mock_install_tailwind_fastapi.assert_called_once_with(
            Path("/tmp/test_project_fastapi")
        )
