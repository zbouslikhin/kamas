import json
from pathlib import Path
import attr
import tomllib

from kamas_trainer.engine.schema import Node, Strategy


def load_strategy(path: str, default_format: str = "toml") -> Strategy:
    """
    Load strategy from TOML by default.
    Supports JSON, YAML if suffix matches.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)

    suffix = path.suffix.lower()
    fmt = default_format

    # Override format by suffix
    if suffix in (".json", ".yml", ".yaml", ".toml"):
        fmt = suffix[1:]  # remove dot

    # Load
    if fmt == "json":
        with open(path, "r") as f:
            data = json.load(f)
    elif fmt == "toml":
        if tomllib is None:
            raise RuntimeError("tomllib/tomli required for TOML strategies")
        with open(path, "rb") as f:
            data = tomllib.load(f)
    else:
        raise ValueError(f"Unsupported format: {fmt}")

    # Convert nodes to Node instances
    nodes = [Node(**node) for node in data.get("nodes", [])]
    outputs = data.get("outputs", {})

    return Strategy(name=data["name"], nodes=nodes, outputs=outputs)
