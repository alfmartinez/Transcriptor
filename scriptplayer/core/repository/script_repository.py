from abc import ABC, abstractmethod
from typing import List
from scriptplayer.core.domain.script import Script

class ScriptRepository(ABC):
    @abstractmethod
    def get_script_ids(self) -> List[str]:
        pass

    @abstractmethod
    def get_script(self, id: str) -> Script:
        pass

    @abstractmethod
    def get_scripts(self) -> list[Script]:
        pass

    @abstractmethod
    def add(self, script: Script):
        pass