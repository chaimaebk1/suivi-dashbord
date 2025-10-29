from __future__ import annotations

import re
from typing import Iterable

import pandas as pd

_POWER_QUERY_TOKEN_PATTERN = re.compile(r"#\(lf\)")
MULTISPACE_PATTERN = re.compile(r"\s{2,}")


def _normalize_header(name: str) -> str:
    cleaned = _POWER_QUERY_TOKEN_PATTERN.sub(" ", name)
    cleaned = cleaned.replace("\n", " ")
    cleaned = MULTISPACE_PATTERN.sub(" ", cleaned)
    return cleaned.strip()


def clean_headers(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column headers with newline and PowerQuery token cleanup."""
    renamed = {col: _normalize_header(str(col)) for col in df.columns}
    return df.rename(columns=renamed)


def _select_revision_columns(columns: Iterable[str], revision_prefixes: list[str]) -> list[str]:
    selected: list[str] = []
    for col in columns:
        for prefix in revision_prefixes:
            if col.startswith(prefix):
                selected.append(col)
                break
    return selected


def to_linear(
    df: pd.DataFrame,
    id_cols: list[str],
    revision_prefixes: list[str],
    drop_blank_values: bool = True,
) -> pd.DataFrame:
    """Transform wide revision columns into a linear table."""

    existing_id_cols = [col for col in id_cols if col in df.columns]
    revision_cols = _select_revision_columns(df.columns, revision_prefixes)

    if not revision_cols:
        raise ValueError("No revision columns found in DataFrame")

    melted = df[existing_id_cols + revision_cols].melt(
        id_vars=existing_id_cols,
        value_vars=revision_cols,
        var_name="Attribut",
        value_name="Valeur",
    )

    melted["TypeRevision"] = melted["Attribut"].str.extract(r"([A-Z]+)")
    melted["NumRevision"] = melted["Attribut"].str.extract(r"(\d+)")
    melted.loc[melted["NumRevision"].isna(), "NumRevision"] = None

    result = melted.drop(columns=["Attribut"])

    if drop_blank_values:
        result = result[result["Valeur"].notna()]
        if not result.empty:
            result = result[result["Valeur"].astype(str).str.strip() != ""]

    return result.reset_index(drop=True)