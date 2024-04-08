from scriptplayer.core.services.load_scripts import LoadScripts
from scriptplayer.infrastructure.repository.file_script_repository import FileScriptRepository
from scriptplayer.infrastructure.repository.json_script_repository import JsonScriptRepository
import os

current_path, _ = os.path.split(__file__)
in_path = os.path.join(current_path, "scriptplayer","sources")
out_path = os.path.join(current_path, "scriptplayer", "json")

scriptRepository = FileScriptRepository(in_path, ".txt")

jsonRepository = JsonScriptRepository(out_path, False)
service = LoadScripts(scriptRepository)

scripts = service.load()

for script in scripts:
    jsonRepository.add(script)
