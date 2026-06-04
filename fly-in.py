import sys
from Parsing.parsing import Parser
from graph.graph import Graph

if __name__ == "__main__":
    try:
        parser = Parser(sys.argv[1])
        level = parser.parsing()
        graph = Graph(level)
        graph.display()
        print(level.nb_drones)
        for hub in level.hubs:
            print(hub)
        for connection in level.connections:
            print(connection)
    except Exception as e:
        print(e)
