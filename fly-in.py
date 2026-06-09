import sys

from Parsing.parsing import Parser
from graph.graph import Graph
from graph.visualizer import visualisation
# from graph.visualizer import GraphVisualizer


def main() -> None:

    parser = Parser(sys.argv[1])

    level = parser.parsing()

    graph = Graph(level)

    graph.display()

    visualisation(level)


if __name__ == "__main__":
    main()