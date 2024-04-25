"""Top-level package for TailGen"""

# tailgen/__init__.py


__app_name__ = "tailgen"
__version__ = "0.1.0"


VALID_FRAMEWORKS = {"flask", "fastapi"}

INPUT_CSS = """@tailwind base;
@tailwind components;
@tailwind utilities"""
