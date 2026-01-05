import pygame

from src.tree.quadtree import Quadtree

from src.entities.entity import Entity

from src.constants import WINDOW, FPS, COLOUR, ENTITIES


pygame.init()


def main():
    screen = pygame.display.set_mode((WINDOW["width"], WINDOW["height"]), pygame.RESIZABLE)
    pygame.display.set_caption(WINDOW["title"])
    clock = pygame.time.Clock()

    quadtree = Quadtree()
    entities = [Entity() for _ in range(ENTITIES)]

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # UPDATE
        for entity in entities:
            entity.update()
        quadtree.construct(entities)
        for entity in entities:
            if entity.colliding:
                continue
            node = quadtree.query(entity.x, entity.y)
            if node is None:
                continue
            for other in node.entities:
                if entity is other:
                    continue
                if entity.collide(other):
                    entity.colliding = other.colliding = True
                    break

        # RENDER
        screen.fill(COLOUR["black"])
        quadtree.render(screen)
        for entity in entities:
            entity.render(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
