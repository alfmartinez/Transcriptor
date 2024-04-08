from dataclasses import dataclass, field
from uuid import UUID, uuid1

ScriptId = str

def id_factory():
    return uuid1().hex

@dataclass
class NextNodeOverride:
    nextNodeId: str = ""
    def setNextNodeId(self, id: str):
        self.nextNodeId = id


@dataclass
class DialogueOption(NextNodeOverride):
    text: str = ""

@dataclass
class Node(NextNodeOverride):
    speaker: str = ""
    id: str = field(default_factory=id_factory)
    lines: list[str] = field(default_factory=list)
    choices: list[DialogueOption] = field(default_factory=list)

    def add_line(self, line: str):
        self.lines.append(line)

    def get_line(self, idx: int):
        last = idx == len(self.lines)-1
        return last, self.lines[idx]

    def get_choices(self):
        return self.choices

@dataclass
class Script:
    file_name: str = ""
    title: str = ""
    id: str = field(default_factory=id_factory)
    summary: list[str] = field(default_factory=list)
    nodes: list[Node] = field(default_factory=list)   

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