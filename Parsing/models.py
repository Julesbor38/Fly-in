from enum import Enum, auto
from dataclasses import dataclass, field


class Zone(Enum):
    NORMAL = auto()
    RESTRICTED = auto()
    PRIORITY = auto()
    BLOCKED = auto()

    @staticmethod
    def get_zone(zone_str: str) -> "Zone":
        match zone_str:
            case "normal":
                return Zone.NORMAL
            case "restricted":
                return Zone.RESTRICTED
            case "priority":
                return Zone.PRIORITY
            case "blocked":
                return Zone.BLOCKED
            case _:
                return Zone.NORMAL


DEFAULT_COLOR = "gray"


@dataclass
class NodeMetadata:
    zone: Zone = Zone.NORMAL
    color: str = DEFAULT_COLOR
    max_drones: int = 1


@dataclass
class ConnectionMetadata:
    max_link_capacity: int = 1


@dataclass
class Node:
    name: str
    x: int
    y: int
    metadata: NodeMetadata = field(default_factory=NodeMetadata)


@dataclass
class Connection:
    source: str
    target: str
    metadata: ConnectionMetadata = field(default_factory=ConnectionMetadata)


@dataclass
class Level:
    nb_drones: int
    start_hub: Node
    end_hub: Node
    hubs: dict[str, Node]
    connections: list[Connection]
