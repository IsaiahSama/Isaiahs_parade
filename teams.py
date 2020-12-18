from dataclasses import dataclass, field

@dataclass()
class Team:
    name: str=""
    guildid: int=0
    leaderid: int=0
    teamid: int=0
    teammates: list=field(default_factory=list)

@dataclass()
class ToAdv:
    teamid: int
    pending: bool
    inadv: list=field(default_factory=list)


