from openai import OpenAI
import os
import subprocess

def get_openai_api_key():
    try:
        # Use pass to get the API key
        return subprocess.check_output(['pass', 'show', 'openai/apikey']).strip().decode('utf-8')
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback to environment variable if pass fails
        return os.environ.get("OPENAI_API_KEY")

# Learn more about calling the LLM: https://the-pocket.github.io/PocketFlow/utility_function/llm.html
def call_llm(prompt):
    api_key = get_openai_api_key()
    if not api_key:
        raise ValueError("OpenAI API key not found. Please set it using `pass` or the OPENAI_API_KEY environment variable.")

    client = OpenAI(api_key=api_key)
    r = client.chat.completions.create(
        model="gpt-5-mini-2025-08-07",
        messages=[{"role": "user", "content": prompt}]
    )
    return r.choices[0].message.content

if __name__ == "__main__":
    prompt = "What is the capital of france?"
    print(call_llm(prompt))