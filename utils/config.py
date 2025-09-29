import yaml
import os
import threading

_config = None
_config_lock = threading.Lock()
_config_path = 'config.yml'

def load_config():
    """
    Loads the YAML configuration file, caching it in memory after the first read.
    This function is thread-safe.
    """
    global _config
    # First check avoids locking if config is already loaded
    if _config is not None:
        return _config

    with _config_lock:
        # Second check handles race condition where another thread loaded config
        # while the current thread was waiting for the lock.
        if _config is not None:
            return _config

        if os.path.exists(_config_path):
            with open(_config_path, 'r') as f:
                _config = yaml.safe_load(f)
        else:
            _config = {}
    return _config