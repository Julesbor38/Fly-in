from dataclasses import dataclass
import pygame


@dataclass
class Viewport:
    scale_x: float
    scale_y: float
    offset_x: float
    offset_y: float


@dataclass
class UIState:
    paused: bool
    dragging_slider: bool
    slider_value: float
    simulation_speed: float
    knob_x: float
    slider_x: int
    slider_y: int
    slider_width: int
    slider_height: int


@dataclass
class Buttons:
    start: pygame.Rect
    pause: pygame.Rect
    restart: pygame.Rect
