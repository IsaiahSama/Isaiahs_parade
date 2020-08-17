from dataclasses import dataclass, field

@dataclass()
class Team:
    name: str
    guildid: int
    leaderid: int
    teamid: int
    teammates: list=field(default_factory=list)

@dataclass()
class ToAdv:
    teamid: int
    pending: bool
    inadv: list=field(default_factory=list)


