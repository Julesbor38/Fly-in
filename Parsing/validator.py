from .models import Node, Connection


def hub_exists(hubs: dict[str, Node], name: str) -> bool:
    """check if hub_name already exist"""
    return name in hubs


def coordinates_exists(hubs: dict[str, Node], x: int, y: int) -> bool:
    """check if hub_coordinate already exist"""
    for hub in hubs.values():
        if hub.x == x and hub.y == y:
            return True
    return False


def connection_exists(connections: list[Connection],
                      source: str, target: str) -> bool:
    """check if connection already exist"""
    return any(
        (connection.source == source and connection.target == target)
        or (connection.source == target and connection.target == source)
        for connection in connections)
