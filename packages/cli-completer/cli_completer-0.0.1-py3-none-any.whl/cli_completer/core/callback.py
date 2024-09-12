import os
from typing import TYPE_CHECKING
from .exception import ValueInvalidError, FileNotFoundError

if TYPE_CHECKING:
    from .abc import FileArg, TypedArg, EnumArg


### Verify callback functions
def typedarg_verify_callback_fn(arg: "TypedArg"):
    supported_types = arg.supported_types
    assert supported_types, "supported_types cannot be empty"

    for type_ in supported_types:
        assert type_ in [int, float]

    def is_int(value: str) -> bool:
        try:
            int(value)
            return True
        except ValueError:
            return False

    def is_float(value: str) -> bool:
        try:
            float(value)
            return True
        except ValueError:
            return False

    for value in arg.parsed_values:
        if int in supported_types and is_int(value):
            continue
        if float in supported_types and is_float(value):
            continue
        raise ValueInvalidError(f"Invalid value type '{value}' for argument {arg.name}")


def enumarg_verify_callback_fn(arg: "EnumArg"):
    choices = arg.choices.copy()

    for value in arg.parsed_values:
        if value in choices:
            if not arg.allow_repeat:
                choices.remove(value)
        else:
            raise ValueInvalidError(f"Invalid value '{value}' for argument {arg.name}")


def filecomplete_verify_callback_fn(arg: "FileArg"):
    supported_exts = arg.supported_exts

    for value in arg.parsed_values:
        if not os.path.exists(value) :
            raise FileNotFoundError(f"File not found: {value}")
        if not check_ext(value, supported_exts):
            raise ValueInvalidError(f"Invalid file extension for argument {arg.name}")

    if not arg.allow_repeat:
        for value in arg.parsed_values:
            if arg.parsed_values.count(value) > 1:
                raise ValueInvalidError(f"Repeated value '{value}' for argument {arg.name}")


### Utility functions
def filecomplete_callback_fn(arg: "FileArg", line: str) -> list[str]:
    """Callback function for FileArg argument
    - arg: FileArg argument
    - line: current line
    """
    dir_name = os.path.dirname(line)
    base_name = os.path.basename(line)

    if dir_name == "":
        if base_name in [".", ".."]:
            dir_name = base_name
            base_name = ""
        else:
            dir_name = "."

    dirs = []
    files = []

    for item in os.listdir(dir_name):
        item_path = os.path.join(dir_name, item)
        if os.path.isdir(item_path):
            dirs.append(item_path + os.sep)
        else:
            files.append(item_path)

    if base_name == ".":
        dirs = [
            os.path.join(dir_name, ".") + os.sep,
            os.path.join(dir_name, "..") + os.sep,
        ] + dirs

    if base_name == "..":
        dirs = [os.path.join(dir_name, "..") + os.sep] + dirs

    dirs = list(filter(lambda x: x.startswith(line), dirs))
    files = list(filter(lambda x: x.startswith(line), files))
    files = list(filter(lambda x: check_ext(x, arg.supported_exts), files))

    choices = dirs + files

    if not arg.allow_repeat:
        for value in arg.parsed_values:
            if value in choices:
                choices.remove(value)

    if not choices:
        raise FileNotFoundError(f"No suitables file found in current directory: {dir_name}")

    if len(choices) == 1 and not os.path.isdir(choices[0]):
        choices[0] += " "
    return choices


def check_ext(file_name: str, support_ext: list[str]) -> bool:
    """check if the file has the supported extension
    - args:
        - file_name: file name
        - support_ext: list of supported extensions (e.g., [".txt", ".md"])
        [] for directories only, ["*"] for all files and directories
    - returns: bool, whether the file has the supported extension
    """
    if "*" in support_ext:
        # * indicates all files
        return os.path.isfile(file_name) or os.path.isdir(file_name)
    elif support_ext == []:
        # [] indicates directories
        if os.path.isdir(file_name):
            return True
    else:
        for ext in support_ext:
            if file_name.endswith(ext) and os.path.isfile(file_name):
                return True
    return False
