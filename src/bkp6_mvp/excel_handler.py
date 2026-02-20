from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd

REQUIRED_SHEETS = ("Комплекты", "Матрица_триггеров", "Правила")


def read_input_excel(path: str | Path) -> Dict[str, pd.DataFrame]:
    """Read and validate input workbook for the rule engine."""
    workbook_path = Path(path)
    if not workbook_path.exists():
        raise FileNotFoundError(f"Excel file not found: {workbook_path}")

    xls = pd.ExcelFile(workbook_path)
    missing = [sheet for sheet in REQUIRED_SHEETS if sheet not in xls.sheet_names]
    if missing:
        raise ValueError(f"Workbook is missing required sheets: {', '.join(missing)}")

    data = {sheet: pd.read_excel(workbook_path, sheet_name=sheet) for sheet in REQUIRED_SHEETS}
    return data


def export_result(df: pd.DataFrame, output_path: str | Path) -> Path:
    """Export calculated selection to Excel."""
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(out, index=False)
    return out
