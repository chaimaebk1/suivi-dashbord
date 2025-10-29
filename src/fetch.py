from __future__ import annotations

import os
from pathlib import Path

import requests


def fetch_excel(direct_url: str, dest: str) -> str:
    """Download Excel from OneDrive direct link to ``dest``. Create parent dirs, raise on HTTP errors."""
    if not direct_url:
        raise ValueError("direct_url must be provided")

    destination = Path(dest).expanduser().resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)

    response = requests.get(direct_url, timeout=60)
    response.raise_for_status()

    with open(destination, "wb") as fh:
        fh.write(response.content)

    return os.fspath(destination)