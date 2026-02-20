from __future__ import annotations

import argparse
import getpass
from pathlib import Path

from .database import connect, save_history
from .excel_handler import export_result, read_input_excel
from .rule_engine import apply_rules


def run_selection(input_file: Path, trigger: str, discipline: str, output_file: Path, db_file: Path) -> Path:
    data = read_input_excel(input_file)
    result = apply_rules(
        packs=data["Комплекты"],
        matrix=data["Матрица_триггеров"],
        rules=data["Правила"],
        trigger=trigger,
        discipline=discipline,
    )
    export_path = export_result(result, output_file)

    conn = connect(db_file)
    save_history(
        conn=conn,
        user_name=getpass.getuser(),
        source_file=str(input_file),
        matched_count=len(result),
        result_file=str(export_path),
    )
    conn.close()
    return export_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Trigger-based documentation selection MVP")
    parser.add_argument("--input", required=True, help="Path to input workbook")
    parser.add_argument("--trigger", required=True, help="Trigger code")
    parser.add_argument("--discipline", required=True, help="Discipline code")
    parser.add_argument("--output", default="output/result.xlsx", help="Output Excel file")
    parser.add_argument("--db", default="output/rules.db", help="SQLite DB path")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    output = run_selection(
        input_file=Path(args.input),
        trigger=args.trigger,
        discipline=args.discipline,
        output_file=Path(args.output),
        db_file=Path(args.db),
    )
    print(f"Done. Result saved to: {output}")


if __name__ == "__main__":
    main()
