import argparse
import sys
import json
from nemo_synthetic_data.topic_generation import generate_subtopics
from nemo_synthetic_data.instruction_generation import instructions_generator
from nemo_synthetic_data.response_generation import generate_responses
from nemo_synthetic_data.data_handling import save_jsonl
from nemo_synthetic_data.config import get_client
import os
def generate_synthetic_dataset(language, domain, n_topics, n_instructions, output_file, 
                               base_url, api_key, model, temperature):
    try:
        print(f"Generating synthetic dataset with parameters:\n"
              f"Language: {language}\nDomain: {domain}\n"
              f"Topics: {n_topics}\nInstructions per topic: {n_instructions}\n"
              f"Output file: {output_file}\nBase URL: {base_url}\n"
              f"Model: {model}\nTemperature: {temperature}\n")
        
        # Get client
        client, model = get_client(base_url, api_key, model)
        
        # Generate topics
        topic_list = generate_subtopics(client, n_topics, language, domain, model, 
                                        temperature=temperature)
        print("Generated topics:", topic_list)
        
        # Generate instructions
        instruction_list = instructions_generator(client, model, topic_list, n_instructions, language,
                                                  temperature=temperature)
        print(f"Generated {len(instruction_list)} instructions")
        
        # Generate responses
        instruction_response_pair_list = generate_responses(client, instruction_list, language, model,
                                                            temperature=temperature)
        print(f"Generated {len(instruction_response_pair_list)} instruction-response pairs")
        
        # Save the dataset
        save_jsonl(instruction_response_pair_list, output_file, encoding='utf-8')
        print(f"Dataset saved to {output_file}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
    
    parser = argparse.ArgumentParser(description="Generate a synthetic dataset for conversational contexts.")
    parser.add_argument("--language", type=str, default="English", help="Language for the dataset")
    parser.add_argument("--domain", type=str, default="conversation", help="Domain for the dataset")
    parser.add_argument("--n_topics", type=int, default=20, help="Number of topics to generate")
    parser.add_argument("--n_instructions", type=int, default=10, help="Number of instructions per topic")
    parser.add_argument("--output_file", type=str, default="synthetic_dataset.jsonl", help="Output file name")
    parser.add_argument("--base_url", type=str, default="https://api.openai.com/v1", help="Base URL for the API")
    parser.add_argument("--api_key", type=str,default=os.environ.get("OPENAI_API_KEY"), required=False, help="API key for authentication")
    parser.add_argument("--model", type=str, default="gpt-4", help="Model to use for generation")
    parser.add_argument("--temperature", type=float, default=0.7, help="Temperature for generation")
    
    args = parser.parse_args()
    
    generate_synthetic_dataset(
        language=args.language,
        domain=args.domain,
        n_topics=args.n_topics,
        n_instructions=args.n_instructions,
        output_file=args.output_file,
        base_url=args.base_url,
        api_key=args.api_key,
        model=args.model,
        temperature=args.temperature,
    )

if __name__ == "__main__":
    main()