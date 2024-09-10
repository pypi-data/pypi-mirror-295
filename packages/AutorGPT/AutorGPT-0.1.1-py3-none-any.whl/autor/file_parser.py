import os

class FileParser:
    def __init__(self, project_path):
        self.project_path = project_path
        self.allowed_extensions = ['.py', '.md', '.txt', '.json', '.yml', '.yaml']

    def parse(self):
        """
        Traverse the project directory and parse relevant files.
        Returns a dictionary with file paths as keys and their content as values.
        """
        files = {}
        for root, _, filenames in os.walk(self.project_path):
            for filename in filenames:
                if self._is_relevant_file(filename):
                    file_path = os.path.join(root, filename)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    files[file_path] = content
        return files

    def _is_relevant_file(self, filename):
        """
        Check if the file is relevant for analysis based on its extension.
        """
        return any(filename.endswith(ext) for ext in self.allowed_extensions)
