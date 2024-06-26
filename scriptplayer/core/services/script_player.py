from abc import ABC, abstractmethod
from typing import Callable
from scriptplayer.core.domain.script import DialogueEvent, DialogueLine, Script
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


class ScriptEventHandler(ABC):
    @abstractmethod
    def handle(self, event:DialogueEvent):
        pass

EventCallback = Callable[[DialogueEvent], None]


class MulticastScriptEventHandler(ScriptEventHandler):
    callbacks: list[EventCallback] = list()

    def register(self, callback: EventCallback):
        if not callback in self.callbacks:
            self.callbacks.append(callback)

    def handle(self, event: DialogueEvent):
        for callback in self.callbacks:
            callback(event)

class ScriptPlayer:

    state: ScriptState
    event_delegate: ScriptEventHandler

    def __init__(self, state: ScriptState, event_delegate: ScriptEventHandler) -> None:
        self.state = state
        self.event_delegate = event_delegate
    
    def getScriptLine(self, script: Script, nodeId, lineId) -> ScriptLine:
        node, line, next, last = self.getLine(script, nodeId, lineId)
        choices = list()
        if last:                
            choices = [choice for choice in node.get_choices() if self.state.check_condition(choice)]

        if line.event:
            self.event_delegate.handle(line.event)

        return choices, ScriptLine(speaker=node.speaker, line=line.text, next=next)
        
    def getLine(self, script: Script, nodeId, lineId) -> DialogueLine :
        node = script.get_node(nodeId)
        while True:
            try:
                last,line = node.get_line(lineId)
                if not line.condition or self.state.check_condition(line):
                    break
                lineId+=1
            except IndexError:
                nodeId = node.nextNodeId
                lineId = 0

        if last:                
            choices = node.get_choices()
            if node.nextNodeId:
                next = ScriptIndex(node.nextNodeId, 0, False)
            else:
                next = ScriptIndex("", 0, True)
        else:
            next = ScriptIndex(nodeId, lineId+1, False) 

        return node, line, next, last

