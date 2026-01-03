from typing import Any, Callable, Dict

import numpy as np
from attr import asdict

from kamas_core.critters.registry import MODEL_REGISTRY
from kamas_core.engine.schema import GraphContext, Signal, Strategy

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
            # compute node output
            resolved_inputs = [resolve_input(i, input_map, state) for i in node.inputs]

            result = MODEL_REGISTRY[node.model](
                *resolved_inputs, **getattr(node, "params", {})
            )

            # apply critters
            for rule in node.critters:
                fn = MODEL_REGISTRY[rule.op]
                ref_value = resolve_input(rule.ref, input_map, state)
                mask = fn(result, ref_value, **rule.params)
                result[mask] = Signal[rule.assign]

            state[node.id] = result

        return state


def build_graph(strategy: Strategy) -> Graph:
    return Graph(strategy=strategy, registry=MODEL_REGISTRY)
