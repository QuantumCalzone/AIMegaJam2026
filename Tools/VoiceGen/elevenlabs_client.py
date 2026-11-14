"""Shared ElevenLabs SDK client for Take 37 tools.

The key is read from ELEVENLABS_API_KEY, loaded from the git-ignored .env.local in the repo root.
It is never printed or stored in code.
"""
from pathlib import Path

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

ENV_FILE = Path(__file__).resolve().parents[2] / ".env.local"


def get_client() -> ElevenLabs:
    load_dotenv(ENV_FILE)
    return ElevenLabs()
