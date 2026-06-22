from pathlib import Path
import pygame
from Parsing.parsing import Parser


def get_maps() -> list[tuple[str, bool]]:
    """Extract all maps from maps/ file, Using a list[tuple[str, bool]] format,
    this is usefull in map_selection to get a representation of unusable map"""

    maps: list[tuple[str, bool]] = []

    for file in Path("maps").rglob("*.txt"):
        try:
            parser = Parser(str(file))
            parser.parsing()
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

        screen = pygame.display.set_mode((1200, 800))

        font = pygame.font.Font(None, 40)

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

            screen.fill((30, 30, 30))

            title = font.render(
                "Choose a map", True, (255, 255, 255))
            instructions = font.render(
                "Press ENTER to launch", True, (180, 180, 180))
            leave_instructions = font.render(
                "Press ESC to quit", True, (180, 180, 180))

            screen.blit(instructions, (50, 70))

            screen.blit(title, (50, 30))

            screen.blit(leave_instructions, (900, 70))

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
                text = font.render(display_name, True, color)
                screen.blit(text, (50, 100 + i * 40))

            pygame.display.flip()
        raise RuntimeError("map_selection exited unexpectecly")
    except Exception as e:
        raise RuntimeError(f"Menu failed: {e}") from e
