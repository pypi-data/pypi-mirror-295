import argparse
from typing import List, Dict
from tqdm import tqdm
import sys
import os
def generate_response(client, model: str, instruction: str, language: str, temperature: float) -> str:
    prompt_template = """\
You are an AI assistant with knowledge about {language} language and culture. 
An user has given you the following instruction:

{instruction}

Please provide a coherent, natural-sounding response in {language}. The response should be appropriate for the given instruction and context.
"""
    prompt = prompt_template.format(instruction=instruction, language=language)
    
    try:
        response = client.chat_completion(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error generating response for '{instruction}': {e}")
        return ""

def generate_responses(client, instruction_list: List[str], language: str, model: str, temperature: float) -> List[Dict[str, str]]:
    instruction_response_pairs = []
    for instruction in tqdm(instruction_list, desc="Generating responses", unit="instruction"):
        response = generate_response(client, model, instruction, language, temperature)
        if response:
            instruction_response_pairs.append([{"role": "user","content": instruction},{"role": "assistant","content": response}])
    return instruction_response_pairs

def main():
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description="Generate responses for given instructions")
    parser.add_argument("--model", type=str, default="gpt-4", help="Model to use for generating responses")
    parser.add_argument("--language", type=str, default="English", help="Language for responses")
    parser.add_argument("--temperature", type=float, default=0.7, help="Temperature for generation")
    parser.add_argument("--base_url", type=str, default="https://api.openai.com/v1", help="Base URL for the API")
    parser.add_argument("--api_key", type=str,default=os.environ.get("OPENAI_API_KEY"), required=False, help="API key for authentication")
    parser.add_argument("instructions", nargs="+", help="List of instructions to generate responses for")
    args = parser.parse_args()

    from nemo_synthetic_data.config import get_client
    client, _ = get_client(args.base_url, args.api_key, args.model)

    instruction_response_pairs = generate_responses(client, args.instructions, args.language, args.model, args.temperature)
    
    for message in instruction_response_pairs:
        print(f"{message['role']}: {message['content']}")
        print()

if __name__ == "__main__":
    main()