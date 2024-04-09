from dataclasses import dataclass, field


@dataclass
class ScriptState:
    tags: list[str] = field(default_factory=list)

    def add_tag(self, tag: str):
        self.tags.append(tag)

    def has_tag(self, tag: str) -> bool:
        return tag in self.tags