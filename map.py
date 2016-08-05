import json

from typing import Dict

from room import Room


class Map:
    def __init__(self, file_path: str):
        self.next = 1
        self.file_path = file_path
        self.rooms = {}  # type: Dict[int, Room]

        self.map = {}

        try:
            with open(file_path) as f:
                self.map = json.load(f)
        except FileNotFoundError:
            self.map['rooms'] = []
            print("warning: '%s' not found. Loading empty map." % file_path)
            self.add_room("start", "In the beginning, there was only this room.")
            return

        for entry in self.map["rooms"]:
            self.rooms[entry["id"]] = Room(entry["id"], entry["name"], entry["desc"])
            self.next_id()

        for entry in self.map["rooms"]:
            room = self.get_room(entry["id"])
            for direction, rid in entry["exits"].items():
                room.add_exit(self.get_room(rid), direction)

    def get_room(self, rid: int) -> Room:
        return self.rooms[rid]

    def add_room(self, name: str, desc: str) -> Room:
        rid = self.next_id()
        room = Room(rid, name, desc)
        self.rooms[rid] = room
        return room

    def add_exit(self, source: Room, target: Room, direction: str):
        self.rooms[source.id].add_exit(target, direction)

    def save(self):
        room_maps = []
        for rid, room in self.rooms.items():
            room_maps.append({
                "id": rid,
                "name": room.name,
                "desc": room.description,
                "exits": room.exit_ids()
            })

        self.map["rooms"] = room_maps
        with open(self.file_path, "w") as f:
            json.dump(self.map, f, indent=2)

    def next_id(self) -> int:
        self.next += 1
        return self.next - 1
