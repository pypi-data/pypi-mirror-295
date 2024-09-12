"""Abstract classes for the CLI completer"""

import os
from typing import overload
from . import callback
from .exception import ConfigError


class Arg:
    def __init__(
        self,
        name: str,
        max_values: int = 1,
        min_values: int = 1,
        pass_to_sub: bool = False,
    ):
        if name == "":
            raise ConfigError("Arg name cannot be empty")
        if max_values < 0 or min_values < 0:
            raise ConfigError("max_values and min_values cannot be negative")
        if min_values > max_values:
            raise ConfigError("min_values cannot be greater than max_values")
        if not name.startswith("-") and max_values == 0:
            raise ConfigError("positional args cannot have max_values=0")
        self.name = name
        self.max_values = max_values
        self.min_values = min_values
        self.pass_to_sub = pass_to_sub
        self.parsed_values: list[str] = []

    def verify(self) -> None:
        pass

    def is_visible(self, cmd: "Cmd", f_line: str) -> bool:
        return True

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} {self.name}"

    @overload
    def __eq__(self, value: str) -> bool: ...
    @overload
    def __eq__(self, value: object) -> bool: ...

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Arg):
            return self is value
        elif isinstance(value, str):
            return self.name == value
        return False


class TypedArg(Arg):
    def __init__(
        self,
        name: str,
        max_values: int = 1,
        min_values: int = 1,
        pass_to_sub: bool = False,
        supported_types: list[type] = [],
    ):
        super().__init__(
            name=name,
            max_values=max_values,
            min_values=min_values,
            pass_to_sub=pass_to_sub,
        )
        if not supported_types:
            raise ConfigError("supported_types cannot be empty")
        for type_ in supported_types:
            if type_ not in [int, float]:
                raise ConfigError(f"Unsupported type: {type_}, only support int and float")
        self.supported_types = supported_types

    def verify(self) -> None:
        callback.typedarg_verify_callback_fn(self)


class EnumArg(Arg):
    def __init__(
        self,
        name: str,
        max_values: int = 1,
        min_values: int = 1,
        pass_to_sub: bool = False,
        choices: list[str] = [],
        allow_repeat: bool = False,
        append_space: bool = True,
    ):
        super().__init__(
            name=name,
            max_values=max_values,
            min_values=min_values,
            pass_to_sub=pass_to_sub,
        )
        self.choices = choices
        self.allow_repeat = allow_repeat
        self.append_space = append_space

    def verify(self) -> None:
        callback.enumarg_verify_callback_fn(self)

    def enum_callback(self, f_line) -> str|None:
        return f_line


class FileArg(EnumArg):
    def __init__(
        self,
        name: str,
        max_values: int = 1,
        min_values: int = 1,
        pass_to_sub: bool = False,
        allow_repeat: bool = False,
        supported_exts: list[str] = ["*"],
    ):
        super().__init__(
            name=name,
            max_values=max_values,
            min_values=min_values,
            pass_to_sub=pass_to_sub,
            choices=[],
            allow_repeat=allow_repeat,
            append_space=False,
        )
        self.supported_exts = supported_exts

    def verify(self) -> None:
        callback.filecomplete_verify_callback_fn(self)

    def enum_callback(self, f_line) -> str|None:
        if len(f_line) > 0 and f_line[-1] in ["\\", "/"]:
            f_line = f_line[:-1] + os.sep
        self.choices = callback.filecomplete_callback_fn(self, f_line)
        return f_line


class Cmd:
    def __init__(
        self,
        name: str,
        start_str: str = "",
        sub_cmds: list["Cmd"] = [],
        args: list[Arg] = [],
    ):
        if name == "":
            raise ConfigError("Cmd name cannot be empty")
        pos_args = list(filter(lambda arg: not arg.name.startswith("-"), args))
        if sub_cmds and pos_args:
            raise ConfigError("Command cannot have both positional args and sub_cmds")
        self.name = name
        self.start_str = start_str
        self.sub_cmds = sub_cmds
        self.args = args
        self.parsed_args: list[Arg] = []
        self._inherited_args: list[Arg] = []

    def __repr__(self) -> str:
        return "Command(%r)" % (self.name)

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Cmd):
            return self.name == value.name
        elif isinstance(value, str):
            return self.name == value
        return False

    @property
    def np_args(self):
        """Get the non-positional arguments"""
        np_args = self.args + self._inherited_args
        np_args = list(filter(lambda arg: arg.name.startswith("-"), np_args))
        np_args = list(filter(lambda arg: arg not in self.parsed_args, np_args))

        return np_args

    @property
    def pos_args(self):
        """Get the positional arguments"""
        pos_args = self.args + self._inherited_args
        pos_args = list(filter(lambda arg: not arg.name.startswith("-"), pos_args))
        pos_args = list(filter(lambda arg: arg not in self.parsed_args, pos_args))

        return pos_args
