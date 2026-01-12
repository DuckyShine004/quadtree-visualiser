import pygame

from collections import deque

from src.tree.node import Node

from src.constants import WINDOW, COLOUR

from typing import Optional


class Quadtree:
    MAX_DEPTH = 8
    MAX_CAPACITY = 2
    THICKNESS = 2
    COLOUR = {"grid": COLOUR["white"]}

    def __init__(self):
        self.root: Optional[Node] = None

        self.grids = []

    def construct(self, entities):
        def _construct(x, y, size, depth) -> Optional[Node]:
            if depth > self.MAX_DEPTH:
                return None

            left = x
            right = x + size
            top = y
            bottom = y + size

            node = Node(x, y, size)

            capacity = 0

            for entity in entities:
                if left <= entity.x < right and top <= entity.y < bottom:
                    node.entities.append(entity)
                    capacity += 1

            if capacity <= self.MAX_CAPACITY:
                return node

            next_size = size >> 1
            next_depth = depth + 1

            node.top_left = _construct(left, top, next_size, next_depth)
            node.top_right = _construct(left + next_size, top, next_size, next_depth)
            node.bottom_left = _construct(left, top + next_size, next_size, next_depth)
            node.bottom_right = _construct(left + next_size, top + next_size, next_size, next_depth)

            return node

        self.root = _construct(0, 0, WINDOW["size"], 0)

    def query(self, x, y) -> Optional[Node]:
        node = self.root

        if node is None:
            return None

        while True:
            next = None

            if node.top_left is not None and node.top_left.contains(x, y):
                next = node.top_left
            elif node.top_right is not None and node.top_right.contains(x, y):
                next = node.top_right
            elif node.bottom_left is not None and node.bottom_left.contains(x, y):
                next = node.bottom_left
            elif node.bottom_right is not None and node.bottom_right.contains(x, y):
                next = node.bottom_right

            if next is None:
                break

            node = next

        return node

    def construct_grid(self):
        self.grids.clear()

        queue = deque([self.root])

        while queue:
            node = queue.popleft()

            if node is None:
                continue

            self.grids.append((node.x, node.y, node.size))

            queue.append(node.top_left)
            queue.append(node.top_right)
            queue.append(node.bottom_left)
            queue.append(node.bottom_right)

    def render(self, screen):
        for x, y, size in self.grids:
            rectangle = (x, y, size, size)
            pygame.draw.rect(screen, self.COLOUR["grid"], rectangle, self.THICKNESS)
