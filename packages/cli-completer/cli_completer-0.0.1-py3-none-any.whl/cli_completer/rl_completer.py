import os
import readline
import shlex
from .core import Cmd, ParseError
from .complete import complete_option


class RLCompleter:
    def __init__(self, cmd: Cmd, use_shlex=True, show_error=False):
        self.cmd = cmd
        self.use_shlex = use_shlex
        self.show_error = show_error
        self.choices: list[str] = []

    def complete(self, _, state):
        "Generic readline completion entry point."
        start_index = readline.get_begidx()
        end_index = readline.get_endidx()
        buffer = readline.get_line_buffer()
        buffer_line = buffer[0:end_index]
        if state == 0:
            if self.use_shlex:
                use_posix = os.name != "nt"
                lines = shlex.split(buffer_line, posix=use_posix)
            else:
                lines = buffer_line.split()
            if start_index == end_index:
                lines.append("")
            if len(lines) == 0:
                self.choices = []
            try:
                self.choices = complete_option(self.cmd, lines)
            except ParseError as e:
                if self.show_error:
                    print("\n" + str(e) + "\n")
                self.choices = []

        return self.choices[state]


def set_rlcomplete(cmd: Cmd, use_shlex: bool = False, show_error: bool = False):
    completer = RLCompleter(cmd, use_shlex=use_shlex, show_error=show_error)
    readline.set_completer_delims(" ")  # type: ignore
    readline.parse_and_bind("tab: complete")  # type: ignore
    readline.set_completer(completer.complete)  # type: ignore
