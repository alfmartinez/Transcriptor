from dataclasses import dataclass, field
from uuid import UUID, uuid1

ScriptId = str

@dataclass
class Node:
    speaker: str
    id: str = ""
    lines: list[str] = field(default_factory=list)
    nextNodeId: str = ""

    def __init__(self, speaker: str, id: str=uuid1().hex, lines: list[str] = list(), nextNodeId: str=""):
        self.speaker = speaker
        self.id = id
        self.lines = lines
        self.nextNodeId = nextNodeId

    def add_line(self, line: str):
        self.lines.append(line)

    def get_line(self, idx: int):
        last = idx == len(self.lines)-1
        return last, self.lines[idx]


@dataclass
class Script:
    file_name: str
    title: str = ""
    id: str = ""
    summary: list[str] = field(default_factory=list)
    nodes: list[Node] = field(default_factory=list)

    def old__init__(self, file_name: str):
        self.file_name = file_name
        self.id = uuid1().hex
        self.summary = list[str]()
        self.nodes = list[Node]()

    def add_summary(self, summary: str):
        self.summary.append(summary)

    def add_node(self, node: Node):
        self.nodes.append(node)

    def get_node(self, nodeId: str) -> Node:
        for node in self.nodes:
            if node.id == nodeId:
                return node
        return None
     
    def get_entrypoint(self) -> str:
        node = self.nodes[0]
        print(node)
        return self.nodes[0].id