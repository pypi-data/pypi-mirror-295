import os

class ReadmeParser:
    def __init__(self, project_path):
        self.project_path = project_path
        self.readme_path = os.path.join(project_path, 'README.md')

    def parse(self):
        """
        Parse the README.md file.
        Returns the content of the README file as a string.
        """
        if not os.path.exists(self.readme_path):
            return "README.md not found"

        with open(self.readme_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return content
