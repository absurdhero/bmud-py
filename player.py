
class Player:
    def __init__(self, world):
        self.room_id = 1
        self.world = world  # type: 'World'

    def set_room(self, room_id: int):
        self.room_id = room_id
