from scriptplayer.core.domain.script import Script, Node
import os

class FileScriptMapper:
    @staticmethod
    def get_script(path: str) -> Script:
        mapper = LineMapper()
        filename = os.path.splitext(os.path.basename(path))[0]
        script = Script(filename)

        with open(path) as file:
            for line in file:    
                mapper.process_line(script, line.rstrip())
        
        return script
    
    
class LineMapper:
    summary_begin: bool = False
    summary_done: bool = False
    title_set: bool = False
    lastNode: Node = None
    
    def process_line(self, script: Script, line: str):

        if line.strip()=="":
            return
        
        if not self.title_set:
            script.title = line.strip()
            self.title_set = True
            return

        if not self.summary_begin:
            if line.endswith("---"):
                self.summary_begin = True
                return

        if not self.summary_done :
            if line.endswith('---'):
                self.summary_done = True
                print("End summary")
                return
            else:
                script.add_summary(line)
                print("added to summary : "+line)
                return
            
        lstripped_line = line.lstrip()
        tab_number = (len(line)-len(lstripped_line)) / 4
        if tab_number == 2:
            ## New Node
            speaker = line.strip()
            node = Node(speaker)
            if self.lastNode:
                self.lastNode.nextNodeId = node.id
            script.add_node(node)
            self.lastNode = node
        if tab_number == 1:
            self.lastNode.add_line(line.strip())


