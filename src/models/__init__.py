from dataclasses import dataclass, field

@dataclass
class GraphData:
    id: int = field(init=True)
    title: str = field(init=True)
    labels: list[str] = field(init=True, default=[])
    values: list[int] = field(init=True, default=[])