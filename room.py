import textwrap

from typing import Dict


class Room:
    def __init__(self, room_id: int, name: str, description=''):
        self.id = room_id
        self.name = name
        self.description = description
        self.exits = {}  # type: Dict[str, Room]

    def describe(self):
        return "\n" + self.name + "\n\n" + textwrap.fill(self.description) + "\n\n" + \
               "exits: " + ", ".join(list(self.exits.keys()))

    def add_exit(self, target: 'Room', direction: str):
        self.exits[direction] = target

    def get_exit(self, direction: str) -> 'Room':
        return self.exits[direction]

    def exit_ids(self):
        return {d: r.id for (d, r) in self.exits.items()}

    def __repr__(self):
        return "Room(%s, %s, %s)" % (self.id, self.name, self.exit_ids())
