from comeit import (
    Body,
    Component,
    Footer,
    Header,
    Rule,
    RuleConfig,
    RuleCreator,
    Severity,
)


def test_rule_creator():
    """Verifies that rules can indeed be created from a config."""
    rule_configs = [
        RuleConfig(
            id="01",
            description="Check header length",
            check="check_header",
            component="HEADER",
            severity=Severity.ERROR,
            dependencies=None,
        ),
        RuleConfig(
            id="02",
            description=
            "Tries to find a colon ':' in the header preceded by exactly one word",
            check="has_type",
            component="HEADER",
            severity=Severity.ERROR,
            dependencies=["01"],
        ),
    ]

    header = Header(types=["feat", "fix"], max_length=52, commit_msg="")
    body = Body()
    footer = Footer()

    expected_rules = {
        "01": Rule(
            id="01",
            description="Check header length",
            check=header.check_header,
            component=Component.HEADER,
            severity=Severity.ERROR,
            dependencies=None,
        ),
        "02": Rule(
            id="02",
            description=
            "Tries to find a colon ':' in the header preceded by exactly one word",
            check=header.has_type,
            component=Component.HEADER,
            severity=Severity.ERROR,
            dependencies=["01"],
        ),
    }

    rule_creator = RuleCreator(
        rule_configs=rule_configs, header=header, body=body, footer=footer
    )
    rules = rule_creator.create_rules()

    assert rules == expected_rules
