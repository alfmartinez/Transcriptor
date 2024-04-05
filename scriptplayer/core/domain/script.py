from dataclasses import dataclass, field
from uuid import UUID, uuid1

ScriptId = str

@dataclass
class Node:
    speaker: str
    id: str = ""
    lines: list[str] = field(default_factory=list)
    nextNodeId: str = None

    def __init__(self, speaker: str):
        self.speaker = speaker
        self.id = uuid1().hex
        self.lines = list[str]()

    def add_line(self, line: str):
        self.lines.append(line)


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