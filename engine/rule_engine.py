"""Applied Skill Rule audit primitives for FinSkillOS.

The structures in this module implement the AUTO-CONTRACT-001 requirement from
`FinSkillOS_skills/skills/05_vibecoding_automation.md`.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable


@dataclass(frozen=True)
class AppliedRule:
    """A single Skill Rule application record shown in dashboard audit logs."""

    rule_id: str
    step: str
    condition: str
    action: str
    result: str
    severity: str = "INFO"

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


class RuleAuditLog:
    """Collects applied Skill Rules across the analysis pipeline."""

    def __init__(self, rules: Iterable[AppliedRule] | None = None) -> None:
        self._rules: list[AppliedRule] = []
        if rules:
            self.extend(rules)

    def add(
        self,
        rule_id: str,
        step: str,
        condition: str,
        action: str,
        result: str,
        severity: str = "INFO",
    ) -> AppliedRule:
        rule = AppliedRule(
            rule_id=rule_id,
            step=step,
            condition=condition,
            action=action,
            result=result,
            severity=severity,
        )
        self._rules.append(rule)
        return rule

    def extend(self, rules: Iterable[AppliedRule | dict[str, str]]) -> None:
        for rule in rules:
            if isinstance(rule, AppliedRule):
                self._rules.append(rule)
            else:
                self._rules.append(AppliedRule(**rule))

    def to_records(self) -> list[dict[str, str]]:
        return [rule.to_dict() for rule in self._rules]

    def deduplicated_records(self) -> list[dict[str, str]]:
        seen: set[tuple[str, str, str]] = set()
        records: list[dict[str, str]] = []
        for rule in self._rules:
            key = (rule.rule_id, rule.step, rule.result)
            if key in seen:
                continue
            seen.add(key)
            records.append(rule.to_dict())
        return records

    def __len__(self) -> int:
        return len(self._rules)
