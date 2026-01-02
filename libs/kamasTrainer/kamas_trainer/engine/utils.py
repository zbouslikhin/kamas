from kamas_trainer.engine.context import GraphContext
from kamas_trainer.engine.graph import Graph
import pandas as pd

def run_graph_on_df(graph: Graph, df: pd.DataFrame) -> pd.DataFrame:
    context = GraphContext(
        close=df["close"],
        high=df["high"],
        low=df["low"],
        tick_volume=df["tick_volume"]
    )
    outputs = graph.run(context)
    for k, v in outputs.items():
        df[k] = v
    return df
