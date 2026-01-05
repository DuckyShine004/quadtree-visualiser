import pygame

from src.constants import WINDOW, COLOUR


class Octree:
    MAX_DEPTH = 8
    CAPACITY = 2
    THICKNESS = 2
    COLOUR = {"grid": COLOUR["white"]}

    def __init__(self):
        self.grids = set()

    def construct(self, entities):
        self.grids = set()

        def _construct(x, y, size, depth):
            if depth > Octree.MAX_DEPTH:
                return False

            left = x
            right = x + size
            top = y
            bottom = y + size

            capacity = 0

            for entity in entities:
                if left <= entity.x < right and top <= entity.y < bottom:
                    capacity += 1

            if capacity <= Octree.CAPACITY:
                return True

            next_size = size >> 1
            next_depth = depth + 1

            if _construct(left, top, next_size, next_depth):
                self.grids.add((left, top, next_size))

            if _construct(left + next_size, top, next_size, next_depth):
                self.grids.add((left + next_size, top, next_size))

            if _construct(left, top + next_size, next_size, next_depth):
                self.grids.add((left, top + next_size, next_size))

            if _construct(left + next_size, top + next_size, next_size, next_depth):
                self.grids.add((left + next_size, top + next_size, next_size))

            return False

        _construct(0, 0, WINDOW["size"], 0)

    def render(self, screen):
        for x, y, size in self.grids:
            rectangle = (x, y, size, size)
            pygame.draw.rect(screen, Octree.COLOUR["grid"], rectangle, Octree.THICKNESS)
