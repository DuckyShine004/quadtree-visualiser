import math
import random
import pygame

from src.constants import COLOUR, WINDOW, EPSILON


class Entity:
    SIZE = 8
    SPEED_LIMIT = (1, 5)
    COLOUR = {"default": COLOUR["blue"], "collision": COLOUR["red"]}

    def __init__(self):
        self.bounds = (self.SIZE, WINDOW["size"] - self.SIZE)

        self.x = random.uniform(*self.bounds)
        self.y = random.uniform(*self.bounds)
        self.centre = (self.x, self.y)

        self.speed = random.uniform(*self.SPEED_LIMIT)
        self.direction = self.get_initial_direction()

        self.colliding = False

    def get_initial_direction(self):
        x = random.uniform(EPSILON, 1) * random.choice([-1, 1])
        y = random.uniform(EPSILON, 1) * random.choice([-1, 1])

        return self.normalise((x, y))

    def normalise(self, vector):
        magnitude = self.get_magnitude(*vector)

        if magnitude <= EPSILON:
            return vector

        dx = vector[0] / magnitude
        dy = vector[1] / magnitude

        return [dx, dy]

    def collide(self, other):
        dx = self.x - other.x
        dy = self.y - other.y

        distance = self.get_magnitude(dx, dy)

        return distance <= self.SIZE

    def get_magnitude(self, x, y):
        return math.sqrt(x * x + y * y)

    def get_velocity(self):
        dx = self.speed * self.direction[0]
        dy = self.speed * self.direction[1]

        return (dx, dy)

    def clamp(self, value, _min, _max):
        return max(_min, min(value, _max))

    def update(self):
        velocity = self.get_velocity()

        dx = self.x + velocity[0]
        dy = self.y + velocity[1]

        out_of_bounds = False

        direction = self.direction

        if dx >= WINDOW["width"]:
            direction[0] = random.uniform(EPSILON, 1) * -1
            out_of_bounds = True

        if dx <= 0:
            direction[0] = random.uniform(EPSILON, 1)
            out_of_bounds = True

        if dy >= WINDOW["height"]:
            direction[1] = random.uniform(EPSILON, 1) * -1
            out_of_bounds = True

        if dy <= 0:
            direction[1] = random.uniform(EPSILON, 1)
            out_of_bounds = True

        if out_of_bounds:
            self.speed = random.uniform(*self.SPEED_LIMIT)
            self.direction = self.normalise(direction)

        self.x = self.clamp(dx, 0, WINDOW["width"])
        self.y = self.clamp(dy, 0, WINDOW["height"])
        self.centre = (self.x, self.y)

        self.colliding = False

    def render(self, screen):
        colour = self.COLOUR["collision"] if self.colliding else self.COLOUR["default"]

        pygame.draw.circle(screen, colour, self.centre, self.SIZE)
