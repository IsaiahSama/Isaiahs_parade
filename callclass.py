from dataclasses import dataclass

@dataclass
class CallClass:
    guildid: int
    guildname: str
    chan1id: int
    pending: bool=False
    incall: bool=False
    chan2id: int=None 