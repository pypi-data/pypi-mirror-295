import os
import openai
from typing import Dict, List



class LLMIntegrator:
    def __init__(self, api_key):
        self.api_key = api_key
        if not self.api_key:
            raise ValueError("API key not found. Please enter your API Key.")
        openai.api_key = self.api_key

    def analyze_and_generate(self, files: Dict[str, str], readme_content: str) -> str:
        """
        Analyze the code and generate a technical article using the LLM.
        """
        prompt = self._create_prompt(files, readme_content)
        return self._generate_article(prompt)

    def _create_prompt(self, files: Dict[str, str], readme_content: str) -> str:
        """
        Create a prompt for the LLM based on the project files and README content.
        """
        prompt = f"""
        You are an AI assistant tasked with analyzing a software project and writing a comprehensive technical article about it.
        Use the following information to create your article:

        README content:
        {readme_content}

        Project files:
        """
        for file_path, content in files.items():
            prompt += f"\n\nFile: {file_path}\nContent:\n{content[:1000]}... (truncated)"

        prompt += """
        Based on this information, write a detailed technical article about the project. Include the following sections:
        1. Introduction
        2. Project Overview
        3. Key Features
        4. Architecture and Design
        5. Main Components
        6. Code Analysis
        7. Usage Examples
        8. Conclusion

        Ensure that your article is well-structured, informative, and provides insights into the project's purpose, implementation, and potential applications.
        """
        return prompt

    def _generate_article(self, prompt: str) -> str:
        """
        Generate the technical article using the Groq API.
        """
        try:
            completion = openai.chat.completions.create(
                model="gpt-4o-mini",  # Using Mixtral model with larger context
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates comprehensive and insightful technical articles."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=8000,
                n=1,
                stop=None,
                temperature=0.7,
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error in generating article: {e}")
            return "Failed to generate the article due to an error."