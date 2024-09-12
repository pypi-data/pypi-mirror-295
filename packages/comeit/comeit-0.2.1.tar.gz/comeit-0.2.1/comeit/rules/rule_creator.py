import logging

from ..checks.body import Body
from ..checks.footer import Footer
from ..checks.header import Header
from .rule import Component, Rule
from .rule_loader import RuleConfig

log = logging.getLogger(__name__)


class RuleCreator:
    """Creates the rules from the values in the rules config yaml file."""

    def __init__(
        self,
        rule_configs: list[RuleConfig],
        header: Header,
        body: Body,
        footer: Footer,
    ):
        self._rule_configs = rule_configs

        self._header = header
        self._body = body
        self._footer = footer

    def create_rules(self) -> dict[str, Rule]:
        return {config.id: self._create_rule(config) for config in self._rule_configs}

    def _create_rule(self, rule_config: RuleConfig) -> Rule:
        if rule_config.component == Component.HEADER:
            check_method = getattr(self._header, rule_config.check)
        elif rule_config.component == Component.BODY:
            check_method = getattr(self._body, rule_config.check)
        elif rule_config.component == Component.FOOTER:
            check_method = getattr(self._footer, rule_config.check)
        else:
            raise Exception("Unknown component. Can't create rule.")

        # Check if the method exists and call it
        if callable(check_method):
            log.debug(f"Found method {rule_config.check}. Creating rule {rule_config.id}...")
        else:
            raise Exception(f"Failed to create rule. Method '{rule_config.check}' not found.")

        return Rule(
            id=rule_config.id,
            description=rule_config.description,
            check=check_method,
            component=rule_config.component,
            severity=rule_config.severity,
            dependencies=rule_config.dependencies,
        )
