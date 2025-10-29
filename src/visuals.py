from __future__ import annotations

from pathlib import Path
from typing import Sequence

import pandas as pd
import plotly.express as px


_DASHBOARD_TITLE = "Suivi des Révisions"


def _format_kpi_block(df: pd.DataFrame) -> str:
    projet_count = df["Projet"].nunique() if "Projet" in df.columns else len(df)
    total_revisions = len(df)
    return (
        f"<div class='kpis'>"
        f"<div><span class='kpi-label'>Projets distincts</span><span class='kpi-value'>{projet_count}</span></div>"
        f"<div><span class='kpi-label'>Révisions totales</span><span class='kpi-value'>{total_revisions}</span></div>"
        f"</div>"
    )


def _make_plotly_div(fig) -> str:
    fig.update_layout(template="plotly_white", margin=dict(l=40, r=40, t=40, b=40))
    return fig.to_html(include_plotlyjs=False, full_html=False)


def _build_type_revision_chart(df: pd.DataFrame) -> str:
    if "TypeRevision" not in df.columns:
        return ""
    counts = df["TypeRevision"].value_counts().reset_index()
    counts.columns = ["TypeRevision", "Total"]
    fig = px.bar(counts, x="TypeRevision", y="Total", title="Révisions par type")
    return _make_plotly_div(fig)


def _build_project_chart(df: pd.DataFrame) -> str:
    if "Projet" not in df.columns:
        return ""
    counts = (
        df.groupby("Projet").size().reset_index(name="Total")
        .sort_values("Total", ascending=False)
        .head(15)
    )
    fig = px.bar(counts, x="Total", y="Projet", orientation="h", title="Top 15 projets par révisions")
    return _make_plotly_div(fig)


def _render_table(df: pd.DataFrame, columns: Sequence[str]) -> str:
    table_df = df[[col for col in columns if col in df.columns]].copy()
    if table_df.empty:
        return "<p>Aucune donnée à afficher.</p>"
    return table_df.to_html(classes="data-table", index=False, border=0)


def build_dashboard_html(df: pd.DataFrame, outfile: str) -> None:
    """Compose a minimal static HTML dashboard with Plotly visualisations."""
    path = Path(outfile).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)

    table_columns = [
        "Projet",
        "Code",
        "TypeRevision",
        "NumRevision",
        "Valeur",
        "Dernies Models",
        "Rev Mod",
        "A faire",
        "Priorité",
        "Commentaires",
    ]

    html_parts = [
        "<!DOCTYPE html>",
        "<html lang='fr'>",
        "<head>",
        "<meta charset='utf-8'>",
        f"<title>{_DASHBOARD_TITLE}</title>",
        "<script src='https://cdn.plot.ly/plotly-2.27.0.min.js'></script>",
        "<style>body{font-family:Arial,Helvetica,sans-serif;margin:2rem;}"
        ".kpis{display:flex;gap:2rem;margin-bottom:2rem;}"
        ".kpis div{background:#f4f6fb;padding:1rem 1.5rem;border-radius:8px;box-shadow:0 1px 2px rgba(0,0,0,0.1);}"
        ".kpi-label{display:block;font-size:0.9rem;color:#555;margin-bottom:0.5rem;}"
        ".kpi-value{font-size:1.6rem;font-weight:bold;color:#222;}"
        "h1{margin-bottom:1.5rem;}"
        ".charts{display:grid;gap:2rem;}"
        ".data-table{border-collapse:collapse;width:100%;margin-top:2rem;}"
        ".data-table th,.data-table td{border:1px solid #ddd;padding:0.5rem;text-align:left;}"
        ".data-table th{background:#fafafa;}",
        "</style>",
        "</head>",
        "<body>",
        f"<h1>{_DASHBOARD_TITLE}</h1>",
        _format_kpi_block(df),
        "<div class='charts'>",
        _build_type_revision_chart(df),
        _build_project_chart(df),
        "</div>",
        "<section>",
        "<h2>Table de données</h2>",
        _render_table(df, table_columns),
        "</section>",
        "</body>",
        "</html>",
    ]

    path.write_text("\n".join(part for part in html_parts if part), encoding="utf-8")