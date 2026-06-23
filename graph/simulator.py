from graph.graph import Graph
from Parsing.models import Drone, Node


class Simulator:
    def __init__(self, graph: Graph, drones: list[Drone]) -> None:
        """simulator use onformations extracted from graph
        this representation add occupation for hub and connection
        we also set the start_hub occupancy to len(nb_drones0)"""
        self.graph: Graph = graph
        self.drones: list[Drone] = drones
        self.hub_occupancy: dict[str, int] = {}
        self.connection_occupancy: dict[tuple[str, str], int] = {}
        self.hub_occupancy[self.graph.start_hub.name] = len(self.drones)

    def can_enter_hub(self, hub_name: str) -> bool:
        """Check if new_hub occupancy is least than max or if hub is end_hub"""
        hub: Node = self.graph.nodes[hub_name]
        hub: Node = self.graph.nodes[hub_name]
        occupancy = self.hub_occupancy.get(hub_name, 0)
        return occupancy < hub.metadata.max_drones

    def can_use_connection(self, source: str, target: str) -> bool:
        """Check if connection occupancy is least than max"""
        connection = self.graph.connection_map[(source, target)]
        occupancy = self.connection_occupancy.get((source, target), 0)
        return occupancy < connection.metadata.max_link_capacity

    def move_drone(self, drone: Drone) -> bool:
        """This methode adjust occupancy for connections and hubs,
        we also adjust drones data for every turn"""
        if drone.wait_turns > 0:
            drone.wait_turns -= 1
            if drone.wait_turns == 0:
                if (drone.pending_hub is not
                   None and not self.can_enter_hub(drone.pending_hub)):
                    drone.wait_turns = 1
                    return False
                assert drone.pending_hub is not None
                self.hub_occupancy[drone.pending_hub] = (
                    self.hub_occupancy.get(drone.pending_hub, 0) + 1)
                drone.current_hub = drone.pending_hub
                drone.path_index += 1
                drone.current_connection = None
                drone.pending_hub = None
                return True
            return False
        if drone.path_index >= len(drone.path) - 1:
            return False
        current_hub = drone.current_hub
        next_hub = drone.path[drone.path_index + 1]
        if current_hub == next_hub:
            drone.path_index += 1
            return True
        cost = self.graph.get_travel_time(next_hub)
        if cost > 1:
            if not self.can_use_connection(current_hub, next_hub):
                return False
            self.connection_occupancy[(current_hub, next_hub)] = (
                self.connection_occupancy.get((current_hub, next_hub), 0) + 1
            )
            self.hub_occupancy[current_hub] -= 1
            drone.current_connection = (current_hub, next_hub)
            drone.pending_hub = next_hub
            drone.wait_turns = cost - 1
            return False
        if not self.can_enter_hub(next_hub) and next_hub:
            return False
        if not self.can_use_connection(current_hub, next_hub):
            return False
        self.connection_occupancy[(current_hub, next_hub)] = (
            self.connection_occupancy.get((current_hub, next_hub), 0) + 1)
        self.hub_occupancy[current_hub] -= 1
        self.hub_occupancy[next_hub] = self.hub_occupancy.get(next_hub, 0) + 1
        drone.path_index += 1
        drone.current_hub = next_hub
        return True

    def step(self) -> None:
        self.connection_occupancy.clear()

        for drone in self.drones:
            self.move_drone(drone)
