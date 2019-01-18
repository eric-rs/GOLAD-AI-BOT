from field.point import Point


class Field:

    def __init__(self):
        self.width = None
        self.height = None
        self.cells = None

    def parse(self, field_input):
        self.cells = [[] for _ in range(self.width)]
        x = 0
        y = 0

        for cell in field_input.split(','):
            self.cells[x].insert(y, cell)
            x += 1

            if x == self.width:
                x = 0
                y += 1

    def get_cell_mapping(self):
        cell_map = {}

        for x in range(self.width):
            for y in range(self.height):
                cell = self.cells[x][y]
                cell_type_list = cell_map.get(cell, [])
                cell_type_list.append(Point(x, y))
                cell_map[cell] = cell_type_list

        return cell_map
