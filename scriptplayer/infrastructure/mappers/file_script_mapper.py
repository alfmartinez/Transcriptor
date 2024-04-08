from scriptplayer.core.domain.script import Script, Node, DialogueOption
import os

class MappingError(Exception):
    pass

class CircularNodeLinkError(MappingError):
    pass

class MissingLabelError(MappingError):
    pass

class FileScriptMapper:
    @staticmethod
    def get_script(path: str) -> Script:
        filename = os.path.splitext(os.path.basename(path))[0]
        script = Script(filename)

        with open(path) as file:
            mapper = LineMapper()
            for line in file:    
                mapper.process_line(script, line.rstrip())
            mapper.post_process_labels()
        return script
    
    
class LineMapper:
    summary_begin: bool = False
    summary_done: bool = False
    title_set: bool = False
    lastNode: Node = None
    labels: dict = dict()
    to_post_process: dict = dict()
    capture_label: str = ""
    
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
                return
            else:
                script.add_summary(line)
                return
            
        lstripped_line = line.lstrip()
        tab_number = (len(line)-len(lstripped_line)) / 4
        if tab_number == 3:
            print("found command "+lstripped_line)
            if lstripped_line.startswith("->"):
                print("found goto")
                _, label = lstripped_line.split()
                self.push_for_post_process(label, self.lastNode)
                return
            if lstripped_line.startswith("*"):
                print("found choice")
                text, label = lstripped_line[2:].split(" -> ")
                option = DialogueOption(text=text)
                self.push_for_post_process(label, option)
                self.lastNode.choices.append(option)
                return
        if tab_number == 2:
            ## New Node
            speaker = line.strip()
            node = Node(speaker=speaker)
            print(node)
            if self.capture_label:
                self.labels[self.capture_label] = node.id
                self.capture_label = ""
            if self.lastNode:
                self.lastNode.nextNodeId = node.id
                if self.lastNode.id == node.id:
                    raise CircularNodeLinkError()
            script.add_node(node)
            self.lastNode = node
            return
        if tab_number == 1:            
            self.lastNode.add_line(line.strip())
            return
        if tab_number == 0:
            self.capture_label, _ = line.split(':')
            return

    def push_for_post_process(self, label: str, item):
        if not label in self.to_post_process:
            self.to_post_process[label] = list()
        self.to_post_process[label].append(item)

    def post_process_labels(self):
        for label in self.to_post_process:
            if not label in self.labels:
                raise MissingLabelError(f'Missing label "{label}"')
            nodeId = self.labels[label]
            for item in self.to_post_process[label]:
                item.setNextNodeId(nodeId)

