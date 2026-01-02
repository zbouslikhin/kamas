from kamas_trainer.engine.graph import Graph
from kamas_trainer.critters.registry import MODEL_REGISTRY
from kamas_trainer.engine.schema import Strategy

def build_graph(strategy: Strategy) -> Graph:
    return Graph(strategy=strategy, registry=MODEL_REGISTRY)
