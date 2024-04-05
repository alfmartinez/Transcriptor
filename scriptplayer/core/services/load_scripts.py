from scriptplayer.core.repository.script_repository import ScriptRepository
import json
from dataclasses import asdict
from uuid import UUID

class LoadScripts:
    scriptRepository: ScriptRepository

    def __init__(self, repository : ScriptRepository) -> None:
        self.scriptRepository = repository
        
    def load(self):
        scriptIds = self.scriptRepository.get_script_ids()

        for scriptId in scriptIds:
            script = self.scriptRepository.get_script(scriptId)
            yield script


