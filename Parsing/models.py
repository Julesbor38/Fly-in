from enum import Enum, auto
from dataclasses import dataclass, field


class Zone(Enum):

    NORMAL = auto()
    RESTRICTED = auto()
    PRIORITY = auto()
    BLOCKED = auto()

    @staticmethod
    def get_zone(zone_str: str) -> "Zone":
        """convert matedata.zone in str to Enum """
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
    """Using parsing regroup every information for the hubs"""
    name: str
    x: int
    y: int
    metadata: NodeMetadata = field(default_factory=NodeMetadata)


@dataclass
class Connection:
    """Using parsing regroup every information for the connections"""
    source: str
    target: str
    metadata: ConnectionMetadata = field(default_factory=ConnectionMetadata)


@dataclass
class Drone:
    """define a specific class for drone, all thes information
    are usefull for algorythm and visualisation"""
    id: int
    current_hub: str
    path: list[str]
    path_index: int = 0
    wait_turns: int = 0
    render_x: float = 0
    render_y: float = 0
    pending_hub: str | None = None
    current_connection: tuple[str, str] | None = None


@dataclass
class Level:
    """class Level is usefull for solver and visualizer
     for every maps, this can give us every information to create a
     great algorythm and visualisation """
    nb_drones: int
    start_hub: Node
    end_hub: Node
    hubs: dict[str, Node]
    connections: list[Connection]
    turn: int = 0
    is_finished: bool = False
