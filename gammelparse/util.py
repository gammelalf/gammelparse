from .const import SUPPRESS


class _AttributeHolder(object):
    """
    Abstract base class that provides __repr__.

    The __repr__ method returns a string in the format::
    ```
    ClassName(
            pos1, pos2, ...,
            key1=value1, key2=value2, ...,
            **{'weird key 3': value3, 'weird key 4': value4}
        )
    ```
    (The spacing is just for illustration)

    The attributes are determined by the methods `_get_args` and ´_get_kwargs`.
    Their default implementations uses __slots__ or __dict__
    """

    def __repr__(self):
        # Sort the keyword arguments by whether their name is an identifier or not
        id_args = {}
        non_id_args = {}
        for name, value in self._get_kwargs():
            if name.isidentifier():
                id_args[name] = value
            else:
                non_id_args[name] = value

        arg_strings = []
        # Add the positional arguments
        arg_strings.extend(map(repr, self._get_args()))
        # Add the identifier arguments
        arg_strings.extend(map(lambda pair: f"{pair[0]}={repr(pair[1])}", id_args))
        # If any present, add non identifier arguments
        if non_id_args:
            arg_strings.append(f"**{repr(non_id_args)}")

        return f"{type(self).__name__}({', '.join(arg_strings)})"

    def _get_kwargs(self):
        if hasattr(self.__class__, "__slots__"):
            return sorted(((key, getattr(self, key)) for key in self.__slots__))
        else:
            return sorted(self.__dict__.items())

    def _get_args(self):
        return []


class Namespace(_AttributeHolder):
    """Simple object for storing attributes.

    Implements equality by attribute names and values, and provides a simple
    string representation.
    """

    def __init__(self, **kwargs):
        for name in kwargs:
            setattr(self, name, kwargs[name])

    def __eq__(self, other):
        if not isinstance(other, Namespace):
            return NotImplemented
        return vars(self) == vars(other)

    def __contains__(self, key):
        return key in self.__dict__


def _copy_items(items):
    """
    Copy a container in _AppendAction, _AppendConstAction or _ExtendAction

    # The copy module is used only in the 'append' and 'append_const'
    # actions, and it is needed only when the default value isn't a list.
    # Delay its import for speeding up the common case.

    :param items: a list or any similar container to be copied
    :type items: a list or any similar container
    :return: the copied parameter
    :rtype: same as parameter
    """
    if items is None:
        return []
    elif type(items) is list:
        return items.copy()
    else:
        import copy
        return copy.copy(items)


def _get_action_name(argument):
    if argument is None:
        return None
    elif argument.option_strings:
        return '/'.join(argument.option_strings)
    elif argument.metavar not in (None, SUPPRESS):
        return argument.metavar
    elif argument.dest not in (None, SUPPRESS):
        return argument.dest
    else:
        return None
