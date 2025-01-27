import json
import os
from pathlib import Path
from typing import Dict, Any

CONFIG_DIR = os.path.expanduser("~/.config/watermark-cli")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

DEFAULT_CONFIG = {
    "text": None,
    "size": 20,
    "color": "#FFFFFF7F",  # 50% transparent white in RRGGBBAA format
    "output": None,
    "folder": None,
    "postfix": "-wm"
}

def load_config() -> Dict[str, Any]:
    if not os.path.exists(CONFIG_FILE):
        os.makedirs(CONFIG_DIR, exist_ok=True)
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

    with open(CONFIG_FILE, 'r') as f:
        return {**DEFAULT_CONFIG, **json.load(f)}

def save_config(config: Dict[str, Any]) -> None:
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
