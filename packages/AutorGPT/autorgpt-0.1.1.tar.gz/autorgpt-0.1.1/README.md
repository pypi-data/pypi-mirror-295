# Technical Article Generator

This project automatically generates technical articles from a project's README and codebase using Large Language Models (LLM).

## Features

- Parses project files and README
- Integrates with LLM to analyze code and generate articles
- Handles API key storage for LLM integration
- Outputs a markdown file with the generated technical article

## Prerequisites

- Python 3.7+
- Access to an LLM API (e.g., OpenAI's GPT-3)

## Usage

Run the script with the following command:

```
generate-article '/path/to/your/project'
```

- `/path/to/your/project`: The path to the project directory you want to analyze
- `--output`: (Optional) Specify the output file name (default: technical_article.md)

On the first run, you will be prompted to enter your API key. This key will be saved in a `key.txt` file for future use.

## Configuration

The project uses a `key.txt` file to store your API key. If this file doesn't exist, you'll be prompted to enter your key when you first run the script.

## Project Structure

- `main.py`: The main script that orchestrates the article generation process
- `file_parser.py`: Handles parsing of project files
- `readme_parser.py`: Parses the project's README file
- `llm_integrator.py`: Integrates with the LLM API for content generation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to [LLM Provider] for providing the API used in this project
- Inspired by the need for automated technical documentation