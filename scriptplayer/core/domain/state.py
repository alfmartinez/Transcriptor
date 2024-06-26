from dataclasses import dataclass, field

from scriptplayer.core.domain.script import Condition, ConditionalItem, TagCondition


@dataclass
class ScriptState:
    tags: list[str] = field(default_factory=list)

    def add_tag(self, tag: str):
        self.tags.append(tag)

    def has_tag(self, tag: str) -> bool:
        return tag in self.tags
    
    def reset(self):
        del self.tags[:]
    
    def check_condition(self, conditionObject: ConditionalItem):
        condition = conditionObject.condition
        if condition == None:
            return True
        tag = condition.tag
        match condition.condition:
            case Condition.ABSENT:
                return not self.has_tag(tag)
            case Condition.PRESENT:
                return self.has_tag(tag)
            case Condition.ADD:
                if tag not in self.tags:
                    self.tags.append(tag)                 
                return True
            case Condition.REMOVE:
                self.tags.remove(tag)
                return True
            
        return True