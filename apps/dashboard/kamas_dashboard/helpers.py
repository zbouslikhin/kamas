from kamas_core.engine.schema import Strategy
import attr


INPUT_SOURCES = {"price_close", "price_high", "price_low", "tick_volume"}

def strategy_to_mermaid(strategy: Strategy) -> str:
    """
    Converts a Strategy object to Mermaid flowchart syntax.
    """
    lines: list[str] = ["graph TD"]

    # --- Nodes ---
    for node in strategy.nodes:
        param_lines = []

        if node.params:
            for k, v in node.params.items():
                param_lines.append(f"{k}={v}")

        label_parts = [
            node.id,
            f"critter: {node.critter}",
            *param_lines,
        ]

        label = "<br/>".join(label_parts)

        lines.append(f'{node.id}["{label}"]')

    # --- Edges ---
    for node in strategy.nodes:
        for inp in node.inputs:
            if isinstance(inp, str) and inp not in INPUT_SOURCES:
                lines.append(f"{inp} --> {node.id}")

    # --- Outputs (buy / sell) ---
    for output_name, node_id in attr.asdict(strategy.output_keys).items():
        lines.append(f"{node_id} --> {output_name}(({output_name.upper()}))")

    return "\n".join(lines)