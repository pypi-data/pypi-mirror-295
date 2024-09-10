import os
import openai
import json
from typing import List, Dict

def prepare_training_data(articles_dir: str) -> List[Dict[str, str]]:
    """
    Prepare training data from the technical articles.
    """
    training_data = []
    for filename in os.listdir(articles_dir):
        if filename.endswith('.md'):
            with open(os.path.join(articles_dir, filename), 'r') as f:
                content = f.read()
            training_data.append({
                "prompt": "Write a technical article about a software project.",
                "completion": content
            })
    return training_data

def save_training_data(data: List[Dict[str, str]], output_file: str):
    """
    Save the training data in JSONL format.
    """
    with open(output_file, 'w') as f:
        for item in data:
            f.write(json.dumps(item) + '\n')

def finetune_model(training_file: str):
    """
    Fine-tune the GPT model using the prepared training data.
    """
    try:
        response = openai.File.create(
            file=open(training_file, "rb"),
            purpose='fine-tune'
        )
        file_id = response.id
        
        fine_tuning_job = openai.FineTuningJob.create(
            training_file=file_id, 
            model="gpt-3.5-turbo"
        )
        
        print(f"Fine-tuning job created. Job ID: {fine_tuning_job.id}")
        print("You can monitor the job status using the OpenAI API or dashboard.")
    except Exception as e:
        print(f"Error in fine-tuning: {e}")

def main():
    articles_dir = 'data/technical_articles'
    training_data_file = 'data/training_data.jsonl'

    # Prepare and save training data
    training_data = prepare_training_data(articles_dir)
    save_training_data(training_data, training_data_file)

    # Fine-tune the model
    finetune_model(training_data_file)

if __name__ == "__main__":
    main()
