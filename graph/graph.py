from Parsing.models import Level, Node, Connection, Zone


class Graph:

    def __init__(self, level: Level) -> None:
        """graph is a visual representation of the map, with all informations
        in level we are able to etablish adjecency between all hubs and get a
        connection_map showing all connections between all hubs"""
        self.nodes: dict[str, Node] = {}
        self.adjacency: dict[str, list[str]] = {}
        self.connection_map: dict[tuple[str, str], Connection] = {}

        self.connections: list[Connection] = level.connections

        self.start_hub = level.start_hub
        self.end_hub = level.end_hub

        self.build_graph(level)

    def build_graph(self, level: Level) -> None:
        """graph is builded, by this method, we can extract a list of all
        adjacency hub to all hubs, and create a connection map"""
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

    def get_travel_time(self, hub_name: str) -> int:
        """all Zone.metadata are represented with a nb of turn value
        to avoid Zome.BLOCKED, travel_time is set to 99999"""
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

    def is_priority_hub(self, hub_name: str) -> bool:
        return (self.nodes[hub_name].metadata.zone == Zone.PRIORITY)
