import tomllib
from pathlib import Path

from kamas_core.engine.schema import (
    CritterRule,
    Node,
    Signal,
    Strategy,
    StrategyOutputKeys,
)

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
    assign = rule.get("assign")
    if assign not in Signal.__dict__:
        raise ValueError(f"Invalid Signal '{assign}'")

    return CritterRule(
        id=rule["id"],
        op=rule["op"],  # operation name
        ref=rule["ref"],  # constant, input, or node reference
        assign=assign,
        params=rule.get("params", {}),
    )


def parse_node(node_data: dict) -> Node:
    critters = [parse_critter_rule(rule) for rule in node_data.get("critters", [])]

    return Node(
        id=node_data["id"],
        model=node_data["model"],
        inputs=node_data.get("inputs", []),
        critters=critters,
        params=node_data.get("params", {}),
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
