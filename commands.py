import inspect

from world import World
from player import Player

from typing import Dict, List


_commands = {}  # type: Dict[str, Command]


class CommandContext:
    def __init__(self, player: Player):
        self.player = player

    @property
    def world(self) -> World:
        return self.player.world


class Command:
    """ define a command available to players in the game """
    def __init__(self, name: str, aliases: List[str] = None, help_text=''):
        if aliases is None:
            aliases = []

        self.name = name
        self.aliases = aliases  # type: List[str]
        self.help_text = help_text
        self.context = None  # type: CommandContext

    def apply(self, context, arg_list: list):
        # inject dynamic context
        self.context = context

        try:
            self._cmd(*arg_list)
        except TypeError:
            self._print("usage: " + self._usage())
        finally:
            self.context = None

    def _cmd(self, *args):
        raise NotImplementedError("command not implemented")

    def _usage(self) -> str:
        """ return a single-line argument list for usage instructions. """
        argspec = inspect.getfullargspec(self._cmd)
        args = argspec[0][1:]  # extract all but the first 'self' arg

        usage = '' + self.name
        for arg in args:
            usage += " <{}>".format(arg)

        return usage

    @staticmethod
    def _print(fmt, *args, **kwargs):
        print(fmt.format(*args, **kwargs))


def register(cmd: Command):
    _commands[cmd.name] = cmd
    for alias in cmd.aliases:
        _commands[alias] = cmd


def handle(context: CommandContext, cmd_line: str):
    if len(cmd_line) == 0:
        return

    tokens = cmd_line.split()
    verb = tokens[0]
    args = tokens[1:]

    try:
        command = _commands[verb]
    except KeyError:
        print("unknown command")
        return

    command.apply(context, args)


class CommandFunction(Command):
    """ make a Command from a function or lambda """
    def __init__(self, name, func, aliases = None, help_text=''):
        super().__init__(name, aliases=aliases, help_text=help_text)
        self.func = func

    def _cmd(self, *args):
        self.func(*args)


class Help(Command):
    def __init__(self):
        super().__init__('help', aliases=['?', 'h'], help_text='print this help text')

    def _cmd(self, *args):
        if args:
            for arg in args:
                self._print_help(arg)
                self._print("usage: " + _commands[arg]._usage())
        else:
            for cmd in sorted(set(_commands.values()), key=lambda c: c.name):
                self._print_help(cmd.name)

    def _print_help(self, name):
        cmd = _commands[name]
        self._print("{:18} {}", ", ".join([cmd.name] + cmd.aliases), cmd.help_text)
