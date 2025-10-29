from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import yaml

from fetch import fetch_excel
from transform import clean_headers, to_linear
from visuals import build_dashboard_html
from export import export_clean


CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.yaml"


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def main() -> int:
    try:
        config = load_config(CONFIG_PATH)

        source_cfg = config.get("source", {})
        files_cfg = config.get("files", {})
        data_cfg = config.get("data", {})

        local_path = fetch_excel(
            source_cfg.get("onedrive_direct_url"),
            files_cfg.get("local_raw_excel", "./suivi_raw.xlsx"),
        )
        print(f"Téléchargement terminé: {local_path}")

        sheet_name = data_cfg.get("sheet_name")
        df = pd.read_excel(local_path, sheet_name=sheet_name)
        df = clean_headers(df)
        df = df.rename(columns=lambda c: str(c).replace("#(lf)", " "))

        linear_df = to_linear(
            df,
            id_cols=data_cfg.get("id_columns", []),
            revision_prefixes=data_cfg.get("revision_prefixes", []),
            drop_blank_values=bool(data_cfg.get("drop_blank_values", True)),
        )

        build_dashboard_html(linear_df, files_cfg.get("dashboard_html", "dashboard.html"))
        print(f"Dashboard créé: {files_cfg.get('dashboard_html')}")

        export_clean(linear_df, files_cfg.get("clean_export_xlsx", "export_clean.xlsx"))
        print(f"Export Excel écrit: {files_cfg.get('clean_export_xlsx')}")

        output_dir = files_cfg.get("output_dir")
        if output_dir:
            Path(output_dir).expanduser().resolve().mkdir(parents=True, exist_ok=True)

        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"Erreur: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())