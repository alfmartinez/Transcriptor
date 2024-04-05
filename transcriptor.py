from application.services.load_scripts import LoadScripts
from infrastructure.repository.file_script_repository import FileScriptRepository
from infrastructure.repository.json_script_repository import JsonScriptRepository
import os

current_path, _ = os.path.split(__file__)
in_path = os.path.join(current_path, "sources")
out_path = os.path.join(current_path, "json")

scriptRepository = FileScriptRepository(in_path, ".txt")

jsonRepository = JsonScriptRepository(out_path)
service = LoadScripts(scriptRepository)

scripts = service.load()

for script in scripts:
    jsonRepository.add(script)
