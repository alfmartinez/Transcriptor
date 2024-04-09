from abc import ABC, abstractmethod
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
                with open(entry.path, "r") as f:
                    data = json.load(f)
                    uuid = data["id"]
                    self.paths[uuid]=entry.path
                    script = Script(**data)
                    scripts[data["id"]]=script
                    script.nodes = list()
                    for node in data["nodes"]:
                        nodeObj = Node(**node)
                        script.add_node(nodeObj)

        return scripts

    def read(self, id: ScriptId) -> Script:
        if id in self.paths:
            with open(self.paths[id], "r") as f:
                data = json.load(f)
                uuid = data["id"]
                data["id"]=uuid
                script = Script(**data)
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
        
                    

        