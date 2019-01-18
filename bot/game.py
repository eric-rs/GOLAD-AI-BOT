from sys import stdin, stdout, stderr
import traceback
import time

from bot.player import Player
from field.field import Field


class Game:
    def __init__(self):
        self.time_per_move = -1
        self.timebank = -1
        self.last_update = None
        self.max_rounds = -1

        self.round = 0
        self.player_names = []
        self.players = {}
        self.me = None
        self.opponent = None
        self.field = Field()

    def update(self, data):
        # start timer
        self.last_update = time.time()
        for line in data.split('\n'):

            line = line.strip()
            if len(line) <= 0:
                continue

            tokens = line.split()
            if tokens[0] == "settings":
                self.parse_settings(tokens[1], tokens[2])
            elif tokens[0] == "update":
                if tokens[1] == "game":
                    self.parse_game_updates(tokens[2], tokens[3])
                else:
                    self.parse_player_updates(tokens[1], tokens[2], tokens[3])
            elif tokens[0] == "action":
                self.timebank = int(tokens[2])
                # Launching bot logic happens after setup finishes

    def parse_settings(self, key, value):
        if key == "timebank":
            self.timebank = int(value)
        elif key == "time_per_move":
            self.time_per_move = int(value)
        elif key == "player_names":
            self.player_names = value.split(',')
            self.players = {name: Player(name) for name in self.player_names}
        elif key == "your_bot":
            self.me = self.players[value]
            self.opponent = self.players[[name for name in self.player_names if name != value][0]]
        elif key == "your_botid":
            self.me.id = value
            self.opponent.id = str(2 - (int(value) + 1))
        elif key == "field_width":
            self.field.width = int(value)
        elif key == "field_height":
            self.field.height = int(value)
        elif key == "max_rounds":
            self.max_rounds = int(value)
        else:
            stderr.write('Cannot parse settings input with key {}'.format(key))

    def parse_game_updates(self, key, value):
        if key == "round":
            self.round = int(value)
        elif key == "field":
            self.field.parse(value)
        else:
            stderr.write('Cannot parse game update with key {}'.format(key))

    def parse_player_updates(self, player_name, key, value):
        player = self.players.get(player_name)

        if player is None:
            stderr.write('Cannot find player with name {}'.format(player_name))
            return

        if key == "living_cells":
            player.living_cells = int(value)
        elif key == "move":
            player.previous_move = value
        else:
            stderr.write('Cannot parse {} update with key {}'.format(player_name, key))

    def time_remaining(self):
        return self.timebank - int(1000 * (time.clock() - self.last_update))

    @staticmethod
    def print_move(move):
        """issue an order"""
        stdout.write('{}\n'.format(move))
        stdout.flush()

    def run(self, bot):
        """parse input, update game state and call the bot classes do_turn method"""
        not_finished = True
        data = ''

        while not stdin.closed and not_finished:
            try:
                current_line = stdin.readline().rstrip('\r\n')

                if len(current_line) <= 0:
                    time.sleep(1)
                    continue

                data += current_line + "\n"
                if current_line.lower().startswith("action"):
                    self.update(data)

                    move = bot.make_move(self)
                    self.print_move(move)

                    data = ''
                elif current_line.lower().startswith("quit"):
                    not_finished = False
            except EOFError:
                break
            except KeyboardInterrupt:
                raise
            except:
                # don't raise error or return so that bot attempts to stay alive
                traceback.print_exc(file=stderr)
                stderr.flush()
