from pathlib import Path
import pygame
from Parsing.parsing import Parser
from graph.graph import Graph
from Parsing.exception import MapError


def get_maps() -> list[tuple[str, bool]]:
    """Extract all maps from maps/ file, Using a list[tuple[str, bool]] format,
    this is usefull in map_selection to get a representation of unusable map"""

    maps: list[tuple[str, bool]] = []

    for file in Path("maps").rglob("*.txt"):
        try:
            parser = Parser(str(file))
            level = parser.parsing()
            graph = Graph(level)
            path = graph.shortest_path(
                graph.start_hub.name, graph.end_hub.name)
            if not path:
                raise MapError(f"Couldn't find Exit point from start: {file}")
            maps.append((str(file), True))
        except Exception:
            maps.append((str(file), False))
    maps.sort()

    return maps


def map_selection() -> str:
    """creation of a first menu using Pygame, this minimalist menu present all
    maps using different color, green for the selected map, yellow for all
    usable map and red for unusable map which cannot be elected, there is
    also information about how tu use it """
    try:
        pygame.init()
        pygame.display.set_caption("Menu Fly-in")

        screen = pygame.display.set_mode((1200, 800))

        font = pygame.font.Font(None, 40)
        fond = pygame.image.load("graph/assets/menu.png").convert()
        fond = pygame.transform.scale(fond, (1200, 800))

        maps = get_maps()
        if not maps:
            raise FileNotFoundError("No map found in maps")

        selected = 0

        running = True

        while running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    raise SystemExit

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_UP:
                        selected = max(0, selected - 1)

                    elif event.key == pygame.K_DOWN:
                        selected = min(
                            len(maps) - 1,
                            selected + 1
                        )

                    elif event.key == pygame.K_RETURN:
                        if maps[selected][1]:
                            pygame.quit()
                            return maps[selected][0]
                    elif event.key == pygame.K_ESCAPE:
                        raise SystemExit
                if event.type == pygame.MOUSEBUTTONDOWN:

                    for i, (map_name, is_valid) in enumerate(maps):

                        display_name = Path(map_name).stem

                        if not is_valid:
                            display_name += " [UNUSABLE]"

                        rect = pygame.Rect(
                            50 - 12,
                            150 + i * 55 - 6,
                            font.size(display_name)[0] + 24,
                            font.size(display_name)[1] + 12
                        )

                        if rect.collidepoint(event.pos):

                            if is_valid:
                                pygame.quit()
                                return map_name
                elif event.type == pygame.MOUSEMOTION:

                    for i, (map_name, is_valid) in enumerate(maps):

                        display_name = Path(map_name).stem

                        if not is_valid:
                            display_name += " [UNUSABLE]"

                        rect = pygame.Rect(
                            50 - 12,
                            140 + i * 55 - 6,
                            font.size(display_name)[0] + 24,
                            font.size(display_name)[1] + 12
                        )

                        if rect.collidepoint(event.pos):
                            selected = i
                            break
            screen.blit(fond, (0, 0))

            draw_text_box(
                screen,
                "Press ENTER to launch",
                font,
                (180, 180, 180),
                (50, 30)
            )

            draw_text_box(
                screen,
                "Choose a map",
                font,
                (255, 255, 255),
                (50, 85)
            )

            draw_text_box(
                screen,
                "Press ESC to quit",
                font,
                (255, 50, 50),
                (930, 30)
            )

            for i, (map_name, is_valid) in enumerate(maps):
                if not is_valid:
                    color = (255, 50, 50)
                elif i == selected:
                    color = (0, 255, 0)
                else:
                    color = (255, 255, 0)
                display_name = Path(map_name).stem
                if not is_valid:
                    display_name += " [UNUSABLE]"
                draw_text_box(
                            screen,
                            display_name,
                            font,
                            color,
                            (50, 140 + i * 55)
                        )

            pygame.display.flip()
        raise RuntimeError("map_selection exited unexpectecly")
    except Exception as e:
        raise RuntimeError(f"Menu failed: {e}") from e


def draw_text_box(screen: pygame.Surface, text: str, font: pygame.font.Font,
                  text_color: tuple[int, int, int], pos: tuple[int, int]) -> pygame.Rect:

    txt = font.render(text, True, text_color)
    rect = txt.get_rect(topleft=pos)

    padding_x = 12
    padding_y = 6

    box_rect = pygame.Rect(rect.x - padding_x,
                           rect.y - padding_y,
                           rect.width + padding_x * 2,
                           rect.height + padding_y * 2)

    bg = pygame.Surface(box_rect.size, pygame.SRCALPHA)

    # Couleur du contour selon la couleur du texte
    if text_color == (0, 255, 0):
        border_color = (0, 255, 120, 255)
    elif text_color == (255, 50, 50):
        border_color = (255, 80, 80, 255)
    else:
        border_color = (255, 200, 0, 255)

    pygame.draw.rect(
        bg,
        (10, 20, 40, 150),
        bg.get_rect(),
        border_radius=8
    )

    pygame.draw.rect(
        bg,
        border_color,
        bg.get_rect(),
        width=2,
        border_radius=8
    )

    screen.blit(
        bg,
        (rect.x - padding_x,
         rect.y - padding_y)
    )

    screen.blit(txt, rect)
    return box_rect

