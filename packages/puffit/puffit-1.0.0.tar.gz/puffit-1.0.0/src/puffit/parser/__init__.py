import re


class TemplateParser:
    # TODO Add docstrings to TemplateParser class
    #  assignees: thechainercygnus
    #  labels: enhancement, documentation
    def __init__(self, template: str):
        if template.endswith(".pft"):
            template = self._read_template(template)
        self._original = self._clean_input(template)  # Clean the input data
        self._original_lines = [
            line for line in self._original.split("\n") if line.strip()
        ]
        self.line_symbol_matrix = self._generate_line_symbol_matrix()
        self.line_indent_matrix = self._generate_line_indent_matrix()
        self.indent_size = self._get_indent_size()
        self.max_indent_level = self._get_max_indent_level()
        self.minified_mapping = self._generate_minified_mapping()
        self.directory_structure = (
            self._build_directory_structure()
        )  # Build the directory structure

    def _clean_input(self, template: str) -> str:
        """Clean the input by removing non-alphanumeric characters and comments."""
        lines = template.splitlines()
        cleaned_lines = []

        for line in lines:
            # Remove comments that start with '#' or after '//'
            line = re.split(r"#|//", line)[0].rstrip()

            # Replace any non-alphanumeric or non-ASCII characters except spaces
            cleaned_line = re.sub(r"[^\w\s/.-]", " ", line)

            # Ensure the line doesn't end with excess spaces due to replacements
            cleaned_line = cleaned_line.rstrip()

            cleaned_lines.append(cleaned_line)

        return "\n".join(cleaned_lines)

    def _build_directory_structure(self):
        structure = {}
        current_path = []  # Tracks the current directory path

        for index, line in enumerate(self._original_lines):
            indent_level = len(self.line_indent_matrix[index]) // self.indent_size
            line_type = self._get_line_type(
                line
            )  # Use the static method to identify type
            line_name = line.strip()

            # Adjust current path to match the indent level
            current_path = current_path[:indent_level]

            if line_type == "D":
                # It's a directory, add to the current level
                current_directory = structure
                for part in current_path:
                    current_directory = current_directory[part]
                current_directory[line_name] = {}  # Create new directory entry
                current_path.append(line_name)  # Add directory to the path
            elif line_type == "F":
                # It's a file, add to the current directory
                current_directory = structure
                for part in current_path:
                    current_directory = current_directory[part]
                current_directory[line_name] = (
                    None  # Add file as None (no substructure)
                )

        return structure

    def _generate_line_symbol_matrix(self):
        line_symbol_matrix = []
        for line in self._original_lines:
            # Remove comments
            if "#" in line:
                line = line.split("#", 1)[0].rstrip()

            # Determine if it's a directory or file
            line_character = "D" if line.rstrip().endswith("/") else "F"

            # Generate symbols for each line
            line_symbols = [
                (
                    line_character
                    if char.isascii() and not char.isspace()
                    else "I" if char.isspace() or not char.isascii() else " "
                )
                for char in line
            ]
            line_symbol_matrix.append("".join(line_symbols))
        return tuple(line_symbol_matrix)

    def _generate_line_indent_matrix(self):
        return tuple(
            re.search("I+", line).group(0) if re.search("I+", line) else ""
            for line in self.line_symbol_matrix
        )

    def _generate_minified_mapping(self):
        return [self.collapse_string(line) for line in self.line_symbol_matrix]

    def _get_indent_size(self):
        indent_sizes = [len(i) for i in self.line_indent_matrix if i]
        if not indent_sizes:
            raise Exception("Indent Size Error: No indentation found")
        return min(indent_sizes)

    def _get_max_indent_level(self):
        return max(
            len(line) // self.indent_size for line in self.line_indent_matrix if line
        )

    @staticmethod
    def _read_template(template_path):
        with open(template_path, "r") as template_reader:
            return template_reader.read()

    @staticmethod
    def _get_line_type(line: str):
        """Determine if the line represents a directory or file."""
        stripped_line = line.rstrip()  # Remove trailing whitespace
        return "D" if stripped_line.endswith("/") else "F"

    @staticmethod
    def collapse_string(s):
        return "".join(c for i, c in enumerate(s) if i == 0 or c != s[i - 1])
