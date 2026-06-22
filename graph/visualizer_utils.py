from Parsing.models import Level
from graph.visualizer_models import Viewport
from graph.visualizer_models import UIState
from graph.visualizer_models import Buttons
import pygame


def build_viewport(
    level: Level,
    width: int,
    height: int,
    padding: int = 150
) -> Viewport:
    """Compute scaling and offsets needed to center the map."""

    min_x = min(node.x for node in level.hubs.values())
    max_x = max(node.x for node in level.hubs.values())

    min_y = min(node.y for node in level.hubs.values())
    max_y = max(node.y for node in level.hubs.values())

    map_width = max_x - min_x
    map_height = max_y - min_y

    scale_x = (
        width - 2 * padding
    ) / max(map_width, 1)

    scale_y = (
        (height - 2 * padding)
        / max(map_height, 1)
        * 0.8
    )

    map_pixel_width = map_width * scale_x
    map_pixel_height = map_height * scale_y

    offset_x = (
        (width - map_pixel_width) / 2
        - min_x * scale_x
    )

    offset_y = (
        (height + map_pixel_height) / 2
        + min_y * scale_y
    )

    return Viewport(
        scale_x=scale_x,
        scale_y=scale_y,
        offset_x=offset_x,
        offset_y=offset_y
    )


def build_ui() -> UIState:
    """Create the initial UI state."""

    return UIState(
        paused=False,
        dragging_slider=False,
        slider_value=0.5,
        simulation_speed=1.0,
        knob_x=0.0,
        slider_x=20,
        slider_y=150,
        slider_width=250,
        slider_height=6
    )


def build_buttons() -> Buttons:
    """Create all simulation control buttons."""

    return Buttons(
        start=pygame.Rect(20, 70, 120, 40),
        pause=pygame.Rect(160, 70, 120, 40),
        restart=pygame.Rect(300, 70, 120, 40)
    )
