import pygame
from Parsing.models import Level

COLORS = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "gray": (128, 128, 128),
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "orange": (255, 165, 0),
    "purple": (128, 0, 128),
    "brown": (165, 42, 42),
    "gold": (255, 215, 0),
    "darkred": (139, 0, 0),
}


def visualisation(level: Level) -> None:
    pygame.init()

    WIDTH = 3000
    HEIGHT = 2000
    SCALE = 200
    OFFSET_X = 100
    OFFSET_Y = HEIGHT // 2
    DEFAULT_COLOR = (180, 180, 180)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fly-in")
    clock = pygame.time.Clock()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        screen.fill((30, 30, 30))
        for node in level.hubs.values():
            x = OFFSET_X + node.x * SCALE
            y = OFFSET_Y - node.y * SCALE
            rgb: tuple[int, int, int] = COLORS.get(
                node.metadata.color.lower(), DEFAULT_COLOR)
            pygame.draw.circle(screen, rgb, (x, y), 60)
        for connections in level.connections:
            hub1 = level.hubs[connections.source]
            hub2 = level.hubs[connections.target]
            x1 = OFFSET_X + hub1.x * SCALE
            y1 = OFFSET_Y - hub1.y * SCALE
            x2 = OFFSET_X + hub2.x * SCALE
            y2 = OFFSET_Y - hub2.y * SCALE
            pygame.draw.line(screen, (200, 200, 200), (x1, y1), (x2, y2), 10)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
