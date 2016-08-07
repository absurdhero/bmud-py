import unittest

import player
import mud
import commands

from world import World


class TestPlayer(player.Player):
    def __init__(self, world, input):
        self.output = []
        super().__init__(world, input, self.output)

    def print(self, fmt: str, *args, **kwargs):
        if not isinstance(fmt, str):
            captured = '{}'.format(fmt)
        else:
            captured = fmt.format(*args, **kwargs)
        self.output.append(captured)
        # print(captured)  # helpful for debugging failing tests


def run_commands(*command_list, world=None) -> list:
    if not world:
        world = World()

    test_player = TestPlayer(world, commands)

    mud.initialize_commands()

    for line in command_list:
        cmd = line.strip()
        context = commands.CommandContext(test_player)
        commands.handle(context, cmd)

    return test_player.output


class TestCommands(unittest.TestCase):
    def assertNoErrors(self, output):
        for line in output:
            if 'usage:' in line:
                self.fail("found unexpected usage message: " + line)

    def test_walk_into_wall(self):
        output = run_commands('walk east\n')
        self.assertIn('cannot walk that way', output)

    def test_walk_no_args(self):
        output = run_commands('walk\n')
        self.assertIn('usage: walk <direction>', output)

    def test_walk_into_room_shows_description(self):
        output = run_commands('room.add foo bar',
                              'room.add-exit 1 2 east',
                              'walk east')
        self.assertNoErrors(output)
        self.assertIn('\nfoo\n\nbar\n\nexits: ', output)

    def test_enter_room_event(self):
        output = run_commands('room.add foo bar',
                              'room.add-exit 1 2 east',
                              'room.add-event 2 enter-room (say "you entered!")',
                              'room.add-event 1 enter-room (say "you came back!")',
                              'walk east')
        self.assertNoErrors(output)
        self.assertIn('you entered!', output)
        self.assertNotIn('you came back!', output)

if __name__ == '__main__':
    unittest.main()
