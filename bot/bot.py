import random

from move.move import Move
from move.move_type import MoveType


class Bot:

    def __init__(self):
        random.seed()  # set seed here if needed

    def make_move(self, game):
        """
        Performs a Birth or a Kill move, currently returns a random move.
        Implement this method to make the bot smarter.
        """
        cell_map = game.field.get_cell_mapping()

        # if random.random() < 0.5:
        return self.make_random_birth_move(game, cell_map)

        # return self.make_random_kill_move(game, cell_map)

    def make_random_birth_move(self, game, cell_map):
        dead_cells = cell_map.get('.', [])
        my_cells = cell_map.get(game.me.id, [])

        if len(dead_cells) <= 0 or len(my_cells) < 2:
            return self.make_random_kill_move(game, cell_map)

        random_birth = dead_cells[random.randrange(len(dead_cells))]

        random_sacrifices = []
        for i in range(2):
            random_sacrifice = my_cells.pop(random.randrange(len(my_cells)))
            random_sacrifices.append(random_sacrifice)

        return Move(MoveType.BIRTH, random_birth, random_sacrifices)

    def make_random_kill_move(self, game, cell_map):
        my_cells = cell_map.get(game.me.id, [])
        opponent_cells = cell_map.get(game.opponent.id, [])
        living_cells = my_cells + opponent_cells

        if len(living_cells) <= 0:
            return Move(MoveType.PASS)

        random_kill = living_cells[random.randrange(len(living_cells))]

        return Move(MoveType.KILL, random_kill)
