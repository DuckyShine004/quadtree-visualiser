from __future__ import annotations

from src.entities.entity import Entity

from typing import List, Optional


class Node:
    def __init__(
        self,
        x,
        y,
        size,
        top_left: Optional[Node] = None,
        top_right: Optional[Node] = None,
        bottom_left: Optional[Node] = None,
        bottom_right: Optional[Node] = None,
    ):
        self.x = x
        self.y = y
        self.size = size

        self.left = x
        self.right = x + size
        self.top = y
        self.bottom = y + size

        self.top_left = top_left
        self.top_right = top_right
        self.bottom_left = bottom_left
        self.bottom_right = bottom_right

        self.entities: List[Entity] = []

    def contains(self, x, y):
        return self.left <= x < self.right and self.top <= y < self.bottom
