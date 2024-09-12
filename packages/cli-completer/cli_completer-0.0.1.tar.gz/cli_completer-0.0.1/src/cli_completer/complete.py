from dataclasses import dataclass
from enum import Enum
from .core import Cmd, EnumArg, Arg
from .core import exception as e


# define some states of a state machine
class State(Enum):
    PARSE_CMD = 0
    PARSE_ARG = 1
    PARSE_VAL = 2
    END = 3


@dataclass
class ParserCtx:
    cmd: Cmd  # the current command
    arg: Arg | None = None  # the current argument
    state = State.PARSE_CMD  # the current state


def parse_cmd(lines: list[str], parser_ctx: ParserCtx):
    if len(lines) == 0:
        if not parser_ctx.cmd.pos_args:
            parser_ctx.state = State.END
            return
        # if the command has positional arguments, parse the positional arguments
        parser_ctx.state = State.PARSE_ARG
        return

    # check if the first line is a sub-command of the current command
    matched_sub_cmd = next(
        (sub_cmd for sub_cmd in parser_ctx.cmd.sub_cmds if sub_cmd == lines[0]), None
    )

    # if the first line is a sub-command
    if matched_sub_cmd:
        lines.pop(0)
        matched_sub_cmd.parsed_args.clear()
        matched_sub_cmd._inherited_args.clear()

        for arg in parser_ctx.cmd.args:
            if arg.pass_to_sub:
                matched_sub_cmd._inherited_args.append(arg)

        parser_ctx.cmd = matched_sub_cmd

        # PARSE_CMD does not need to parse arguments
        if matched_sub_cmd.sub_cmds:
            # if the sub-command has sub-commands, continue to parse the sub-command
            parser_ctx.state = State.PARSE_CMD
            return

    # if the first line is not a sub-command, try to parse the arguments
    # current cmd does not change, next state is PARSE_ARG
    parser_ctx.state = State.PARSE_ARG
    # pass the inherited arguments
    return


def parse_arg(lines: list[str], parse_state: ParserCtx):
    # try to parse the positional arguments first
    pos_args = parse_state.cmd.pos_args

    if pos_args:
        # positional arguments do not have a name
        # next state is PARSE_VALUE
        parse_state.state = State.PARSE_VAL
        pos_args[0].parsed_values.clear()

        # clear the parsed values
        parse_state.arg = pos_args[0]

        if pos_args[0] not in parse_state.cmd.parsed_args:
            parse_state.cmd.parsed_args.append(pos_args[0])

        return

    # if no positional arguments, try to parse the non-positional arguments
    if len(lines) == 0:
        # if no lines to parse, return END state
        parse_state.state = State.END
        return

    # try to parse the non-positional arguments
    np_args = parse_state.cmd.np_args

    next_line = lines.pop(0)

    np_args = list(
        filter(lambda arg: arg.is_visible(parse_state.cmd, next_line), np_args)
    )
    if not np_args:
        raise e.ArgExhaustedError(f"No more arguments to parse at '{next_line}'")

    match_arg = next((arg for arg in np_args if arg == next_line), None)
    if match_arg is None:
        raise e.ArgInvalidError(
            f"No argument matched for '{next_line}'"
        )  # argument not found

    # if the argument is found
    if match_arg not in parse_state.cmd.parsed_args:
        parse_state.cmd.parsed_args.append(match_arg)

    if match_arg.max_values == 0:
        # if the n_values is 0, this argument is done
        parse_state.state = State.PARSE_ARG
        return

    # if the n_values is not 0, next state is PARSE_VALUE
    # update the current argument
    # initialize the parsed values and the remaining number of values
    match_arg.parsed_values.clear()
    parse_state.arg = match_arg
    parse_state.state = State.PARSE_VAL


def parse_val(lines: list[str], parse_state: ParserCtx, f_line: str):
    assert parse_state.arg is not None, "The argument must not be None"

    num_value_given = len(parse_state.arg.parsed_values)
    is_value_sufficient = num_value_given >= parse_state.arg.min_values

    if len(lines) == 0:  # no lines to parse
        # f_line is a stop string
        if f_line.startswith("-"):
            if not is_value_sufficient:
                raise e.ValueInsufficientError(
                    f"Insufficient values for argument {parse_state.arg.name}, "
                    + f"expected {parse_state.arg.min_values} values, got {num_value_given}"
                )

            parse_state.arg.verify()
            parse_state.state = State.END
            parse_state.arg = None
            return

        # finish this argument
        parse_state.state = State.END
        return

    # parse lines[0] as a value
    next_line = lines[0]

    if isinstance(parse_state.arg, EnumArg):
        parse_state.arg.enum_callback(next_line)

    # check if it is a stop_str
    stop_here = next_line.startswith("-")

    if stop_here:
        if not is_value_sufficient:
            raise e.ValueInsufficientError(
                f"Insufficient values for argument {parse_state.arg.name}"
            )

        parse_state.arg.verify()
        # if the number of values is sufficient and verified, finish this argument
        parse_state.state = State.PARSE_ARG
        parse_state.arg = None
        return

    lines.pop(0)

    # add the value to the parsed values
    parse_state.arg.parsed_values.append(next_line)
    parse_state.arg.verify()

    if len(parse_state.arg.parsed_values) < parse_state.arg.max_values:
        parse_state.state = State.PARSE_VAL
        return

    parse_state.state = State.PARSE_ARG
    parse_state.arg = None
    return


def search_cmd(lines: list[str], entry: Cmd) -> ParserCtx:
    f_line = lines[-1]  # final line
    lines = lines.copy()[:-1]

    entry.parsed_args.clear()
    entry._inherited_args.clear()
    # start state
    parser_ctx = ParserCtx(cmd=entry)

    while parser_ctx.state != State.END:
        match parser_ctx.state:
            case State.PARSE_CMD:
                parse_cmd(lines, parser_ctx)
            case State.PARSE_ARG:
                parse_arg(lines, parser_ctx)
            case State.PARSE_VAL:
                parse_val(lines, parser_ctx, f_line)
    return parser_ctx


def complete_option(
    cmd: Cmd, lines: list[str], ignore_parse_error: bool = False
) -> list[str]:
    try:
        parse_state = search_cmd(lines, cmd)
        f_line = lines[-1]

        options = []
        if parse_state.arg is None:
            if not parse_state.cmd.parsed_args:
                options.extend(
                    [
                        sub_cmd.name
                        for sub_cmd in parse_state.cmd.sub_cmds
                        if sub_cmd.name.startswith(f_line)
                        and f_line.startswith(sub_cmd.start_str)
                    ]
                )
            np_args = parse_state.cmd.np_args
            np_args = list(
                filter(lambda arg: arg.is_visible(parse_state.cmd, f_line), np_args)
            )
            np_args = list(filter(lambda arg: arg.name.startswith(f_line), np_args))
            options.extend([arg.name for arg in np_args])
            if len(options) == 0:
                raise e.ArgInvalidError(f"No argument matched for '{f_line}'")
            if len(options) == 1:
                options[0] += " "
            return options

        if len(parse_state.arg.parsed_values) >= parse_state.arg.min_values:
            np_args = parse_state.cmd.np_args
            np_args = list(
                filter(lambda arg: arg.is_visible(parse_state.cmd, f_line), np_args)
            )
            np_args = list(filter(lambda arg: arg.name.startswith(f_line), np_args))
            options.extend([arg.name for arg in np_args])

        if isinstance(parse_state.arg, EnumArg):
            _f_line = parse_state.arg.enum_callback(f_line)
            if _f_line is not None:
                f_line = _f_line
            choices = parse_state.arg.choices.copy()
            if not parse_state.arg.allow_repeat:
                choices = [c for c in choices if c not in parse_state.arg.parsed_values]
            for choice in choices:
                if choice.startswith(f_line):
                    options.append(choice)
            if len(options) == 0:
                raise e.ValueInvalidError(f"Invalid value '{f_line}' for argument {parse_state.arg.name}")
            if len(options) == 1 and parse_state.arg.append_space:
                options[0] += " "
        return options

    except e.ParseError as error:
        if ignore_parse_error:
            return []
        raise error
