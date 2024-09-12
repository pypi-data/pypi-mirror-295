from dataclasses import dataclass
from pathlib import Path

import yaml

from .rule import Component, Severity


@dataclass
class RuleConfig:
    id: str
    description: str
    check: str
    component: Component
    severity: Severity
    dependencies: list[str] | None

    def __post_init__(self):
        # Convert the string to the corresponding Severity enum
        try:
            self.severity = Severity(self.severity)
        except (KeyError, ValueError) as e:
            raise ValueError(
                f"Severity field in rules.yml has invalid value. {e}. "
                "Choose from {Severity.get_members()}"
            )

        try:
            self.component = Component(self.component)
        except (KeyError, ValueError) as e:
            raise ValueError(
                f"Component field in rules.yml has invalid value. {e}. "
                "Choose from {Component.get_members()}"
            )


class RuleLoader:
    def __init__(self, rules_yml: Path = Path("rules.yml")) -> None:
        self._rules_yml = rules_yml

    def load_rules(self) -> list[RuleConfig]:
        try:
            with self._rules_yml.open() as file:
                rules_data = yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: The file '{self._rules_yml}' was not found.")
        except yaml.YAMLError as e:
            raise yaml.YAMLError(
                f"Error: Failed to parse YAML file '{self._rules_yml}'. Details: {e}"
            )
        except OSError as e:
            raise OSError(f"An I/O error occurred while reading '{self._rules_yml}'. Details: {e}")
        except Exception as e:
            raise Exception(f"Error: An unexpected error occurred. Details: {e}")

        # config = {RuleConfig(**d) for d in rules_data}
        config = [RuleConfig(**d) for d in rules_data]
        return config
