from __future__ import annotations

from fnmatch import fnmatch
from typing import Iterable

import pandas as pd


def _normalize_patterns(value: object) -> list[str]:
    if value is None or pd.isna(value):
        return []
    return [item.strip() for item in str(value).split(";") if item.strip()]


def _matches_any(value: object, patterns: Iterable[str]) -> bool:
    patterns = list(patterns)
    if not patterns:
        return True
    text = "" if pd.isna(value) else str(value)
    return any(fnmatch(text, pattern) for pattern in patterns)


def _rule_match(row: pd.Series, rule: pd.Series) -> bool:
    return (
        _matches_any(row.get("Здание"), _normalize_patterns(rule.get("Здания")))
        and _matches_any(row.get("Система"), _normalize_patterns(rule.get("Системы")))
        and _matches_any(row.get("Отметка"), _normalize_patterns(rule.get("Отметки")))
    )


def _trigger_enabled(matrix: pd.DataFrame, trigger: str, discipline: str) -> bool:
    filtered = matrix.loc[matrix.iloc[:, 0].astype(str) == str(trigger)]
    if filtered.empty or discipline not in matrix.columns:
        return False
    value = filtered.iloc[0][discipline]
    return str(value).strip() in {"1", "1.0", "True", "TRUE", "да", "ДА"}


def apply_rules(
    packs: pd.DataFrame,
    matrix: pd.DataFrame,
    rules: pd.DataFrame,
    trigger: str,
    discipline: str,
) -> pd.DataFrame:
    if not _trigger_enabled(matrix, trigger, discipline):
        return pd.DataFrame(columns=list(packs.columns) + ["Причина_попадания"])

    base = packs.loc[packs["Спец"].astype(str) == str(discipline)].copy()
    if base.empty:
        return pd.DataFrame(columns=list(packs.columns) + ["Причина_попадания"])

    filtered_rules = rules.loc[
        (rules["Триггер"].astype(str) == str(trigger)) & (rules["Спец"].astype(str) == str(discipline))
    ].copy()
    mode_series = filtered_rules["Режим(INCLUDE/EXCLUDE)"].fillna("").astype(str).str.upper()

    include_rules = filtered_rules.loc[mode_series == "INCLUDE"]
    exclude_rules = filtered_rules.loc[mode_series == "EXCLUDE"]

    selected = pd.DataFrame(columns=base.columns)
    reasons: dict[object, str] = {}

    if include_rules.empty:
        selected = base.copy()
        for _, row in selected.iterrows():
            reasons[row.get("DocID", row.name)] = "Базовый отбор по специальности"
    else:
        for _, rule in include_rules.iterrows():
            matched = base.loc[base.apply(lambda row: _rule_match(row, rule), axis=1)]
            for _, row in matched.iterrows():
                key = row.get("DocID", row.name)
                reasons[key] = f"INCLUDE:{rule.get('RuleID', 'n/a')}"
            selected = pd.concat([selected, matched], ignore_index=True)

    if selected.empty:
        selected = pd.DataFrame(columns=base.columns)
    else:
        selected = selected.drop_duplicates(subset=["DocID"], keep="first")

    for _, rule in exclude_rules.iterrows():
        mask = selected.apply(lambda row: _rule_match(row, rule), axis=1) if not selected.empty else []
        matched_ids = set(selected.loc[mask, "DocID"].tolist()) if len(mask) else set()
        if matched_ids:
            selected = selected.loc[~selected["DocID"].isin(matched_ids)]
            for doc_id in matched_ids:
                reasons[doc_id] = f"EXCLUDE:{rule.get('RuleID', 'n/a')}"

    result = selected.copy()
    result["Причина_попадания"] = result["DocID"].map(reasons).fillna("Базовый отбор")
    return result
