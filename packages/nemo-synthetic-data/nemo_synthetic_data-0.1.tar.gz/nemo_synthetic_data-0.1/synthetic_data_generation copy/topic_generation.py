import argparse
from typing import List
from tqdm import tqdm
import sys

def generate_subtopics(client, n_subtopics: int, language: str, domain: str, model: str, temperature: float = 0.2) -> List[str]:
    prompt_template = """\
I want to create a synthetic dataset for {language} language conversational interactions in the domain of {domain}. Based on this context, give me {n_subtopics} subtopics
to cover various common topics and themes that should be included in {language} conversations.

The list must be without numbers, and without any description of the subtopics. The subtopics should be separated by a comma. There must be no other text than the list.
"""
    prompt = prompt_template.format(n_subtopics=n_subtopics, language=language, domain=domain)
    try:
        subtopics = []
        for _ in tqdm(range(n_subtopics), desc="Generating subtopics", unit="subtopic"):
            response = client.chat_completion(
                model=model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                top_p=0.7,
            )
            subtopics.extend([topic.strip() for topic in response['choices'][0]['message']['content'].split(",")])
        return subtopics[:n_subtopics]  # Ensure we return exactly n_subtopics
    except Exception as e:
        print(f"Error generating subtopics: {e}")
        return []

def main():
    # Set UTF-8 encoding for input/output
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

    parser = argparse.ArgumentParser(description="Generate conversation subtopics")
    parser.add_argument("--n_subtopics", type=int, default=5, help="Number of subtopics to generate")
    parser.add_argument("--language", type=str, default="Hindi", help="Language for conversation topics")
    parser.add_argument("--domain", type=str, default="general", help="Domain for conversation topics")
    parser.add_argument("--model", type=str, default="gpt-3.5-turbo", help="Model to use for generating subtopics")
    parser.add_argument("--temperature", type=float, default=0.7, help="Temperature for generation")
    parser.add_argument("--base_url", type=str, default="https://api.openai.com/v1", help="Base URL for the API")
    parser.add_argument("--api_key", type=str, required=True, help="API key for authentication")
    args = parser.parse_args()

    from synthetic_data_generation.config import get_client
    client, _ = get_client(args.base_url, args.api_key, args.model)

    subtopics = generate_subtopics(
        client, 
        args.n_subtopics, 
        args.language, 
        args.domain, 
        args.model, 
        temperature=args.temperature, 
    )
    print(f"Generated {len(subtopics)} subtopics for {args.language} conversations in {args.domain} domain:")
    for topic in subtopics:
        print(f"- {topic}")

if __name__ == "__main__":
    main()