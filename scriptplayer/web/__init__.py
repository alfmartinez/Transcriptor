from flask import Flask,request, render_template
from flask_bootstrap import Bootstrap5 as Bootstrap
from dependency_injector.wiring import inject, Provide
from scriptplayer.core.repository.script_repository import ScriptRepository
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
    print(scripts)
    return render_template(
        "script_list.html",
        scripts = scripts
    )


container.wire(packages=[__name__])