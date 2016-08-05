import sys

from world import World
from player import Player

# state

current_world = None  # type: World
player = Player()


# commands


def walk(args):
    direction = args[0]
    room = current_world.get_room(player.room_id)
    try:
        next_room = room.get_exit(direction)
    except KeyError:
        print("cannot walk that way")
    else:
        player.set_room(next_room.id)
        print(next_room.describe())


def quit_cmd(_):
    sys.exit(0)


def add_room(args):
    global current_world
    (rid, name, desc) = args
    current_world.add_room(rid, name, desc)


def load_world(args):
    global current_world
    current_world = World(args[0])


def room_add(args):
    if len(args) != 2:
        print("usage: room.add <name> <description>")
        return
    room = current_world.add_room(*args)
    print(room)


def room_add_exit(args):
    if len(args) != 3:
        print("usage: room.add-exit <source-id> <dest-id> <direction>")
        return
    source = int(args[0])
    dest = int(args[1])
    current_world.add_exit(current_world.get_room(source), current_world.get_room(dest), args[2])
    print(current_world.get_room(source))


def world_list(_):
    print(current_world.rooms.values())


commands = {
    'walk': walk,
    'n': lambda _: walk(['north']),
    'e': lambda _: walk(['east']),
    's': lambda _: walk(['south']),
    'w': lambda _: walk(['west']),
    'quit': quit_cmd,

    # admin commands
    'room.add': room_add,
    'room.add-exit': room_add_exit,
    'world.ls': world_list,
    'world.save': lambda _: current_world.save()
}


def handle(cmd):
    if len(cmd) == 0:
        return

    verb = cmd.split()[0]
    args = cmd.split()[1:]

    try:
        command = commands[verb]
    except KeyError:
        print("unknown command")
        return

    command(args)


def prompt_loop():
    try:
        print("> ", end='', flush=True)
        for line in sys.stdin:
            cmd = line.strip()
            handle(cmd)
            print("> ", end='', flush=True)
    except EOFError:
        sys.exit(0)


def main():
    global current_world
    current_world = World("world.json")
    print(current_world.get_room(player.room_id).describe())
    prompt_loop()


main()
