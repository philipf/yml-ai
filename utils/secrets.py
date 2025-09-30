import os
import subprocess
import asyncio

def get_secret(env_var_name, pass_path):
    """
    Retrieves a secret, first checking for an environment variable,
    then falling back to the 'pass' password manager.

    Args:
        env_var_name (str): The name of the environment variable.
        pass_path (str): The path to the secret in 'pass'.

    Returns:
        str: The secret, or None if not found.
    """
    secret = os.environ.get(env_var_name)
    if secret:
        return secret

    try:
        return subprocess.check_output(['pass', 'show', pass_path]).strip().decode('utf-8')
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

async def get_secret_async(env_var_name, pass_path):
    """
    Asynchronously retrieves a secret.
    """
    return await asyncio.to_thread(get_secret, env_var_name, pass_path)
