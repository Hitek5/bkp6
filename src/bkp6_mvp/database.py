from __future__ import annotations

import sqlite3
from pathlib import Path


SCHEMA = """
CREATE TABLE IF NOT EXISTS templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trigger_code TEXT NOT NULL,
    discipline_code TEXT NOT NULL,
    building_patterns TEXT,
    system_patterns TEXT,
    elevation_patterns TEXT,
    mode TEXT NOT NULL,
    comment TEXT,
    author TEXT,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS rule_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    template_id INTEGER,
    run_at TEXT DEFAULT CURRENT_TIMESTAMP,
    user_name TEXT,
    source_file TEXT,
    matched_count INTEGER,
    result_file TEXT,
    FOREIGN KEY(template_id) REFERENCES templates(id)
);
"""


def connect(db_path: str | Path) -> sqlite3.Connection:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.executescript(SCHEMA)
    conn.commit()
    return conn


def save_history(
    conn: sqlite3.Connection,
    user_name: str,
    source_file: str,
    matched_count: int,
    result_file: str,
    template_id: int | None = None,
) -> None:
    conn.execute(
        """
        INSERT INTO rule_history(template_id, user_name, source_file, matched_count, result_file)
        VALUES (?, ?, ?, ?, ?)
        """,
        (template_id, user_name, source_file, matched_count, result_file),
    )
    conn.commit()
