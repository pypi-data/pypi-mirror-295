import argparse
from pathlib import Path
from typing import List, Optional

from .generator import ProjectGenerator
from .parser import TemplateParser


def parse_arguments(args: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse command-line arguments.

    Args:
        args (Optional[List[str]]): Command-line arguments. Defaults to None.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    # TODO Flesh out parser details and update documentation
    #  assignees: thechainercygnus
    #  labels: enhancement, documentation

    # TODO Consider moving to click or something
    #  assignees: thechainercygnus
    #  labels: enhancement, research

    parser = argparse.ArgumentParser(
        prog="puffit",
        description="Generate a project scaffold based on a *.pft template in the current directory.",
    )
    parser.add_argument("template", type=str, help="Path to the *.pft template file")
    return parser.parse_args(args)


def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the Personal Finance Tool.

    Args:
        args (Optional[List[str]]): Command-line arguments. Defaults to None.

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    # parse user arguments
    parsed_args = parse_arguments(args)

    # Parse the template file
    template_parser = TemplateParser(parsed_args.template)

    # Generate the project scaffold
    project_generator = ProjectGenerator(template_parser.directory_structure)
    # TODO Implement option to pass base_path as cli arg or set as envvar
    #  assignees: thechainercygnus
    #  labels: enhancement
    base_path = Path.cwd()
    project_generator.create_scaffold(base_path)

    print(f"Project scaffold generated in {base_path}")

# TODO Save code coverage report in automation for later review
#  assignees: thechainercygnus
#  labels: enhancement, research
if __name__ == "__main__":
    main()
