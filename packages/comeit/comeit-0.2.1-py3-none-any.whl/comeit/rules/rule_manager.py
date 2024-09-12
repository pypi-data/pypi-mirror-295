from .rule import Rule, Severity


class RuleManager:
    def __init__(self, rules: dict[str, Rule]):
        self._rules = rules

    def apply_rules(self) -> dict[str, bool | None]:
        """Applies all the rules.

        Returns
            dict[str, bool | None]: Rule ID and success or None for ignored rules.

        """
        results: dict[str, bool | None] = {}

        for rule_id, rule in self._rules.items():
            if rule.severity == Severity.IGNORE:
                results[rule.id] = None
                continue

            result, error = rule.apply()
            rule.error_message = error

            # Warnings are considered PASS
            results[rule_id] = result

        return results
