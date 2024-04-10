from abc import ABC, abstractmethod
from collections import namedtuple
from scriptplayer.core.domain.script import Script, ScriptId, Node
from dataclasses import make_dataclass
import json
import os
from uuid import UUID

class ScriptReader(ABC):
    @abstractmethod
    def read(self, id: ScriptId) -> Script:
        pass
    @abstractmethod
    def readIndexes(self) -> list[ScriptId]:
        pass
    @abstractmethod
    def read_all(self) -> dict[ScriptId, Script]:
        pass

def ScriptDecoder(scriptDict):
    return namedtuple('Script', scriptDict.keys())(*scriptDict.values())


class JsonScriptReader(ScriptReader):
    path: str
    paths: dict = dict()

    def __init__(self, path: str):
         self.path = path

    def readIndexes(self) -> list[ScriptId]:
        return self.paths.keys()

    def read_all(self) -> dict[str, Script]:
        self.paths = dict()
        scripts = dict()
        it = os.scandir(self.path)
        for entry in it:
            if entry.is_file() and entry.name.endswith(".json"):            
                script = Script.from_json_file(entry.path)
                scripts[script.id] = script
                   

        return scripts

    def read(self, id: ScriptId) -> Script:
        if id in self.paths:
            script = Script.from_json_file(self.paths[id])
            return script
        
        return None

    def update(self):
        self.paths = dict()
        it = os.scandir(self.path)
        for entry in it:
            if entry.is_file() and entry.name.endswith(".json"):
                with open(entry.path, "r") as f:
                    data = json.load(f)
                    uuid = data["id"]
                    self.paths[uuid]=entry.path
        
                    

        