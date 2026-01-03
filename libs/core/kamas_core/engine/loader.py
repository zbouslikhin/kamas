from pathlib import Path
import tomllib

from kamas_core.engine.schema import (
    Strategy,
    StrategyOutputKeys,
    Node,
    CritterRule,
)
from kamas_core.engine.schema import Signal


MONOREPO_ROOT = Path(__file__).parents[4]
STRATEGIES_DIR = MONOREPO_ROOT / "strategies"


# ----------------------------
# file loading
# ----------------------------

def load_strategy_file(name: str) -> dict:
    path = STRATEGIES_DIR / f"{name}.toml"
    if not path.exists():
        raise FileNotFoundError(f"Strategy file not found: {path}")

    with open(path, "rb") as f:
        return tomllib.load(f)


# ----------------------------
# parsing helpers
# ----------------------------

def parse_outputs(data: dict) -> StrategyOutputKeys:
    return StrategyOutputKeys(
        buy=data["outputs"]["buy"],
    )


def parse_critter_rule(rule: dict) -> CritterRule:
    try:
        assign = Signal[rule["assign"]]
    except KeyError:
        raise ValueError(f"Invalid Signal '{rule['assign']}'")

    return CritterRule(
        critter=rule["critter"],
        assign=assign,
        params=rule.get("params", {}),
    )


def parse_node(node_data: dict) -> Node:
    critters = [
        parse_critter_rule(rule)
        for rule in node_data.get("critters", [])
    ]

    if not critters:
        raise ValueError(f"Node '{node_data['id']}' has no critters")

    return Node(
        id=node_data["id"],
        inputs=node_data.get("inputs", []),
        critters=critters,
    )


def load_strategy(name: str) -> Strategy:
    data = load_strategy_file(name)

    nodes = [parse_node(n) for n in data["nodes"]]
    outputs = parse_outputs(data)

    return Strategy(
        name=data["name"],
        nodes=nodes,
        output_keys=outputs,
    )
