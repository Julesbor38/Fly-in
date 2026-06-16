from .models import Node, Connection


def hub_exists(hubs: dict[str, Node], name: str) -> bool:
    return name in hubs


def coordinates_exists(hubs: dict[str, Node], x: int, y: int) -> bool:
    for hub in hubs.values():
        if hub.x == x and hub.y == y:
            return True
    return False


def connection_exists(connections: list[Connection],
                      source: str, target: str) -> bool:
    return any(
        (connection.source == source and connection.target == target)
        or (connection.source == target and connection.target == source)
        for connection in connections)