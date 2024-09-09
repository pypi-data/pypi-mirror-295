import argparse
import os
from nemo_synthetic_data.topic_generation import generate_subtopics
from tqdm import tqdm
import sys

def generate_instructions(client, model, sub_topic, n_instructions, language, temperature):
    prompt_template = """\
Objective: Create a dataset of natural language questions or instructions that someone might ask an AI model in {language}.
Given a topic, generate {n_instructions} concise and clear questions or requests that a person might ask an LLM. These should avoid technical jargon and be easy to understand.

Your response should be in a list format with {n_instructions} items.
**STRICT**:ONLY GENERATE {n_instructions} ITEMS IN THE LIST.
Topic: {sub_topic}
Output Format: The list should contain {n_instructions} questions or instructions, each separated by a newline character, with no additional text. Avoid numbering the items.
"""
    prompt = prompt_template.format(sub_topic=sub_topic, n_instructions=n_instructions, language=language)
    try:
        response = client.chat_completion(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            top_p=0.7,
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error generating instructions for '{sub_topic}': {e}")
        return ""

def instructions_generator(client, model, topic_list, n_instructions, language, temperature):
    instruction_list = []
    for topic in tqdm(topic_list, desc="Generating instructions", unit="topic"):
        instructions = generate_instructions(client, model, topic, n_instructions, language, temperature)
        instruction_list.append(instructions)

    instruction_list_formatted = []
    for instruction_set in tqdm(instruction_list, desc="Formatting instructions", unit="set"):
        instruction_list_formatted.extend([instruction.strip() for instruction in instruction_set.split("\n") if instruction])
    return instruction_list_formatted

def main():
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description="Generate conversation instructions")
    parser.add_argument("--model", type=str, default="gpt-4", help="OpenAI model to use")
    parser.add_argument("--n_instructions", type=int, default=10, help="Number of instructions per subtopic")
    parser.add_argument("--base_url", type=str, default="https://api.openai.com/v1", help="Base URL for the API")
    parser.add_argument("--api_key", type=str, default=os.environ.get("OPENAI_API_KEY"), required=False, help="API key for authentication")
    parser.add_argument("--language", type=str, default="English", help="Language for the dataset")
    parser.add_argument("--domain", type=str, default="conversation", help="Domain for the dataset")
    parser.add_argument("--n_topics", type=int, default=20, help="Number of topics to generate")
    parser.add_argument("--output_file", type=str, default="synthetic_dataset.jsonl", help="Output file name")
    parser.add_argument("--temperature", type=float, default=0.7, help="Temperature for generation")
    parser.add_argument("subtopics", nargs="*", help="List of subtopics")
    args = parser.parse_args()

    from nemo_synthetic_data.config import get_client
    client, _ = get_client(base_url=args.base_url, api_key=args.api_key, model=args.model)

    # If subtopics are not provided, generate them based on n_topics
    if not args.subtopics:
        args.subtopics = generate_subtopics(client, args.model, args.domain, args.n_topics)

    instructions = instructions_generator(client, args.model, args.subtopics, args.n_instructions, args.language, args.temperature)
    
    # Write instructions to the output file
    with open(args.output_file, 'w', encoding='utf-8') as f:
        for instruction in instructions:
            f.write(f"{instruction}\n")

    print(f"Instructions have been written to {args.output_file}")

if __name__ == "__main__":
    main()