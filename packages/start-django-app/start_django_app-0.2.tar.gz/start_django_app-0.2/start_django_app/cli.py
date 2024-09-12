import argparse
from .start_django_app import start_django_app


def main():
    parser = argparse.ArgumentParser(
        description="Create a new Django project with a virtual environment."
    )
    parser.add_argument("project_name", help="The name of the Django project.")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output."
    )
    args = parser.parse_args()

    start_django_app(args.project_name, args.verbose)
