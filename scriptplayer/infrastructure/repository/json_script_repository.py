from typing import List
import os
from uuid import uuid1
from scriptplayer.core.domain.script import Script, ScriptId
from scriptplayer.core.repository.script_repository import ScriptRepository
from scriptplayer.infrastructure.json.script_writer import JsonScriptWriter
from scriptplayer.infrastructure.json.script_reader import JsonScriptReader


class JsonScriptRepository(ScriptRepository):
    
    scriptIds : List[ScriptId] = list()
    scripts : dict = dict()
    reader: JsonScriptReader
    writer: JsonScriptWriter

    def __init__(self, path: str):        
        self.writer = JsonScriptWriter(path)
        self.reader = JsonScriptReader(path)
        self._init_data()
    
    def _init_data(self):
        self.scripts = self.reader.read_all()

    def add(self, script: Script):
        self.scripts[script.id] = script
        self.scriptIds.append(script.id)
        print(script)
        self.writer.write(script)
        self.reader.update()
        self.reader.read(script.id)

    def get_script_ids(self) -> List[ScriptId]:
        if len(self.scriptIds) == 0:
            self.scriptIds = self.reader.readIndexes() 
        return self.scriptIds 

    def get_script(self, id: ScriptId) -> Script:
        if self.scripts[id]:
            return self.scripts[id]
        else:
            script = self.reader.read(id)
            if script:
                self.scripts[script.id] = script
                self.scriptIds.append(script.id)
                return script
            return None
                        
    def get_scripts(self) -> List[Script]:
        return [script for script in self.scripts]
