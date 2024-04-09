from scriptplayer.core.domain.script import DialogueOption, Node
from scriptplayer.infrastructure.mappers.abstract_classes import AbstractMapperRule
from scriptplayer.infrastructure.mappers.exceptions import CircularNodeLinkError

class EmptyLineRule(AbstractMapperRule):
    def check_condition(self, line: str) -> bool:
        return line.strip() == ""
    
    def do_apply_rule(self, line: str):
        return 

class TitleRule(AbstractMapperRule):
    title_set: bool = False

    def check_condition(self, line: str) -> bool:
        return not self.title_set
    
    def do_apply_rule(self, line: str):
        self.mapper.script.title = line.strip()
        self.title_set = True

class SummaryRule(AbstractMapperRule):
    summary_begin: bool = False
    summary_done: bool = False
    
    def check_condition(self, line: str) -> bool:
        return not self.summary_done
    
    def do_apply_rule(self, line: str):
        if line.endswith("---"):
            if not self.summary_begin:
                self.summary_begin = True
                return 
            else:
                self.summary_done = True
                return
        if self.summary_begin:
            self.mapper.script.add_summary(line.strip())
            return
        
class GotoCommandRule(AbstractMapperRule):
    def check_condition(self, line: str) -> bool:
        return GotoCommandRule.has_indentation(line, 3) and line.lstrip().startswith("->")
    
    def do_apply_rule(self, line: str):
        _, label = line.lstrip().split()
        self.mapper.push_for_post_process(label, self.mapper.lastNode)
            
        
class ChoiceRule(AbstractMapperRule):
    def check_condition(self, line: str) -> bool:
        return ChoiceRule.has_indentation(line, 3) and line.lstrip().startswith("*")
    
    def do_apply_rule(self, line: str):
        text, label = line.lstrip()[2:].split(" -> ")
        option = DialogueOption(text=text)
        self.mapper.push_for_post_process(label, option)
        self.mapper.lastNode.choices.append(option)

class NewNodeRule(AbstractMapperRule):
    def check_condition(self, line: str) -> bool:
        return NewNodeRule.has_indentation(line, 2)
    
    def do_apply_rule(self, line: str):
        speaker = line.strip()
        node = Node(speaker=speaker)
        if self.mapper.capture_label:
            self.mapper.labels[self.mapper.capture_label] = node.id
            self.mapper.capture_label = ""
        if self.mapper.lastNode:
            self.mapper.lastNode.nextNodeId = node.id
            if self.mapper.lastNode.id == node.id:
                raise CircularNodeLinkError()
        self.mapper.script.add_node(node)
        self.mapper.lastNode = node
        
class NewLineRule(AbstractMapperRule):
    def check_condition(self, line: str) -> bool:
        return NewLineRule.has_indentation(line, 1)
    
    def do_apply_rule(self, line: str):
        self.mapper.lastNode.add_line(line.strip())

class CaptureLabelRule(AbstractMapperRule):
    def check_condition(self, line: str) -> bool:
        return CaptureLabelRule.has_indentation(line, 0) and (':' in line)
    
    def do_apply_rule(self, line: str):
        self.mapper.capture_label, _ = line.split(":")