from Parsing.parsing import Parser
from graph.graph import Graph
from graph.visualizer import visualisation
from graph.simulator import Simulator
from Parsing.models import Drone
from graph.solver import Planner
from graph.menu import map_selection


def main() -> None:
    while True:
        try:
            selected_map = map_selection()
        except KeyboardInterrupt:
            print("Warning, please interrupt program properly")
            break
        try:

            parser = Parser(selected_map)

            level = parser.parsing()

            graph = Graph(level)

            planner = Planner(graph)

            paths = planner.generate_all_paths(
                level.nb_drones
            )

            drones = [
                Drone(
                    id=i + 1,
                    current_hub=paths[i][0],
                    path=paths[i]
                )
                for i in range(level.nb_drones)
            ]

            simulator = Simulator(
                graph,
                drones
            )
        except Exception as e:
            print(e)
            continue

        action = visualisation(
            level,
            simulator
        )

        if action == "menu":
            continue

        break


if __name__ == "__main__":
    main()
