from .models import (
    Node, Connection, NodeMetadata, ConnectionMetadata, Level)
from .validator import (hub_exists, connection_exists, coordinates_exists)
from .metadata_parser import parse_connection_metadata, parse_node_metadata
from .exception import ParsingError


class Parser:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.nb_drones: int | None = None
        self.start_hub: Node | None = None
        self.end_hub: Node | None = None
        self.hubs: dict[str, Node] = {}
        self.connections: list[Connection] = []

    def extract_line(self) -> list[tuple[int, str]]:
        lines: list[tuple[int, str]] = []
        try:
            with open(self.filename, "r") as f:
                for line_number, raw_line in enumerate(f, start=1):
                    line = raw_line.strip()
                    if not line:
                        continue
                    if line.startswith("#"):
                        continue
                    lines.append((line_number, line))
        except Exception as e:
            print(e)
        return (lines)

    def parsing(self) -> Level:
        lines: list[tuple[int, str]] = self.extract_line()
        if not lines:
            raise ParsingError(None, "Empty file")
        first_line: str = lines[0][1]
        if not first_line.startswith("nb_drones"):
            raise ParsingError(lines[0][0], "First line must be'nb_drones'")
        for line_number, line in lines:
            if line.startswith("nb_drones:"):
                self.nb_drones = self.parse_nb_drones(line, line_number)
            elif line.startswith("start_hub:"):
                self.start_hub = self.parse_start_hub(line, line_number)
            elif line.startswith("end_hub:"):
                self.end_hub = self.parse_end_hub(line, line_number)
            elif line.startswith("hub:"):
                self.parse_hub(line, line_number)
            elif line.startswith("connection:"):
                self.parse_connection(line, line_number)
            else:
                raise ParsingError(line_number, "invalid description")
        self.check_data()
        assert self.nb_drones is not None
        assert self.start_hub is not None
        assert self.end_hub is not None
        return Level(
            nb_drones=self.nb_drones,
            start_hub=self.start_hub,
            end_hub=self.end_hub,
            hubs=self.hubs,
            connections=self.connections
        )

    def parse_nb_drones(self, line: str, line_number: int) -> int | None:
        try:
            parts: list[str] = line.split(":")
            if len(parts) != 2:
                raise ParsingError(line_number, "invalid nb_drones format")
            value = int(parts[1].strip())
            if value <= 0:
                raise ParsingError(line_number, "nb_drones must be positive")
            return (value)
        except ParsingError as e:
            print(e)
        return (None)

    def parse_start_hub(self, line: str, line_number: int) -> Node:
        if self.start_hub is not None:
            raise ParsingError(line_number,
                               "There must be exactly one start_hub: zone")
        parts: list[str] = line.split(":")
        if len(parts) != 2:
            raise ParsingError(line_number, "invalid start_hub format")
        content: str = parts[1].strip()
        metadata = NodeMetadata()
        if "[" in content:
            content, metadata_part = content.split("[", 1)
            metadata_part = metadata_part.rstrip("]")
            metadata = parse_node_metadata(metadata_part, line_number)
        info = content.split()
        if len(info) != 3:
            raise ParsingError(line_number,
                               "start_hub must contain name, x, y")
        name = info[0]
        if hub_exists(self.hubs, name):
            raise ParsingError(line_number, f"hub '{name}' already exists")
        try:
            x = int(info[1])
            y = int(info[2])
            if coordinates_exists(self.hubs, x, y):
                raise ParsingError(line_number,
                                   f"coordinates ({x}, {y}) already used")
        except ValueError:
            raise ParsingError(line_number, "x and y must be integer")
        self.start_hub = Node(
            name=name,
            x=x,
            y=y,
            metadata=metadata
        )
        self.hubs[self.start_hub.name] = self.start_hub
        return self.start_hub

    def parse_end_hub(self, line: str, line_number: int) -> Node:
        if self.end_hub is not None:
            raise ParsingError(line_number,
                               "There must be exactly one end_hub: zone")
        parts: list[str] = line.split(":")
        if len(parts) != 2:
            raise ParsingError(line_number, "invalid end_hub format")
        content: str = parts[1].strip()
        metadata = NodeMetadata()
        if "[" in content:
            content, metadata_part = content.split("[", 1)
            metadata_part = metadata_part.rstrip("]")
            metadata = parse_node_metadata(metadata_part, line_number)
        info = content.split()
        if len(info) != 3:
            raise ParsingError(line_number,
                               "end_hub must contain name, x, y")
        name = info[0]
        if hub_exists(self.hubs, name):
            raise ParsingError(line_number, f"hub '{name}' already exists")
        try:
            x = int(info[1])
            y = int(info[2])
            if coordinates_exists(self.hubs, x, y):
                raise ParsingError(line_number,
                                   f"coordinates ({x}, {y}) already used")
        except ValueError:
            raise ParsingError(line_number, "x and y must be integer")
        self.end_hub = Node(
            name=name,
            x=x,
            y=y,
            metadata=metadata
        )
        self.hubs[self.end_hub.name] = self.end_hub
        return self.end_hub

    def check_data(self) -> None:
        if self.nb_drones is None:
            raise ParsingError(None, "Missing nb_drones")
        if self.start_hub is None:
            raise ParsingError(None, "Missig start_hub")
        if self.end_hub is None:
            raise ParsingError(None, "Missing end_hub")
        if self.connections == []:
            raise ParsingError(None, "Missing connection(s)")

    def parse_hub(self, line: str, line_number: int) -> None:
        parts: list[str] = line.split(":", 1)
        if len(parts) != 2:
            raise ParsingError(line_number, "Invalid hub format")
        content: str = parts[1].strip()
        metadata = NodeMetadata()
        if "[" in content:
            content, metadata_part = content.split("[", 1)
            metadata_part = metadata_part.rstrip("]")
            metadata = parse_node_metadata(metadata_part, line_number)
        info = content.split()
        if len(info) != 3:
            raise ParsingError(line_number, "hub must contain name, x, y")
        name: str = info[0]
        if hub_exists(self.hubs, name):
            raise ParsingError(line_number, f"hub '{name}' already exists")
        try:
            x = int(info[1])
            y = int(info[2])
            if coordinates_exists(self.hubs, x, y):
                raise ParsingError(line_number,
                                   f"coordinates ({x}, {y}) already used")
        except ValueError:
            raise ParsingError(line_number, "x and y must be integer")
        node = Node(name=name, x=x, y=y, metadata=metadata)
        self.hubs[node.name] = node

    def parse_connection(self, line: str, line_number: int) -> None:
        parts: list[str] = line.split(":", 1)
        if len(parts) != 2:
            raise ParsingError(line_number, "invalid connection format")
        content: str = parts[1].strip()
        metadata = ConnectionMetadata()
        if "[" in content:
            content, metadata_part = content.split("[", 1)
            metadata_part = metadata_part.rstrip("]")
            metadata = parse_connection_metadata(
                metadata_part, line_number)
        connection = content.split("-")
        if len(connection) != 2:
            raise ParsingError(line_number,
                               "connection: must contain 'source'-'target'")

        source = connection[0].strip()
        if not hub_exists(self.hubs, source):
            raise ParsingError(line_number, f"unknow hub {source}")
        target = connection[1].strip()
        if source == target:
            raise ParsingError(line_number, "a hub cannot connect to himself")
        if not hub_exists(self.hubs, target):
            raise ParsingError(line_number, f"unknow hub {target}")
        if (connection_exists(self.connections, source, target)):
            raise ParsingError(line_number,
                               f"connection {source}-{target} already used")
        self.connections.append(
            Connection(source=source, target=target, metadata=metadata))
