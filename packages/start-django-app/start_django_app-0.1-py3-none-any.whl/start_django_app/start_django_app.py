import os
import subprocess
import sys


def is_venv_active():
    """Check if the virtual environment is already active."""
    return hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )


def create_virtualenv():
    """Create a new virtual environment."""
    print("Creating virtual environment...")
    subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
    print("Virtual environment created successfully.")


def run_in_venv(command):
    """Run a command inside the virtual environment."""
    if os.name == "nt":
        venv_python = ".venv\\Scripts\\python.exe"
    else:
        venv_python = ".venv/bin/python"

    subprocess.run([venv_python] + command, check=True)


def install_django():
    """Install Django in the virtual environment."""
    try:
        run_in_venv(["-m", "pip", "show", "django"])
        print("Django is already installed.")
    except subprocess.CalledProcessError:
        print("Django is not installed. Installing Django...")
        run_in_venv(["-m", "pip", "install", "django"])
        print("Django installed successfully.")


def start_django_project(project_name):
    """Start a new Django project with the given name."""
    project_name_underscore = project_name.replace("-", "_")
    try:

        subprocess.run(["django-admin", "startproject", project_name_underscore, "."])

        print(f"Django project '{project_name_underscore}' created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to start Django project. {e}")
        sys.exit(1)


def start_django_app(project_name, verbose=False):
    """Main function to create the Django app."""

    try:
        os.mkdir(project_name)
    except FileExistsError:
        print(f"Error: Directory '{project_name}' already exists.")
        sys.exit(1)

    os.chdir(project_name)
    print(f"Project '{project_name}' directory created.")

    if not is_venv_active():
        create_virtualenv()
    else:
        print("Virtual environment is already active.")

    install_django()
    start_django_project(project_name)
    print("\nTo activate the virtual environment, run:")
    print(f"  cd {project_name}")
    if os.name == "nt":
        print("  .venv\\Scripts\\activate")
    else:
        print("  source .venv/bin/activate")
    print("To deactivate the virtual environment, run:")
    print("  deactivate")
