from aiosqlite import Connection
from random import sample
from string import hexdigits

digits = list(hexdigits)

def generate_id() -> str:
    return sample(digits, k=7)


class Team:
    def __init__(self, name, guildid, ownerid, leaderid, teamid, teammates) -> None:
        self.name = name 
        self.guildid = guildid
        self.ownerid = ownerid
        self.leaderid = leaderid
        self.teamid = generate_id()
        # Teammates is a list of ids
        self.teammates = [int(mate) for mate in teammates.split(", ")] if isinstance(teammates, str) and teammates else teammates

class Database:

    def __init__(self) -> None:
        pass

    async def setup(self, db:Connection):
        """Function which accepts a database connection, and sets up the Team Database"""

        await db.execute("""CREATE TABLE IF NOT EXISTS TeamTable(
            ID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            NAME TEXT, 
            GUILD_ID INTEGER,
            LEADER_ID INTEGER,
            TEAM_ID INTEGER,
            TEAMMATES TEXT);""")

        await db.commit()

    async def query_all_teams(self, db:Connection):
        """FUNction which queries the database for all teams"""
        cursor = await db.execute("SELECT * FROM TeamTable")
        return await cursor.fetchall()

    async def insert_or_replace(self, db:Connection, team: Team):
        """Function which accepts a database connection and an instance of the Team class, and inserts it into the database"""

        entry = list(team.__dict__)
        if isinstance(entry[-1], list):
            entry[-1] = [str(tag) for tag in entry[-1]]
            entry[-1] = ", ".join(entry[-1])

        await db.execute("INSERT OR REPLACE INTO TeamTable (NAME, GUILD_ID, LEADER_ID, TEAM_ID, TEAMMATES) VALUES (?, ?, ?, ?, ?)", tuple(entry))

        await db.commit()

teamdb = Database()