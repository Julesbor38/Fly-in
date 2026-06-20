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


def draw_hubs(
    screen: pygame.Surface,
    level: Level,
    simulator: Simulator,
    font: pygame.font.Font,
    scale: int,
    offset_x: int,
    offset_y: int,
) -> None:

    HUB_RADIUS = 45

    for node in level.hubs.values():

        x = offset_x + node.x * scale
        y = offset_y - node.y * scale

        rgb = COLORS.get(
            node.metadata.color.lower(),
            (180, 180, 180)
        )

        occupancy = simulator.hub_occupancy.get(
            node.name,
            0
        )

        pygame.draw.circle(
            screen,
            rgb,
            (x, y),
            HUB_RADIUS
        )

        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (x, y),
            HUB_RADIUS,
            3
        )

        count_text = font.render(
            str(occupancy),
            True,
            (255, 255, 255)
        )

        screen.blit(
            count_text,
            (
                x - count_text.get_width() // 2,
                y - HUB_RADIUS - 25
            )
        )

        name_text = font.render(
            node.name,
            True,
            (255, 255, 255)
        )

        screen.blit(
            name_text,
            (
                x - name_text.get_width() // 2,
                y + HUB_RADIUS + 10
            )
        )


def draw_connections(
    screen: pygame.Surface,
    level: Level,
    scale: int,
    offset_x: int,
    offset_y: int,
) -> None:

    for connection in level.connections:

        source = level.hubs[
            connection.source
        ]

        target = level.hubs[
            connection.target
        ]

        x1 = offset_x + source.x * scale
        y1 = offset_y - source.y * scale

        x2 = offset_x + target.x * scale
        y2 = offset_y - target.y * scale

        pygame.draw.line(
            screen,
            (180, 180, 180),
            (x1, y1),
            (x2, y2),
            8
        )


def draw_drones(
    screen: pygame.Surface,
    level: Level,
    simulator: Simulator,
    drone_image: pygame.Surface,
    font: pygame.font.Font,
    scale: int,
    offset_x: int,
    offset_y: int,
) -> None:

    for drone in simulator.drones:

        if drone.current_connection:

            source_name, target_name = (
                drone.current_connection
            )

            source = level.hubs[source_name]
            target = level.hubs[target_name]

            target_x = (
                offset_x
                + ((source.x + target.x) / 2) * scale
            )

            target_y = (
                offset_y
                - ((source.y + target.y) / 2) * scale
            )

        else:

            hub = level.hubs[
                drone.current_hub
            ]

            target_x = (
                offset_x
                + hub.x * scale
            )

            target_y = (
                offset_y
                - hub.y * scale
            )

        drone.render_x += (
            target_x - drone.render_x
        ) * 0.15

        drone.render_y += (
            target_y - drone.render_y
        ) * 0.15

        screen.blit(
            drone_image,
            (
                drone.render_x
                - drone_image.get_width() // 2,

                drone.render_y
                - drone_image.get_height() // 2
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
                drone.render_x
                - text.get_width() // 2,

                drone.render_y
                - text.get_height() // 2
            )
        )


def visualisation(level: Level, simulator: Simulator) -> None:
    pygame.init()

    WIDTH = 4600
    HEIGHT = 2000
    SCALE = 200
    OFFSET_X = 100
    OFFSET_Y = HEIGHT // 2
    MOVE_DURATION = 500
    last_move = pygame.time.get_ticks()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fly-in")
    clock = pygame.time.Clock()
    drone_image = pygame.image.load("graph/assets/drones.png").convert_alpha()
    drone_image = pygame.transform.scale(drone_image, (50, 50))
    font = pygame.font.Font(None, 30)
    running = True
    for drone in simulator.drones:
        hub = level.hubs[drone.current_hub]
        drone.render_x = OFFSET_X + hub.x * SCALE
        drone.render_y = OFFSET_Y - hub.y * SCALE
    while running:
        if all(
            drone.current_hub == level.end_hub.name
            for drone in simulator.drones
        ):
            running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        current_time = pygame.time.get_ticks()
        if current_time - last_move > MOVE_DURATION:
            level.turn += 1
            simulator.step()
            last_move = current_time
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
        draw_connections(screen, level, SCALE, OFFSET_X, OFFSET_Y)

        draw_hubs(screen, level, simulator, font, SCALE, OFFSET_X, OFFSET_Y)

        current_time = pygame.time.get_ticks()

        draw_drones(screen, level, simulator, drone_image,
                    font, SCALE, OFFSET_X, OFFSET_Y)

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
