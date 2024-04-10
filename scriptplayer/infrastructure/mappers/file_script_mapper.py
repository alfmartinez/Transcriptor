from dataclasses import dataclass, field
from scriptplayer.core.domain.script import DialogueLine, Script, Node, DialogueOption
import os

from scriptplayer.infrastructure.mappers.abstract_classes import AbstractLineMapper, AbstractMapperRule
from scriptplayer.infrastructure.mappers.exceptions import LineDoesntMatchAnyRuleError, MissingLabelError
from scriptplayer.infrastructure.mappers.rules import CallDelegateRule, CaptureLabelRule, ChoiceRule, ConditionalChoiceRule, EmptyLineRule, GotoCommandRule, NewLineRule, NewLineWithConditionRule, NewNodeRule, SummaryRule, TitleRule

rules_list = [
    EmptyLineRule,
    TitleRule,
    SummaryRule,
    GotoCommandRule,
    ConditionalChoiceRule,
    ChoiceRule,
    NewNodeRule,
    NewLineWithConditionRule,
    NewLineRule,
    CaptureLabelRule,
    CallDelegateRule
]

class FileScriptMapper:
    @staticmethod
    def get_script(path: str) -> Script:
        filename = os.path.splitext(os.path.basename(path))[0]
        script = Script(filename)
        mapper = LineMapper(script)

        with open(path) as file:
            for line in file:    
                mapper.process_line(line.rstrip())
            mapper.post_process_labels()
        
        return script
    
@dataclass    
class LineMapper(AbstractLineMapper):
    script: Script
    lastNode: Node = None
    lastLine: DialogueLine = None
    labels: dict = field(default_factory=dict)
    to_post_process: dict = field(default_factory=dict)
    capture_label: str = ""

    rules: list[AbstractMapperRule] = field(default_factory=list)

    def __init__(self, script: Script) -> None:
        self.script = script
        self.rules = list()
        self.to_post_process = dict()
        self.labels = dict()
        for rule in rules_list:
            self.rules.append(rule(self))
    
    def process_line(self, line: str):
        
        for rule in self.rules:
            if rule.apply_rule(line):
                return
        
        raise LineDoesntMatchAnyRuleError(line)

    def push_for_post_process(self, label: str, item):
        if not label in self.to_post_process:
            self.to_post_process[label] = list()
        self.to_post_process[label].append(item)

    def post_process_labels(self):
        for label in self.to_post_process:
            if not label in self.labels:
                raise MissingLabelError(f'Missing label "{label}"')
            nodeId = self.labels[label]
            for item in self.to_post_process[label]:
                item.setNextNodeId(nodeId)

