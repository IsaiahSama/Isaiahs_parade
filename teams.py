from aiosqlite import Connection
from random import sample
from string import hexdigits

digits = list(hexdigits)

def generate_id() -> str:
    return ''.join(sample(digits, k=7))


class Team:
    def __init__(self, name, guildid, ownerid, leaderid, teamid=None, teammates=[]) -> None:
        self.name = name 
        self.guildid = guildid
        self.ownerid = ownerid
        self.leaderid = leaderid
        self.teamid = teamid or generate_id()
        # Teammates is a list of ids
        if not teammates:
            self.teammates = []
        else:
            self.teammates = [int(mate) for mate in teammates.split(", ")] if isinstance(teammates, str) else teammates

    def __repr__(self):
        return f"{self.name} is owned by user with id {self.ownerid}."

class Database:

    def __init__(self) -> None:
        pass

    async def setup(self, db:Connection):
        """Function which accepts a database connection, and sets up the Team Database"""

        await db.execute("""CREATE TABLE IF NOT EXISTS TeamTable(
            NAME TEXT, 
            GUILD_ID INTEGER,
            OWNER_ID INTEGER,
            LEADER_ID INTEGER,
            TEAM_ID TEXT PRIMARY KEY,
            TEAMMATES TEXT);""")

        await db.commit()

    async def query_all_teams(self, db:Connection):
        """FUNction which queries the database for all teams"""
        cursor = await db.execute("SELECT * FROM TeamTable")
        return await cursor.fetchall()

    async def insert_or_replace(self, db:Connection, team: Team):
        """Function which accepts a database connection and an instance of the Team class, and inserts it into the database"""

        
        entry = list(team.__dict__.values())
        print(entry)
        if isinstance(entry[-1], list):
            if not entry[-1]: entry[-1] = ""
            else:
                entry[-1] = [str(tag) for tag in entry[-1]]
                entry[-1] = ", ".join(entry[-1])

        await db.execute("INSERT OR REPLACE INTO TeamTable (NAME, GUILD_ID, OWNER_ID, LEADER_ID, TEAM_ID, TEAMMATES) VALUES (?, ?, ?, ?, ?,?)", tuple(entry))

        await db.commit()

teamdb = Database()