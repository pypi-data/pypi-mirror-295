import logging
from pathlib import Path

from rich.console import Console
from rich.table import Table

from comeit import (
    Body,
    Footer,
    Header,
    Rule,
    RuleConfig,
    RuleCreator,
    RuleLoader,
    RuleManager,
)

logger = logging.getLogger("comeit")

CONVENTIONAL_TYPES = set(["feat", "fix"])
DEFAULT_TYPES = set(["build", "chore", "ci", "docs", "perf", "refactor", "revert", "style", "test"])
MAX_HEADER_LENGTH = 52  # Make this a config later
MAX_BODY_LENGTH = 70  # Make this a config later
MAX_FOOTER_LENGTH = 52  # Make this a config later


def init_rules(types: set[str], commit_msg: tuple[str, str, str]) -> dict[str, Rule]:
    # Init check classes
    header = Header(types=types, max_length=MAX_HEADER_LENGTH, commit_msg=commit_msg[0])  # FINISH
    body = Body()
    footer = Footer()

    # Load rules from yaml config
    rule_loader = RuleLoader(Path("rules.yml"))
    loaded_rules: list[RuleConfig] = rule_loader.load_rules()

    # Create rule objects
    rule_creator = RuleCreator(rule_configs=loaded_rules, header=header, body=body, footer=footer)
    rules: dict[str, Rule] = rule_creator.create_rules()

    return rules


def parse_commit_message(commit_message: str):
    lines = commit_message.strip().split("\n")
    header = lines[0] if lines else ""
    body = ""
    footer = ""

    if len(lines) > 1:
        remaining = "\n".join(lines[1:])
        parts = remaining.split("\n\n", 1)
        body = parts[0].strip() if len(parts) > 0 else ""
        footer = parts[1].strip() if len(parts) > 1 else ""

    return header, body, footer


def create_commit_types(extra_types: list[str] = None, custom_types: list[str] = None) -> set[str]:
    """Create commit types from default types and/or custom types or extra types.

    Args:
    ----
        extra_types (list[str]): Adds extra types to the default types.
        custom_types (list[str], optional): Create your own types. This will disgard the
            default types, however it keeps "feat" and "fix" as they are required.
            Specifying this overrides the `extra_types` if it was given. Defaults to
            None.

    """
    types = CONVENTIONAL_TYPES

    if extra_types and not custom_types:
        types |= set(extra_types) | DEFAULT_TYPES
    elif custom_types:
        types |= set(custom_types)
    else:
        types |= DEFAULT_TYPES

    logger.debug("Allowed commit types: %s", "|".join(types))
    return types


# Make a commit parser file
def commit_parser():
    """Parse out header, body and footer."""


def configure_logger():
    logging.basicConfig(level=logging.DEBUG)


def main():
    configure_logger()

    logger.info("Creating allowed commit types...")
    allowed_commit_types = create_commit_types()

    logger.info("Preparing commit message...")
    commit_msg = ("feat: this is a feature", "", "")

    logger.info("Initializing rules...")
    rules = init_rules(types=allowed_commit_types, commit_msg=commit_msg)

    logger.info("Listing rules...")
    for rule_id, rule in rules.items():
        logger.debug("%s", rule)

    logger.info("Applying rules to commit %s", commit_msg)
    rule_manager = RuleManager(rules)

    # Rule ID and successful/unsuccessful run returned
    results = rule_manager.apply_rules()

    # Display results
    console = Console()
    table = Table(title="Rules Summary")
    table.add_column("Rule", justify="center")
    table.add_column("Pass", justify="center")
    table.add_column("Severity", justify="center")
    table.add_column("Description", justify="left")
    for rule_id, result in results.items():
        rule = rules[rule_id]

        status = "✅" if result else ("❌" if result is not None else "👻")

        # Warnings are always pass
        if rule.severity.is_warning():
            status = "🚧"

        table.add_row(rule_id, status, rule.severity.emoji, rule.description)

        if result is False and rule.severity.is_error():
            table.add_row("", "", "", f"[bold red]{rule.error_message}[/bold red]")
        elif result is False and rule.severity.is_warning():
            table.add_row("", "", "", f"[bold yellow]{rule.error_message}[/bold yellow]")

    console.print(table)


if __name__ == "__main__":
    main()
