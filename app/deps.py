import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from slowapi import Limiter
from slowapi.util import get_remote_address

load_dotenv()

start_time = datetime.now(timezone.utc)

EXPECTED_TOKEN = os.getenv("SPECIESNET_API_KEY", "")
if not EXPECTED_TOKEN:
    raise RuntimeError("Environment variable SPECIESNET_API_KEY is not set")


TMP_DIR = "/tmp/species_uploads"
os.makedirs(TMP_DIR, exist_ok=True)

limiter = Limiter(key_func=get_remote_address)
