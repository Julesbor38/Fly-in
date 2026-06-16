import sys

from Parsing.parsing import Parser
from graph.graph import Graph
from graph.visualizer import visualisation
from graph.simulator import Simulator
from Parsing.models import Drone
from graph.solver import Planner


def main() -> None:
    try:
        parser = Parser(sys.argv[1])

        level = parser.parsing()

        graph = Graph(level)

        planner = Planner(graph)

        paths = planner.generate_all_paths(
            level.nb_drones
        )
        print("Longest path:", max(len(path) for path in paths))
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
        visualisation(
            level,
            simulator
        )
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
