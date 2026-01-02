from typing import Any, Dict, Callable
from kamas_trainer.engine.schema import Strategy
from kamas_trainer.engine.context import GraphContext
from attr import asdict

class Graph:
    def __init__(self, strategy: Strategy, registry: Dict[str, Callable]) -> None:
        self.strategy = strategy
        self.registry = registry
        self.context: Dict[str, Any] = {}

    def run(self, inputs: GraphContext) -> Dict[str, Any]:
        self.context.update(asdict(inputs))
        for node in self.strategy.nodes:
            fn = self.registry[node.model]
            args = [(self.context[inp] if isinstance(inp, str) else inp) for inp in node.inputs]
            args += node.args
            self.context[node.id] = fn(*args)
        return self.context
