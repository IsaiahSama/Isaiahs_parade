from dataclasses import dataclass, field

@dataclass()
class Team:
    teamname: str
    guildid: int
    leaderid: int
    teamid: int
    teammates: list=field(default_factory=list)

