import attr
from typing import List, Any, Optional, Dict

@attr.s(auto_attribs=True)
class Node:
    id: str
    model: str
    inputs: List[Any] = attr.Factory(list)
    args: List[Any] = attr.Factory(list)

@attr.s(auto_attribs=True)
class Strategy:
    name: str
    nodes: List[Node] = attr.Factory(list)
    outputs: Optional[Dict[str, str]] = attr.Factory(dict)
