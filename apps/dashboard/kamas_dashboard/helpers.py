import attr
from kamas_core.engine.schema import Strategy

INPUT_SOURCES = {"price_close", "price_high", "price_low", "tick_volume"}


def strategy_to_mermaid(strategy: Strategy) -> str:
    """
    Converts a Strategy object to Mermaid flowchart syntax.
    """
    lines: list[str] = ["graph TD"]

    for node in strategy.nodes:
        sections: list[str] = []

        # Header
        sections.append(f"<b>{node.id}</b> <i>({node.model})</i>")

        # Inputs
        if node.inputs:
            inputs = ", ".join(map(str, node.inputs))
            sections.append(f"📥 <b>inputs</b>: {inputs}")

        # Params
        if node.params:
            params = ", ".join(f"{k}={v}" for k, v in node.params.items())
            sections.append(f"⚙️ <b>params</b>: {params}")

        # Critters
        if node.critters:
            sections.append("🧪 <b>critters</b>:")
            for c in node.critters:
                sections.append(
                    f"&nbsp;&nbsp;• {c.op}({node.id}, {c.ref}) → <b>{c.assign}</b>"
                )

        label = "<br/>".join(sections)
        lines.append(f'{node.id}["{label}"]')

    # --- Edges ---
    for node in strategy.nodes:
        for inp in node.inputs:
            if isinstance(inp, str) and inp not in INPUT_SOURCES:
                lines.append(f"{inp} --> {node.id}")

        for critter in node.critters:
            if isinstance(critter.ref, str) and critter.ref not in INPUT_SOURCES:
                lines.append(f"{critter.ref} -.-> {node.id}")

    # --- Outputs ---
    for output_name, node_id in attr.asdict(strategy.output_keys).items():
        lines.append(f"{node_id} --> {output_name}(({output_name.upper()}))")

    return "\n".join(lines)

