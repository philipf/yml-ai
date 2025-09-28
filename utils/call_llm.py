from openai import OpenAI, AsyncOpenAI
import os
import subprocess
import asyncio

def get_openai_api_key():
    try:
        # Use pass to get the API key
        return subprocess.check_output(['pass', 'show', 'openai/apikey']).strip().decode('utf-8')
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback to environment variable if pass fails
        return os.environ.get("OPENAI_API_KEY")

async def get_openai_api_key_async():
    return await asyncio.to_thread(get_openai_api_key)

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

async def call_llm_async(prompt, semaphore: asyncio.Semaphore = None):
    async def _call():
        api_key = await get_openai_api_key_async()
        if not api_key:
            raise ValueError("OpenAI API key not found. Please set it using `pass` or the OPENAI_API_KEY environment variable.")

        client = AsyncOpenAI(api_key=api_key)
        r = await client.chat.completions.create(
            model="gpt-5-mini-2025-08-07",
            messages=[{"role": "user", "content": prompt}]
        )
        return r.choices[0].message.content

    if semaphore:
        async with semaphore:
            return await _call()
    else:
        return await _call()

if __name__ == "__main__":
    prompt = "What is the capital of france?"
    print(call_llm(prompt))