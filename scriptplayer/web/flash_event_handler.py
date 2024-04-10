from scriptplayer.core.domain.script import DialogueEvent
from scriptplayer.core.services.script_player import ScriptEventHandler
from flask import flash

class FlashEventHandler(ScriptEventHandler):
    def handle(self, event:DialogueEvent):
        flash(f'Event "{event}" received')
        
