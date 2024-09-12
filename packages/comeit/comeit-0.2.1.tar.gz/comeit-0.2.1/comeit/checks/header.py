import logging

log = logging.getLogger(__name__)


class Header:
    def __init__(self, types: list, max_length: int, commit_msg: str) -> None:
        self._types = types
        self._max_len = max_length
        self._commit_msg = commit_msg

    # This might be waaay too complex. Rather run all the other ones.
    def check_header(self):
        """A full test for the header.

        Should this fail, run the other header tests to find the exact issue.
        """

    def length(self) -> tuple[bool, str]:
        """Header cannot be longer than configured.

        This is an independent rule that can run paralell to other rules.

        Error: Header is longer than <max_len>
        """
        log.debug(f"Running {self.length.__name__}()")

        success = False
        error_msg = f"Exceeded header length. {100}/{self._max_len}"

        if success:
            return True, ""
        else:
            return False, error_msg

    def has_type(self) -> tuple[bool, str]:
        """Tries to find a colon ':' in the header preceded by exactly one word.

        Error: No colon found
        """
        log.debug(f"Running {self.has_type.__name__}()")

        success = True
        error_msg = "No colon found. Cannot identify a type."

        if success:
            return True, ""
        else:
            return False, error_msg

    # Dependent on "has_type() to be True if this should run"
    def type_empty(self, types: set):
        """Cannot have a ':' with no [a-z] char preceding it.

        Error: Found colon but there was nothing before it meaning empty type.
        """

    # Dependent on "has_type() to be True to run"
    # Dependent on "type_empty() to be False to run"
    def type_in_type_set(self, types: set):
        """Must be a type in the type-set followed by colon ':' or '!:'.

        Optional: An optional exclamation mark '!' can be added.

        Error: Type is not matching any defined types.
        """

    # Dependent on "has_type() to be True if this should run"
    def type_case(self, types: set):
        """Must be a lower case type followed by ':'.

        Being a lower case [a-z] followed by ':' is enough to satisfy this check.

        Optional: An optional exclamation mark '!' can be added.

        Error: Wrong case on the type even if it was the correct word.
        """

    def has_scope(self) -> bool:
        """Found a scope meaning parentheses after colon.

        :(word) is a valid scope and :(word and much more) is not. However it is
            recognized as scope
        either way.

        Optional
        """

    # Dependent on "has_scope() to be True if this should be run"
    def scope_chars(self):
        """Scope has invalid characters.

        A scope MUST be one word with no newlines, spaces, tabs, underscores, hyphens
            etc. Strictly
        [a-z].

        Error: Scope contains invalid characters.
        """

    # Dependent on "_has_scope() to be True if this should be run"
    def scope_case(self):
        """Scope case is invalid.

        Scope MUST be lower case [a-z] only.

        Error: Scope is not lower case.
        """

    # Dependent on "_has_scope() to be True if this should be run"
    def scope_length(self):
        """Scope length MUST follow the defined max length.

        Error: Scope length exceeded <max scope length>
        """

    def has_summary(self):
        """The header needs a summary additional to a type.

        The summary can in principle be any character. A colon will be confusing.
            Should colon be
        allowed?

        Error: Header does not contain a summary.
        """

    def summary_length(self):
        """This doesn't make sense since the entire header is checked for length."""

    def summary_case(self):
        """Summary MUST be lower case.

        Error: Summary must be written in lower case.
        """
