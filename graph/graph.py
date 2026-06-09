from Parsing.models import Level, Node, Connection


class Graph:

    def __init__(self, level: Level) -> None:

        self.nodes: dict[str, Node] = {}
        self.adjacency: dict[str, list[str]] = {}

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

    def get_neighbors(self, hub_name: str) -> list[str]:
        return self.adjacency[hub_name]

    def get_node(self, hub_name: str) -> Node:
        return self.nodes[hub_name]

    def display(self) -> None:
        for hub, neighbors in self.adjacency.items():
            print(f"{hub} -> {neighbors}")
