from dataclasses import dataclass, field

@dataclass(init=True)
class GraphData:
    id: int
    title: str
    description: str
    graph_type: str = 'bar'
    labels: list = field(default_factory=list)
    data: list = field(default_factory=list)

    def to_json(self):
        return {
        'title': self.title,
        'graph_type': self.type,
        'labels': self.labels,
        'data': self.data,
        'description': self.description,
        'id': self.id
    }
