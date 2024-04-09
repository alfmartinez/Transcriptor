from abc import ABC, abstractmethod

from scriptplayer.core.domain.script import Script

class AbstractLineMapper(ABC):
    pass


class AbstractMapperRule(ABC):
    mapper : AbstractLineMapper = None

    def __init__(self, mapper: AbstractLineMapper):
        self.mapper = mapper

    def apply_rule(self, line) -> bool :
        if self.check_condition(line):
            self.do_apply_rule(line)
            return True
        return False

    @abstractmethod
    def check_condition(self, line: str) -> bool :
        pass

    @abstractmethod
    def do_apply_rule(self, line: str):
        pass
    
    @classmethod
    def has_indentation(cls, line: str, indent: int) -> bool:
        lstripped_line = line.lstrip()
        tab_number = (len(line)-len(lstripped_line)) / 4
        return tab_number == indent