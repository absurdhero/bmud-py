import sys

import commands

from world import World
from player import Player


class RoomAdd(commands.Command):
    def __init__(self):
        super().__init__('room.add', help_text='create a new room')

    def _cmd(self, name, description):
        room = self.context.world.add_room(name, description)
        self._print(room)


class RoomAddExit(commands.Command):
    def __init__(self):
        super().__init__('room.add-exit', help_text='connect two rooms')

    def _cmd(self, source_id, destination_id, direction):
        world = self.context.world

        self.context.world.add_exit(world.get_room(int(source_id)), world.get_room(int(destination_id)), direction)
        self._print(world.get_room(int(source_id)))


class WorldList(commands.Command):
    def __init__(self):
        super().__init__('world.ls')

    def _cmd(self):
        self._print(self.context.world.rooms.values())


class RoomFind(commands.Command):
    def __init__(self):
        super().__init__('room.find', help_text='search for a room that contains the given string')

    def _cmd(self, name: str):
        results = []
        for room in self.context.world.rooms.values():
            if name.lower() in room.name.lower():
                results.append(room)

        for room in results:
            self._print("{}: {}", room.id, room.name)


class Quit(commands.Command):
    def __init__(self):
        super().__init__('quit', help_text='exit the game')

    def _cmd(self):
        import sys
        sys.exit(0)


class Walk(commands.Command):
    def __init__(self, direction: str = None):
        """ If direction is not given, then it is expected as an argument to the command. """

        self.direction = direction

        if not direction:
            super().__init__('walk', help_text='move between rooms')
        else:
            super().__init__(direction, aliases=[direction[0]], help_text='move ' + direction)

    def _cmd(self, *args):
        try:
            direction = self.direction or args[0]
        except IndexError:
            raise TypeError("expected direction argument")

        room = self.context.world.get_room(self.context.player.room_id)
        try:
            next_room = room.get_exit(direction)
        except KeyError:
            self._print("cannot walk that way")
        else:
            self.context.player.set_room(next_room.id)
            self._print(next_room.describe())

    def _usage(self):
        if self.direction:
            return "walk"
        else:
            return "walk <direction>"


def initialize_commands():
    commands.register(Quit())
    commands.register(Walk())
    commands.register(Walk('north'))
    commands.register(Walk('east'))
    commands.register(Walk('south'))
    commands.register(Walk('west'))
    commands.register(RoomAdd())
    commands.register(RoomAddExit())
    commands.register(RoomFind())
    commands.register(WorldList())

    commands.register(commands.Help())


def prompt_loop(player: Player):
    try:
        player.print("> ", end='', flush=True)
        for line in player.input:
            cmd = line.strip()
            context = commands.CommandContext(player)
            commands.handle(context, cmd)
            player.print("> ", end='', flush=True)
    except EOFError:
        return


def main():
    world = World("world.json")
    player = Player(world, sys.stdin, sys.stdout)
    initialize_commands()
    player.print(world.get_room(player.room_id).describe())
    prompt_loop(player)

if __name__ == '__main__':
    main()
