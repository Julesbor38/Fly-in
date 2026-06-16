from Parsing.models import Level, Node, Connection, Zone
from Parsing.exception import MapError


class Graph:

    def __init__(self, level: Level) -> None:

        self.nodes: dict[str, Node] = {}
        self.adjacency: dict[str, list[str]] = {}
        self.connection_map: dict[tuple[str, str], Connection] = {}

        self.connections: list[Connection] = level.connections

        self.start_hub = level.start_hub
        self.end_hub = level.end_hub

        self.build_graph(level)

    def build_graph(self, level: Level) -> None:
        for hub in level.hubs.values():
            self.nodes[hub.name] = hub
            self.adjacency[hub.name] = []
        for connection in level.connections:
            self.adjacency[connection.source].append(connection.target)
            self.adjacency[connection.target].append(connection.source)
            self.connection_map[
                (connection.source, connection.target)] = connection
            self.connection_map[
                (connection.target, connection.source)] = connection

    def get_neighbors(self, hub_name: str) -> list[str]:
        return self.adjacency[hub_name]

    def get_node(self, hub_name: str) -> Node:
        return self.nodes[hub_name]

    def get_travel_time(self, hub_name: str) -> int:
        node: Node = self.nodes[hub_name]

        match node.metadata.zone:
            case Zone.NORMAL:
                return 1
            case Zone.RESTRICTED:
                return 2
            case Zone.PRIORITY:
                return 1
            case Zone.BLOCKED:
                return 99999

    def display(self) -> None:
        for hub, neighbors in self.adjacency.items():
            print(f"{hub} -> {neighbors}")

    def is_priority_hub(self, hub_name: str) -> bool:
        return (self.nodes[hub_name].metadata.zone == Zone.PRIORITY)

    def shortest_path(self, start: str, end: str) -> list[str]:
        from heapq import heappush, heappop

        distances = {
            node_name: float("inf")
            for node_name in self.nodes
        }
        distances[start] = 0
        parents: dict[str, str | None] = {
            start: None
        }
        heap: list[tuple[float, str]] = []
        heappush(heap, (0, start))
        while heap:
            current_cost, current = heappop(heap)
            if current_cost > distances[current]:
                continue
            if current == end:
                break
            for neighbor in self.adjacency[current]:
                if self.nodes[neighbor].metadata.zone == Zone.BLOCKED:
                    continue
                new_cost = (current_cost + self.get_travel_time(neighbor))
                if new_cost < distances[neighbor]:
                    distances[neighbor] = new_cost
                    parents[neighbor] = current
                    heappush(heap, (new_cost, neighbor))
        if end not in parents:
            raise MapError("Couldn't find Exit point from start")
        path: list[str] = []
        current: str | None = end
        while current is not None:
            path.append(current)
            current = parents[current]
        print(distances)
        return path[::-1]
