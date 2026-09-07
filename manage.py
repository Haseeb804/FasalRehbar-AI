#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import subprocess
import sys
from pathlib import Path


def _ensure_venv() -> None:
    """If running outside the project's virtualenv, re-execute with the venv python."""
    base_dir = Path(__file__).resolve().parent
    if sys.platform == "win32":
        venv_python = base_dir / "venv" / "Scripts" / "python.exe"
    else:
        venv_python = base_dir / "venv" / "bin" / "python"

    if venv_python.exists():
        current_exe = Path(sys.executable).resolve()
        target_exe = venv_python.resolve()
        if current_exe != target_exe and os.environ.get("_PAKAGRI_VENV_SWITCHED") != "1":
            os.environ["_PAKAGRI_VENV_SWITCHED"] = "1"
            os.environ["VIRTUAL_ENV"] = str(base_dir / "venv")
            scripts_dir = str(venv_python.parent)
            os.environ["PATH"] = scripts_dir + os.pathsep + os.environ.get("PATH", "")
            try:
                sys.exit(subprocess.call([str(target_exe)] + sys.argv))
            except Exception:
                pass


def main() -> None:
    _ensure_venv()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:  # pragma: no cover - bootstrap helper
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH environment variable?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
