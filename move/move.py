from move.move_type import MoveType


class Move:

    def __init__(self, move_type, target_point=None, sacrifice_points=None):
        self.move_type = move_type
        self.target_point = target_point
        self.sacrifice_points = sacrifice_points

    def __str__(self):
        if self.move_type == MoveType.KILL:
            return '{} {}'.format(self.move_type, self.target_point)
        elif self.move_type == MoveType.BIRTH:
            sacrifice_string = ' '.join(str(p) for p in self.sacrifice_points)
            return '{} {} {}'.format(self.move_type, self.target_point, sacrifice_string)

        return str(MoveType.PASS)
