from enum import Enum
from typing import Callable


class Severity(Enum):
    """Different levels of severity for rules.

    Attributes
    ----------
        ERROR (str): Indicates a critical issue that must be fixed.
        WARNING (str): Indicates a potential issue that should be reviewed.
        INFO (str): Provides informational messages or suggestions.
        IGNORE (str): Indicates issues that should be ignored or not reported.

    """

    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    IGNORE = "IGNORE"

    def is_error(self):
        return self == Severity.ERROR

    def is_warning(self):
        return self == Severity.WARNING

    def is_info(self):
        return self == Severity.INFO

    def is_ignore(self):
        return self == Severity.IGNORE

    @property
    def emoji(self):
        emojis = {"ERROR": " 🛑", "WARNING": "🟡", "INFO": " 🔵", "IGNORE": "⚫"}
        return emojis[self.value]

    @classmethod
    def get_members(cls) -> list[str]:
        """Return all the enum members as a list of strings.

        Returns
        -------
            list[str]: A list of names of all members in the `Severity` enum.

        """
        return [member.name for member in cls]


class Component(Enum):
    """Different components of a structure where rules can be applied.

    Attributes
    ----------
        HEADER (str): Represents the header component.
        BODY (str): Represents the body component.
        FOOTER (str): Represents the footer component.

    """

    HEADER = "HEADER"
    BODY = "BODY"
    FOOTER = "FOOTER"

    @classmethod
    def get_members(cls) -> list[str]:
        """Return all the enum members as a list of strings.

        Returns
        -------
            list[str]: A list of names of all members in the `Component` enum.

        """
        return [member.name for member in cls]


class Rule:
    """Represents a validation rule with associated metadata and logic.

    Attributes
    ----------
        id (str): A unique identifier for the rule.
        description (str): A brief description of what the rule checks.
        check (Callable): A function that contains the logic to execute the rule.
        component (Component): The component of the structure to which the rule applies.
        severity (Severity): The severity level of the rule. Defaults to
            `Severity.WARNING`.
        dependencies (list[str]): A list of other rules that this rule depends on.
            Defaults to an empty list.

    """

    def __init__(
        self,
        id: str,
        description: str,
        check: Callable,
        component: Component,
        severity: Severity = Severity.WARNING,
        dependencies: list[str] | None = None,
    ):
        """Args:
        ----
            id (str): A unique identifier for the rule.
            description (str): A brief description of what the rule checks.
            check (Callable): A function that contains the logic to execute the rule.
            component (Component): component of the structure to which the rule applies.
            severity (Severity): The severity level of the rule. Defaults to
                `Severity.WARNING`.
            dependencies (list[str], optional): A list of other rules that this rule
                depends on. Defaults to None.

        """
        self.id = id
        self.description = description
        self.check = check
        self.component = component
        self.severity = severity
        self.dependencies = dependencies if dependencies else []
        self.error_message: str = ""

    def apply(self, *args, **kwargs) -> tuple[bool, str]:
        """Executes the rule's check function with the provided arguments.

        Args:
        ----
            *args: Positional arguments to pass to the check function.
            **kwargs: Keyword arguments to pass to the check function.

        Returns:
        -------
            The result of the check function. Could be anything or nothing.

        """
        return self.check(*args, **kwargs)

    def __str__(self):
        """Returns a string representation of the Rule instance."""
        return (
            f"Rule(id='{self.id}', description='{self.description}', "
            f"check={self.check.__name__}(),"
            f" component='{self.component}', severity='{self.severity}', "
            f"dependencies={self.dependencies})"
        )

    def __eq__(self, other):
        """Checks if two Rule instances are equal by comparing their attributes."""
        if not isinstance(other, Rule):
            return False

        return (
            self.id == other.id
            and self.description == other.description
            and self.check == other.check
            and self.component == other.component
            and self.severity == other.severity
            and self.dependencies == other.dependencies
        )
