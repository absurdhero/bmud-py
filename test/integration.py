import unittest

import player
import mud
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


def run_commands(*commands, world=None) -> list:
    if not world:
        world = World("test.json")
    test_player = TestPlayer(world, commands)
    mud.initialize_commands()
    mud.prompt_loop(test_player)
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


if __name__ == '__main__':
    unittest.main()
