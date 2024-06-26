from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID, uuid1
from enum import StrEnum, auto
from dataclass_wizard import JSONFileWizard

ScriptId = str

def id_factory():
    return uuid1().hex

@dataclass
class NextNodeOverride:
    nextNodeId: str = ""
    nextNodeLabel: str = ""
    def setNextNodeId(self, id: str):
        self.nextNodeId = id


class Condition(StrEnum):
    NONE = auto()
    PRESENT = auto()
    ABSENT = auto()
    ADD = auto()
    REMOVE = auto()

@dataclass
class TagCondition:
    tag: str
    condition: Condition

    def __str__(self) -> str:
        return self.condition + " " + self.tag

@dataclass
class ConditionalItem:
    condition: Optional[TagCondition] = None

@dataclass
class DialogueOption(NextNodeOverride, ConditionalItem):
    text: str = ""
    label: str = ""

@dataclass
class DialogueEvent:
    name: str
    args: list = field(default_factory=list)


@dataclass
class DialogueLine(ConditionalItem):
    text: str = ""
    event: Optional[DialogueEvent] = None

@dataclass
class Node(NextNodeOverride):
    speaker: str = ""
    label: str = ""
    id: str = field(default_factory=id_factory)
    lines: list[DialogueLine] = field(default_factory=list)
    choices: list[DialogueOption] = field(default_factory=list)

    def add_line(self, line: DialogueLine):        
        self.lines.append(line)

    def get_line(self, idx: int):
        last = idx == len(self.lines)-1
        return last, self.lines[idx]

    def get_choices(self):
        return self.choices

@dataclass
class Script(JSONFileWizard):
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