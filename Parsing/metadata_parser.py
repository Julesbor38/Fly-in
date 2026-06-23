from .models import (
    NodeMetadata,
    ConnectionMetadata,
    Zone
)
from .exception import ParsingError


def parse_node_metadata(
    metadata_str: str,
    line_number: int
) -> NodeMetadata:
    metadata = NodeMetadata()
    """Parse hub's metadata if they are only great
    informations, color, zone and max_drones"""
    if not metadata_str:
        return metadata
    for item in metadata_str.split():
        parts = item.split("=")
        if len(parts) != 2:
            raise ParsingError(
                line_number,
                f"invalid metadata {item}"
            )
        key = parts[0]
        value = parts[1]
        match key:
            case "color":
                metadata.color = value
            case "zone":
                metadata.zone = Zone.get_zone(value, line_number)
            case "max_drones":
                try:
                    metadata.max_drones = int(value)
                except ValueError:
                    raise ParsingError(
                        line_number,
                        "max_drones must be an integer"
                    )
                if metadata.max_drones <= 0:
                    raise ParsingError(
                        line_number,
                        "max_drones must be > 0"
                    )
            case _:
                raise ParsingError(
                    line_number,
                    f"unknown metadata key '{key}'"
                )
    return metadata


def parse_connection_metadata(
    metadata_str: str,
    line_number: int
) -> ConnectionMetadata:
    metadata = ConnectionMetadata()
    """Parse connection's metadata if they are only great
    informations, max_link_capacity"""
    if not metadata_str:
        return metadata
    for item in metadata_str.split(" "):
        parts = item.split("=")
        if len(parts) != 2:
            raise ParsingError(
                line_number,
                f"invalid metadata {item}"
            )
        key = parts[0]
        value = parts[1]
        match key:
            case "max_link_capacity":
                try:
                    metadata.max_link_capacity = int(value)
                except ValueError:
                    raise ParsingError(
                        line_number,
                        "max_link_capacity must be an integer"
                    )
                if metadata.max_link_capacity <= 0:
                    raise ParsingError(
                        line_number,
                        "max_link_capacity must be > 0"
                    )
            case _:
                raise ParsingError(
                    line_number,
                    f"unknown metadata key '{key}'"
                )
    return metadata
