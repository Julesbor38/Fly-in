from .models import Node, Connection


def hub_exists(hubs: list[Node], name: str) -> bool:
    return any(hub.name == name for hub in hubs)


def coordinates_exists(hubs: list[Node], x: int, y: int) -> bool:
    return any(hub.x == x and hub.y == y for hub in hubs)


def connection_exists(connections: list[Connection],
                      source: str, target: str) -> bool:
    return any(
        (connection.source == source and connection.target == target)
        or (connection.source == target and connection.target == source)
        for connection in connections)
