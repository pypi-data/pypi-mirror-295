import time
from datetime import datetime, timezone

def get_current_time_ms() -> float:
    return time.time() * 1000

def get_iso_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()

