from abc import ABC, abstractmethod
from scriptplayer.core.domain.script import Script
from dataclasses import asdict
import json
import os
from uuid import UUID

class ScriptWriter(ABC):
    @abstractmethod
    def write(self, script: Script):
        pass

class JsonScriptWriter(ScriptWriter):
    path: str

    def __init__(self, path: str):
         self.path = path

    def write(self, script: Script):
        file_path = os.path.join(self.path, script.file_name+".json")
        with open(file_path, "w", encoding="utf-8") as file:
             json.dump(asdict(script), file, ensure_ascii=False, indent=4, default=uuid_convert)


def uuid_convert(o):
        if isinstance(o, UUID):
            return o.hex