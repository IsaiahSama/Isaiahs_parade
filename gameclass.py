from dataclasses import dataclass, field

@dataclass
class wordgame:
    chanid: int
    mode: str
    storywords: list=field(default_factory=list)
    hangword: str=None
    hiddenword: str=None
    trycount: int=0 