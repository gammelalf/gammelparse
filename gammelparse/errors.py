from .util import _get_action_name


class ArgumentError(Exception):
    """
    An error from creating or using an argument (optional or positional).

    The string value of this exception is the message, augmented with
    information about the argument that caused it.
    """

    def __init__(self, argument, message):
        self.argument_name = _get_action_name(argument)
        self.message = message

    def __str__(self):
        if self.argument_name is None:
            return f"{self.message}"
        else:
            return f"argument {self.argument_name}: {self.message}"


class ArgumentTypeError(Exception):
    """An error from trying to convert a command line string to a type."""
    pass
