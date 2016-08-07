from lispy2 import Env, Sym, global_env


class Player:
    def __init__(self, world, input, output):
        self.output = output
        self.input = input
        self.room_id = 1
        self.world = world  # type: 'World'
        self.name = 'no-name'
        self.env = Env(
            (Sym('player-name'),
             Sym('say'),
             ),
            (self.name,
             self.print,
             ),
            outer=global_env
            )

    def set_room(self, room_id: int):
        self.room_id = room_id

    def print(self, fmt, *args, **kwargs):
        if not isinstance(fmt, str):
            print('{}'.format(fmt))
        else:
            print(fmt.format(*args, **kwargs), file=self.output, **kwargs)
