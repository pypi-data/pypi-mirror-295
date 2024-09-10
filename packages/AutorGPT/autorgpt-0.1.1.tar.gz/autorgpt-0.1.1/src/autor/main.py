import argparse
import os
from .file_parser import FileParser
from .readme_parser import ReadmeParser
from .llm_integrator import LLMIntegrator


def get_api_key():
    key_file = "key.txt"
    if os.path.exists(key_file):
        with open(key_file, "r") as f:
            return f.readline().strip()
    else:
        api_key = input("Please enter your API key: ")
        with open(key_file, "w") as f:
            f.write(api_key)
        return api_key

def main():
    parser = argparse.ArgumentParser(description="Generate a technical article from a project's README and codebase using LLM.")
    parser.add_argument("project_path", help="Path to the project directory")
    parser.add_argument("--output", default="technical_article.md", help="Output file name")
    args = parser.parse_args()

    if not os.path.isdir(args.project_path):
        print(f"Error: {args.project_path} is not a valid directory.")
        return

    # Get API key
    api_key = get_api_key()

    # Initialize components
    file_parser = FileParser(args.project_path)
    readme_parser = ReadmeParser(args.project_path)
    llm_integrator = LLMIntegrator(api_key)

    # Process the project
    files = file_parser.parse()
    readme_content = readme_parser.parse()

    # Generate the article
    article = llm_integrator.analyze_and_generate(files, readme_content)

    # Write the article to a file
    with open(args.output, 'w') as f:
        f.write(article)

    print(f"Technical article has been generated and saved to {args.output}")

if __name__ == "__main__":
    main()