from typing import List
from dependency_injector import containers, providers
from scriptplayer.core.domain.script import Script
from scriptplayer.infrastructure.repository.json_script_repository import JsonScriptRepository
from scriptplayer.core.repository.script_repository import ScriptRepository

import os

current_path, _ = os.path.split(__file__)
in_path = os.path.join(current_path, os.pardir, "sources")
json_path = os.path.join(current_path, os.pardir, "json")

class MockRepo(ScriptRepository):
    def __init__(self, path: str):
        print(path)

    def get_scripts(self) -> list[Script]:
        return list()
    
    def add(self, script: Script):
        pass

    def get_script(self, id: str) -> Script:
        return None
    
    def get_script_ids(self) -> List[str]:
        return list()

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    script_repository = providers.Singleton(
        JsonScriptRepository,
        path=json_path
    )
