from typing import List
import os
from uuid import uuid1
from scriptplayer.core.domain.script import Script
from scriptplayer.core.repository.script_repository import ScriptRepository
from scriptplayer.infrastructure.mappers.file_script_mapper import FileScriptMapper

class FileScriptRepository(ScriptRepository):
    
    scriptIds : List[str] = list()
    paths : dict = dict()
    path : str
    suffix: str

    def __init__(self, path : str, suffix: str):
        self.path = path
        self.suffix = suffix
        self._init_data()

    def _init_data(self):
        it = os.scandir(self.path)
        for entry in it:
            if entry.is_file() and entry.name.endswith(self.suffix):
                id = uuid1()
                self.paths[id] = entry.path
                self.scriptIds.append(id)
                pass


    def get_script_ids(self) -> List[str]:
        return self.scriptIds 

    def get_script(self, id: str) -> Script:
        path = self.paths[id]
        return FileScriptMapper.get_script(path)

