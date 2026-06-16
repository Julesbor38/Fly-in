import pygame
from Parsing.models import Level
from graph.simulator import Simulator

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


def visualisation(level: Level, simulator: Simulator) -> None:
    pygame.init()

    WIDTH = 4600
    HEIGHT = 2000
    SCALE = 200
    OFFSET_X = 100
    OFFSET_Y = HEIGHT // 2
    DEFAULT_COLOR = (180, 180, 180)
    last_move = pygame.time.get_ticks()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fly-in")
    clock = pygame.time.Clock()
    drone_image = pygame.image.load("graph/assets/drones.png").convert_alpha()
    drone_image = pygame.transform.scale(drone_image, (50, 50))
    font = pygame.font.Font(None, 30)
    running = True
    while running:
        if all(
            drone.current_hub == level.end_hub.name
            for drone in simulator.drones
        ):
            print(
                f"Finished in {level.turn} turns"
            )
            running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        screen.fill((30, 30, 30))
        turn_text = font.render(
            f"Turn: {level.turn}",
            True,
            (255, 255, 255)
        )

        screen.blit(
            turn_text,
            (20, 20)
        )
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
        current_time = pygame.time.get_ticks()
        if current_time - last_move > 1000:
            level.turn += 1
            simulator.step()
            last_move = current_time
        try:
            for drone in simulator.drones:

                if drone.current_connection is not None:

                    source_name, target_name = drone.current_connection

                    source = level.hubs[source_name]
                    target = level.hubs[target_name]

                    x1 = OFFSET_X + source.x * SCALE
                    y1 = OFFSET_Y - source.y * SCALE

                    x2 = OFFSET_X + target.x * SCALE
                    y2 = OFFSET_Y - target.y * SCALE

                    # milieu de la connexion
                    x = (x1 + x2) // 2
                    y = (y1 + y2) // 2

                else:

                    hub = level.hubs[drone.current_hub]

                    x = OFFSET_X + hub.x * SCALE
                    y = OFFSET_Y - hub.y * SCALE

                screen.blit(
                    drone_image,
                    (
                        x - drone_image.get_width() // 2,
                        y - drone_image.get_height() // 2
                    )
                )

                text = font.render(
                    str(drone.id),
                    True,
                    (255, 255, 255)
                )

                screen.blit(
                    text,
                    (
                        x - text.get_width() // 2,
                        y - text.get_height() // 2
                    )
                )
            pygame.display.flip()
            clock.tick(60)
        except Exception:
            print("MapError, could not identify Exit point from start")
            break
    pygame.quit()
