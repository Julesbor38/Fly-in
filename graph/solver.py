from graph.graph import Graph
from Parsing.models import Zone
from Parsing.exception import MapError


class Planner:
    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        self.hub_reservations: dict[tuple[str, int], int] = {}
        self.connection_reservations: dict[tuple[str, str,  int], int] = {}

    def generate_all_paths(self, nb_drones: int) -> list[list[str]]:
        paths: list[list[str]] = []
        for _ in range(nb_drones):
            path = self.shortest_path_with_reservations(
                self.graph.start_hub.name, self.graph.end_hub.name)
            self.reserve_path(path)
            paths.append(path)
        return paths

    def shortest_path_with_reservations(self, start: str,
                                        end: str) -> list[str]:
        from heapq import heappush, heappop

        start_state = (start, 0)
        distance: dict[tuple[str, int], float] = {start_state: 0}
        parents: dict[tuple[str, int], tuple[str, int] | None] = {
            start_state: None}
        heap: list[tuple[float, int, str, int]] = []
        heappush(heap, (0, 0,  start, 0))
        end_state: tuple[str, int] | None = None
        while heap:
            current_cost, current_priority, current, current_turn = (
                heappop(heap))
            current_state = (current, current_turn)
            if (current_cost > distance[current_state]):
                continue
            if current == end:
                end_state = current_state
                break
            wait_turn = current_turn + 1
            wait_state = (current, wait_turn)
            wait_cost = current_cost + 1
            if (wait_state not in distance
               or wait_cost < distance[wait_state]):
                distance[wait_state] = wait_cost
                parents[wait_state] = current_state
                heappush(heap, (wait_cost, current_priority,
                                current, wait_turn))

            for neighbor in self.graph.adjacency[current]:
                if (self.graph.nodes[neighbor].metadata.zone == Zone.BLOCKED):
                    continue
                arrival_turn = (current_turn +
                                self.graph.get_travel_time(neighbor))
                if not self.can_use_hub(neighbor, arrival_turn):
                    continue
                if not self.can_use_connection(
                   current, neighbor, current_turn):
                    continue
                new_priority = current_priority
                if self.graph.is_priority_hub(neighbor):
                    new_priority -= 1
                new_cost = (current_cost +
                            self.graph.get_travel_time(neighbor))
                neighbor_state = (neighbor, arrival_turn)
                if (neighbor_state not in distance
                   or new_cost < distance[neighbor_state]):
                    distance[neighbor_state] = new_cost
                    parents[neighbor_state] = current_state
                    heappush(heap, (new_cost, new_priority,
                                    neighbor, arrival_turn))
        if end_state is None:
            raise MapError("Couldn't find Exit point from start")
        path: list[str] = []
        current_state = end_state
        while current_state is not None:
            node_name, _ = current_state
            path.append(node_name)
            current_state = (parents[current_state])
        return path[::-1]

    def reserve_path(self, path: list[str]) -> None:

        current_turn = 0

        self.hub_reservations[(path[0], current_turn)] = (
            self.hub_reservations.get((path[0], current_turn), 0) + 1
        )

        for i in range(len(path) - 1):

            source = path[i]
            target = path[i + 1]

            self.connection_reservations[
                (source, target, current_turn)
            ] = (
                self.connection_reservations.get(
                    (source, target, current_turn),
                    0
                ) + 1
            )

            current_turn += self.graph.get_travel_time(target)

            self.hub_reservations[
                (target, current_turn)
            ] = (
                self.hub_reservations.get(
                    (target, current_turn),
                    0
                ) + 1
            )

    def can_use_hub(self, hub_name: str, turn: int) -> bool:
        if hub_name == self.graph.end_hub.name:
            return True
        hub = self.graph.nodes[hub_name]
        occupancy = self.hub_reservations.get((hub_name, turn), 0)
        return occupancy < hub.metadata.max_drones

    def can_use_connection(self, source: str, target: str, turn: int) -> bool:
        connection = self.graph.connection_map[(source, target)]
        occupancy = self.connection_reservations.get((source, target, turn), 0)
        return occupancy < connection.metadata.max_link_capacity
