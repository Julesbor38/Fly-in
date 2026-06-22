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
    scale_x: float,
    scale_y: float,
    offset_x: float,
    offset_y: float,
) -> None:
    """Draw all hubs on the screen.

    Each hub is rendered using its configured color. The current
    occupancy is displayed above the hub and the hub name is shown
    below it.
    """
    HUB_RADIUS = 45

    for node in level.hubs.values():

        x = offset_x + node.x * scale_x
        y = offset_y - node.y * scale_y

        rgb = COLORS.get(
            node.metadata.color.lower(), (180, 180, 180))

        occupancy = simulator.hub_occupancy.get(
            node.name, 0)

        pygame.draw.circle(screen, rgb, (x, y), HUB_RADIUS)

        pygame.draw.circle(screen, (255, 255, 255), (x, y), HUB_RADIUS, 3)

        count_text = font.render(str(occupancy), True, (255, 0, 0))
        screen.blit(
            count_text, (x - count_text.get_width() // 2, y - HUB_RADIUS - 25))

        name_text = font.render(node.name, True, (180, 130, 20))
        screen.blit(
            name_text, (x - name_text.get_width() // 2, y + HUB_RADIUS + 10))


def draw_connections(
    screen: pygame.Surface,
    level: Level,
    scale_x: float,
    scale_y: float,
    offset_x: float,
    offset_y: float,
) -> None:
    """Draw all connections between hubs.

    Connections are represented as lines linking the coordinates
    of their source and target hubs.
    """

    for connection in level.connections:

        source = level.hubs[connection.source]
        target = level.hubs[connection.target]

        x1 = offset_x + source.x * scale_x
        y1 = offset_y - source.y * scale_y

        x2 = offset_x + target.x * scale_x
        y2 = offset_y - target.y * scale_y

        pygame.draw.line(
            screen, (180, 180, 180), (x1, y1), (x2, y2), 8)


def draw_drones(
    screen: pygame.Surface,
    level: Level,
    simulator: Simulator,
    drone_image: pygame.Surface,
    font: pygame.font.Font,
    scale_x: float,
    scale_y: float,
    offset_x: float,
    offset_y: float,
) -> None:
    """Draw and animate drones.

    Drones smoothly interpolate toward their target position,
    whether they are located on a hub or currently travelling
    through a connection.
    """
    for drone in simulator.drones:
        if drone.current_connection:

            source_name, target_name = (
                drone.current_connection)

            source = level.hubs[source_name]
            target = level.hubs[target_name]

            target_x = (
                offset_x + ((source.x + target.x) / 2) * scale_x)

            target_y = (
                offset_y - ((source.y + target.y) / 2) * scale_y)

        else:

            hub = level.hubs[drone.current_hub]

            target_x = (offset_x + hub.x * scale_x)
            target_y = (offset_y - hub.y * scale_y)

        drone.render_x += (target_x - drone.render_x) * 0.15
        drone.render_y += (target_y - drone.render_y) * 0.15

        screen.blit(
            drone_image,
            (drone.render_x - drone_image.get_width() // 2,
             drone.render_y - drone_image.get_height() // 2))

        text = font.render(str(drone.id), True, (255, 255, 255))

        screen.blit(
            text,
            (drone.render_x - text.get_width() // 2,
             drone.render_y - text.get_height() // 2))


def handle_events(running: bool, paused: bool, dragging_slider: bool,
                  knob_x: float, slider_x: int, slider_width: int,
                  start_button: pygame.Rect,
                  pause_button: pygame.Rect, restart_button: pygame.Rect
                  ) -> tuple[bool, bool, bool, float | None, bool, bool]:
    """Handle user inputs.

    Processes keyboard and mouse events to control the simulation,
    including play/pause, restart, speed slider interaction and
    return to the map selection menu.

    Returns:
        Updated simulation state flags and optional slider value.
    """
    slider_value = None
    restart_requested = False
    back_to_menu = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            back_to_menu = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                paused = False
            elif pause_button.collidepoint(event.pos):
                paused = True
            elif restart_button.collidepoint(event.pos):
                restart_requested = True
            elif abs(event.pos[0] - knob_x) < 15:
                dragging_slider = True
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging_slider = False
        elif (event.type == pygame.MOUSEMOTION and dragging_slider):
            slider_value = (event.pos[0] - slider_x) / slider_width
            slider_value = max(0.0, min(1.0, slider_value))

    return (running, paused, dragging_slider, slider_value,
            restart_requested, back_to_menu)


def draw_ui(screen: pygame.Surface, font: pygame.font.Font, level: Level,
            start_button: pygame.Rect, pause_button: pygame.Rect,
            restart_button: pygame.Rect, slider_x: int, slider_y: int,
            slider_width: int, slider_height: int,
            knob_x: float, simulation_speed: float, paused: bool) -> None:
    """Draw the simulation user interface.

    Displays the current turn counter, control buttons, speed
    slider and simulation state indicator.
    """

    turn_text = font.render(f"Turn: {level.turn}", True, (255, 255, 255))
    screen.blit(turn_text, (20, 20))

    pygame.draw.rect(screen, (50, 150, 50), start_button, border_radius=10)
    pygame.draw.rect(screen, (180, 120, 30), pause_button, border_radius=10)
    pygame.draw.rect(screen, (180, 50, 50), restart_button, border_radius=10)
    pygame.draw.rect(screen, (100, 100, 100), (slider_x, slider_y,
                                               slider_width, slider_height))
    pygame.draw.circle(screen, (255, 255, 255),
                       (int(knob_x), slider_y + slider_height // 2), 10)
    screen.blit(font.render("Start", True, (255, 255, 255)), (50, 80))
    screen.blit(font.render("Pause", True, (255, 255, 255)), (190, 80))
    screen.blit(font.render("Restart", True, (255, 255, 255)),
                (restart_button.x + 15, restart_button.y + 10))
    speed_text = font.render(f"Speed x{simulation_speed:.1f}",
                             True, (255, 255, 255))
    screen.blit(speed_text, (slider_x, slider_y + 25))
    state_text = font.render(
        "PAUSED" if paused else "RUNNING", True, (255, 255, 255))
    screen.blit(state_text, (20, 220))


def update_speed(slider_x: int, slider_width: int,
                 slider_value: float) -> tuple[float, float]:
    """Compute simulation speed from slider position.

    Converts the slider value into a simulation speed multiplier
    and updates the visual position of the slider knob.

    Returns:
        A tuple containing the simulation speed and knob position.
    """
    knob_x = (slider_x + slider_width * slider_value)
    simulation_speed = (0.25 + slider_value * 3.75) / 2
    return simulation_speed, knob_x


def restart_simulation(level: Level, simulator: Simulator, scale_x: float,
                       scale_y: float,
                       offset_x: float, offset_y: float) -> bool:
    """Reset the simulation to its initial state.

    All drones are moved back to the start hub, occupancies are
    cleared, the turn counter is reset and rendering positions are
    reinitialized.

    Returns:
        True to indicate that the simulation should remain paused
        after the reset.
    """
    level.turn = 0
    simulator.hub_occupancy.clear()
    simulator.connection_occupancy.clear()
    simulator.hub_occupancy[
        simulator.graph.start_hub.name] = len(simulator.drones)
    for drone in simulator.drones:
        drone.current_hub = (simulator.graph.start_hub.name)
        drone.path_index = 0
        drone.wait_turns = 0
        drone.pending_hub = None
        drone.current_connection = None
        hub = level.hubs[drone.current_hub]
        drone.render_x = (offset_x + hub.x * scale_x)
        drone.render_y = (offset_y - hub.y * scale_y)
    return True


def visualisation(level: Level, simulator: Simulator) -> str | None:
    """Run the main visualization loop.

    Creates the Pygame window, renders the graph and drones,
    updates the simulation state and handles user interactions.

    Returns:
        "menu" when the user requests a return to the map selection
        screen, otherwise None when the visualization is closed.
    """
    pygame.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    PADDING = 150
    min_x = min(node.x for node in level.hubs.values())
    max_x = max(node.x for node in level.hubs.values())

    min_y = min(node.y for node in level.hubs.values())
    max_y = max(node.y for node in level.hubs.values())

    map_width = max_x - min_x
    map_height = max_y - min_y

    SCALE_X = (WIDTH - 2 * PADDING) / max(map_width, 1)
    SCALE_Y = ((HEIGHT - 2 * PADDING) / max(map_height, 1) * 0.8)

    map_pixel_width = map_width * SCALE_X
    map_pixel_height = map_height * SCALE_Y

    OFFSET_X = ((WIDTH - map_pixel_width) / 2 - min_x * SCALE_X)
    OFFSET_Y = ((HEIGHT + map_pixel_height) / 2 + min_y * SCALE_Y)
    MOVE_DURATION = 500
    paused = False
    slider_x = 20
    slider_y = 150
    slider_width = 250
    slider_height = 6
    slider_value = 0.5
    simulation_speed, knob_x = update_speed(slider_x,
                                            slider_width, slider_value)
    dragging_slider = False
    last_move = pygame.time.get_ticks()

    pygame.display.set_caption("Fly-in")
    clock = pygame.time.Clock()
    drone_image = pygame.image.load("graph/assets/drones.png").convert_alpha()
    drone_image = pygame.transform.scale(drone_image, (50, 50))
    font = pygame.font.Font(None, 30)
    start_button = pygame.Rect(20, 70, 120, 40)
    pause_button = pygame.Rect(160, 70, 120, 40)
    restart_button = pygame.Rect(300, 70, 120, 40)
    running = True
    for drone in simulator.drones:
        hub = level.hubs[drone.current_hub]
        drone.render_x = OFFSET_X + hub.x * SCALE_X
        drone.render_y = OFFSET_Y - hub.y * SCALE_Y
    while running:
        (
            running,
            paused,
            dragging_slider,
            new_slider_value,
            restart_requested,
            back_to_menu
        ) = handle_events(
            running,
            paused,
            dragging_slider,
            knob_x,
            slider_x,
            slider_width,
            start_button,
            pause_button,
            restart_button
        )
        if back_to_menu:
            pygame.display.quit()
            return "menu"
        if restart_requested:
            paused = restart_simulation(level,
                                        simulator, SCALE_X, SCALE_Y,
                                        OFFSET_X, OFFSET_Y)
            last_move = pygame.time.get_ticks()
        if new_slider_value is not None:
            slider_value = new_slider_value
        simulation_speed, knob_x = (update_speed(slider_x,
                                                 slider_width, slider_value))

        current_time = pygame.time.get_ticks()
        effective_duration = (MOVE_DURATION / simulation_speed)
        if (not paused and current_time - last_move > effective_duration):
            simulator.step()
            last_move = current_time
            if not all(drone.current_hub == level.end_hub.name for
                       drone in simulator.drones):
                level.turn += 1
        screen.fill((30, 30, 30))

        draw_ui(screen, font, level, start_button, pause_button,
                restart_button, slider_x, slider_y, slider_width,
                slider_height, knob_x, simulation_speed, paused)

        draw_connections(screen, level, SCALE_X, SCALE_Y, OFFSET_X, OFFSET_Y)

        draw_hubs(screen, level, simulator, font, SCALE_X,
                  SCALE_Y, OFFSET_X, OFFSET_Y)

        draw_drones(screen, level, simulator, drone_image,
                    font, SCALE_X, SCALE_Y, OFFSET_X, OFFSET_Y)
        current_time = pygame.time.get_ticks()

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
