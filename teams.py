from dataclasses import dataclass, field

@dataclass()
class Team:
    name: str
    guildid: int
    leaderid: int
    teamid: int
    teammates: list=field(default_factory=list)

