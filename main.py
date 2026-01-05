import pygame

from src.entities.entity import Entity
from src.entities.octree import Octree

from src.constants import WINDOW, FPS, COLOUR, ENTITIES


pygame.init()


def main():
    screen = pygame.display.set_mode((WINDOW["width"], WINDOW["height"]), pygame.RESIZABLE)
    pygame.display.set_caption(WINDOW["title"])
    clock = pygame.time.Clock()

    octree = Octree()
    entities = [Entity() for _ in range(ENTITIES)]

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # UPDATE
        for entity in entities:
            entity.update()
        for entity in entities:
            for other in entities:
                if entity == other:
                    continue
                if entity.collide(other):
                    entity.colliding = True
                    break
        octree.construct(entities)

        # RENDER
        screen.fill(COLOUR["black"])
        octree.render(screen)
        for entity in entities:
            entity.render(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
