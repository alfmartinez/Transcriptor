from flask import Flask, session, request, render_template, url_for, redirect, flash
from flask_bootstrap import Bootstrap5 as Bootstrap
from dependency_injector.wiring import inject, Provide
from scriptplayer.core.domain.state import ScriptState
from scriptplayer.core.repository.script_repository import ScriptRepository
from scriptplayer.core.services.script_player import ScriptPlayer
from scriptplayer.web.flash_event_handler import FlashEventHandler
from .container import Container

container = Container()

app = Flask(__name__)
app.container = container

bootstrap = Bootstrap()
bootstrap.init_app(app)

@app.route("/")
def index():
    return render_template(
        "index.html",
    )

@app.route("/scripts/list")
@inject
def list_scripts(scriptRepository: ScriptRepository = Provide[Container.script_repository]):
    scripts = scriptRepository.get_scripts()
    return render_template(
        "script_list.html",
        scripts = scripts
    )

@app.route("/scripts/<id>")
@inject
def view_script(id: str, scriptRepository: ScriptRepository = Provide[Container.script_repository]):
    script = scriptRepository.get_script(id)
    return render_template(
        "script_view.html",
        script = script
    )

@app.route("/scripts/<id>/play")
@inject
def play_script(id: str, scriptRepository: ScriptRepository = Provide[Container.script_repository], scriptState: ScriptState = Provide[Container.script_state]):
    script = scriptRepository.get_script(id)
    scriptState.reset()
    nodeId = script.get_entrypoint()
    return redirect(url_for('play_node', id=id, nodeId=nodeId, line=0))

@app.route("/scripts/<id>/play/node/<nodeId>/<line>")
@inject
def play_node(
        id: str, nodeId: str, line:int, 
        scriptRepository: ScriptRepository = Provide[Container.script_repository], 
        scriptPlayer: ScriptPlayer = Provide[Container.script_player],
        flashHandler: FlashEventHandler = Provide[Container.flash_handler]
    ):
    scriptPlayer.event_delegate.register(flashHandler.handle)
    script = scriptRepository.get_script(id)    
    choices, scriptLine = scriptPlayer.getScriptLine(script, nodeId, int(line))
    return render_template(
        "script_play.html",
        scriptId=script.id,
        scriptLine = scriptLine,
        choices = choices
    )

container.wire(packages=[__name__])