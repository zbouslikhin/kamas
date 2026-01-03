from typing import Any, Dict, Callable

from attr import asdict
import numpy as np

from kamas_core.engine.schema import Strategy, GraphContext, Signal
from kamas_core.critters.registry import MODEL_REGISTRY

NodeValue = np.ndarray | float | int | bool
NodeContext = Dict[str, NodeValue]

def resolve_input(
    inp: Any,
    inputs: dict[str, Any],
    state: dict[str, Any],
) -> Any:
    if not isinstance(inp, str):
        return inp

    if inp in inputs:
        return inputs[inp]

    if inp in state:
        return state[inp]

    raise KeyError(f"Unknown input reference: {inp}")


class Graph:
    def __init__(self, strategy: Strategy, registry: Dict[str, Callable]) -> None:
        self.strategy = strategy
        self.registry = registry
        self.state: NodeContext = {}

    
    def run(self, inputs: GraphContext) -> Dict[str, Any]:
        input_map = asdict(inputs)
        state: Dict[str, np.ndarray] = {}

        for node in self.strategy.nodes:
            result = np.full(
                len(next(iter(input_map.values()))),
                Signal.NOT,
                dtype=int,
            )
            # input can be a number. Example:
            # [[nodes]]
            # id = "volume_ok"
            # model = "gt"
            # inputs = ["vol_ratio", 1.2]
            resolved_inputs = [
            input_map[i] if i in input_map else state[i]
            for i in node.inputs
        ]

            for rule in node.critters:
                fn = self.registry[rule.critter]
                mask = fn(*resolved_inputs, **rule.params)

                result[mask] = Signal[rule.assign]

            state[node.id] = result

        return state


def build_graph(strategy: Strategy) -> Graph:
    return Graph(strategy=strategy, registry=MODEL_REGISTRY)