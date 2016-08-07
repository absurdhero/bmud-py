# bmud - python edition

After figuring out how to write a mud in Racket a few years ago
([bmud](http://github.com/absurdhero/bmud)),
I'm at it again with Python 3. This time I'm not trying to learn
a new language through writing a mud.
Instead, I'm seeing how quickly I can write something in a language
I have some experience with.

# Usage

Execute `mud.py` in a python3 interpreter.

Run the `help` command to see what commands are available.

# World Building

The world is made of connected rooms.
To start, there is only a single starting room in the world.

Build out your world using the `room.add` and `room.add-exit` commands.
Type `help room.add` to get more detailed help for the command.

Run `world.save` to write the rooms to disk in a file named `world.json`.

# Scripting

Add game logic by attaching scripts to rooms with the `room.add-event`
command. This command requires a room-id, event name, and a script.
room-id may be set to `here`.

Scripts are written in scheme and have access to symbols
in the room and player's environment. If a script
defines a new symbol, it is stored in the room's environment.


### Events

- enter-room (sets global `last-room`)

  Return `#f` to prevent the player from entering the room

- exit-room (sets global `next-room`)

  Return `#f` to prevent the player from leaving the room

- say-room (sets global `said`)

- say-world (sets global `said`)

Scripts may register other events and may trigger each other with
the `dispatch-event` function.

### Variables

 - `room` - The room the script was called from
 - `player-name` - The player's name

### Functions

- `say message` prints text to a player in the same room
- `dispatch-event name` - calls another event script and keeps the current global environment 


# Networking

This time, I'm starting development without any networking by supporting
a single player reading and writing from stdout and stdin.

Networking and color output will wait until there's something worth playing.
Since I implemented sufficient remote terminal support in bmud, I'm not too
concerned or interested in this aspect of this new mud yet.