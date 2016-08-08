import textwrap
import lispy2

from typing import Dict


class Room:
    def __init__(self, room_id: int, name: str, description=''):
        self.id = room_id
        self.name = name
        self.description = description
        self.exits = {}  # type: Dict[str, Room]
        self.events = {}  # type: Dict[str, str]
        self.env = lispy2.Env(
            (lispy2.Sym('room'),),
            (self,),
            outer=lispy2.global_env)

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

    def add_event(self, event: str, script: str):
        self.events[event] = script

    def execute_event(self, event, context):
        if event not in self.events:
            return

        # build a new environment for this room and inherit from the player's environment
        env = lispy2.Env(outer=context.player.env, **self.env)

        return lispy2.eval(self.events[event], env)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "desc": self.description,
            "exits": self.exit_ids(),
            "events": self.events
        }
