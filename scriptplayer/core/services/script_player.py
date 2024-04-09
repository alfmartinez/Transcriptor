from scriptplayer.core.domain.script import Script
from dataclasses import dataclass

from scriptplayer.core.domain.state import ScriptState

@dataclass
class ScriptIndex:
    nodeId: str
    lineId: int
    end: bool

@dataclass
class ScriptLine:
    speaker: str
    line: str
    next: ScriptIndex

class ScriptPlayer:

    state: ScriptState

    def __init__(self, state: ScriptState) -> None:
        self.state = state
    
    def getScriptLine(self, script: Script, nodeId, lineId) -> ScriptLine:
        node = script.get_node(nodeId=nodeId)
        if node:
            last, line = node.get_line(lineId)
            choices = list()
            if last:                
                choices = node.get_choices()
                if node.nextNodeId:
                    next = ScriptIndex(node.nextNodeId, 0, False)
                else:
                    next = ScriptIndex("", 0, True)
            else:
                next = ScriptIndex(nodeId, lineId+1, False)            
            return choices, ScriptLine(speaker=node.speaker, line=line, next=next)
