from dataclasses import dataclass, field
from uuid import UUID, uuid1
from enum import StrEnum, auto

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
    label: str = ""

class Condition(StrEnum):
    NONE = auto()
    PRESENT = auto()
    ABSENT = auto()
    ADD = auto()
    REMOVE = auto()

@dataclass
class LineCondition:
    tag: str
    condition: Condition

@dataclass
class DialogueLine:
    text: str
    condition: LineCondition = None
    event: str = ""

@dataclass
class Node(NextNodeOverride):
    speaker: str = ""
    label: str = ""
    id: str = field(default_factory=id_factory)
    lines: list[DialogueLine] = field(default_factory=list)
    choices: list[DialogueOption] = field(default_factory=list)

    def add_line(self, line: str, tag: str = "", condition: Condition = Condition.NONE):
        match tag:
            case w if tag == "":
                conditionObj = None
            case w:
                conditionObj = LineCondition(tag, condition)


        lineObj = DialogueLine(line,conditionObj)
        print(lineObj)
        self.lines.append(lineObj)

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
        return self.nodes[0].id