from __future__ import annotations

from pathlib import Path

import pandas as pd


def export_clean(df: pd.DataFrame, path: str) -> None:
    """Write the linear table to an .xlsx without index; create parent dirs."""
    destination = Path(path).expanduser().resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(destination, index=False)