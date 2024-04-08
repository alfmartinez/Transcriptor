from typing import List
from dependency_injector import containers, providers
from scriptplayer.core.domain.script import Script
from scriptplayer.infrastructure.repository.json_script_repository import JsonScriptRepository
from scriptplayer.core.repository.script_repository import ScriptRepository
from scriptplayer.core.services.script_player import ScriptPlayer

import os

current_path, _ = os.path.split(__file__)
in_path = os.path.join(current_path, os.pardir, "sources")
json_path = os.path.join(current_path, os.pardir, "json")

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    script_repository = providers.Singleton(
        JsonScriptRepository,
        path=json_path
    )
    script_player = providers.Singleton(
        ScriptPlayer
    )
