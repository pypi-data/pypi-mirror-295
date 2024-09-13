import os
from pathlib import Path


class ProjectGenerator:
    # TODO Add docstrings to ProjectGenerator class
    #  assignees: thechainercygnus
    #  labels: enhancement, documentation
    def __init__(self, directory_structure: dict):
        self.directory_structure = directory_structure

    def create_scaffold(self, base_path, structure=None):
        if structure is None:
            structure = self.directory_structure

        for name, content in structure.items():
            path = os.path.join(base_path, name)
            if isinstance(content, dict):
                Path(path).mkdir(parents=True, exist_ok=True)
                self.create_scaffold(path, content)
            else:
                Path(path).touch()
