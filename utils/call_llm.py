import logging
from google.generativeai import GenerativeModel
import google.generativeai as genai
import asyncio
import time
from collections import deque
import threading

from .config import load_config
from .secrets import get_secret, get_secret_async

_request_timestamps = deque()
_lock = threading.Lock()

def _rate_limit_wait():
    config = load_config()
    try:
        rpm_limit = int(config.get('gemini_rpm_limit') or 0)
    except (ValueError, TypeError):
        rpm_limit = 0

    if not rpm_limit:
        return

    with _lock:
        now = time.monotonic()
        # Remove timestamps older than 60 seconds
        while _request_timestamps and now - _request_timestamps[0] >= 60:
            _request_timestamps.popleft()

        if len(_request_timestamps) >= rpm_limit:
            wait_time = (_request_timestamps[0] + 60) - now
            if wait_time > 0:
                logging.info(f"Rate limit reached. Waiting {wait_time:.2f} seconds...")
                time.sleep(wait_time)
        
        _request_timestamps.append(time.monotonic())

async def _rate_limit_wait_async():
    # Run the synchronous rate-limiting logic in a separate thread
    await asyncio.to_thread(_rate_limit_wait)

def get_gemini_api_key():
    return get_secret('GEMINI_API_KEY', 'gemini/apikey')

async def get_gemini_api_key_async():
    return await get_secret_async('GEMINI_API_KEY', 'gemini/apikey')

def call_llm(prompt):
    _rate_limit_wait()
    api_key = get_gemini_api_key()
    if not api_key:
        raise ValueError("Gemini API key not found. Please set it using `pass` or the GEMINI_API_KEY environment variable.")

    config = load_config()
    model_name = config.get('gemini_model', 'gemini-fast')

    genai.configure(api_key=api_key)
    model = GenerativeModel(model_name)
    r = model.generate_content(prompt)
    return r.text

async def call_llm_async(prompt, semaphore: asyncio.Semaphore = None):
    async def _call():
        await _rate_limit_wait_async()
        api_key = await get_gemini_api_key_async()
        if not api_key:
            raise ValueError("Gemini API key not found. Please set it using `pass` or the GEMINI_API_KEY environment variable.")

        config = load_config()
        model_name = config.get('gemini_model', 'gemini-fast')
        
        genai.configure(api_key=api_key)
        model = GenerativeModel(model_name)
        r = await model.generate_content_async(prompt)
        return r.text

    if semaphore:
        async with semaphore:
            return await _call()
    else:
        return await _call()

if __name__ == "__main__":
    prompt = "What is the capital of france?"
    print(call_llm(prompt))
