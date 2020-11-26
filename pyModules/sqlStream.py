# -[ Python Modules ]- #
import sqlite3
import os
import pathlib

# -[ Classes ]- #
class createNewStream():
    def __init__(self, hostName, isMem):
        self.cwd = pathlib.Path(os.path.dirname(os.path.realpath(__file__))).parent

        self.hostName = hostName
        self.hostFile = f"{self.cwd}/pyData/{hostName}"

        self.host_table = "host_table"

        if isMem: self.hostFile = ":memory:"

        self.presetRules = [f"""CREATE TABLE IF NOT EXISTS {self.host_table} (
            id interger PRIMARY KEY,
            team_name text,
            team_points text
            )
        """]

        self.sqlConnection = None

        self.connect()
        self.createMainTbl()

    def executeSQL(self, sqlCommand, fetch):
        try:
            sqlCursor = self.sqlConnection.cursor()
            sqlCursor.execute(sqlCommand)

            if fetch:
                return sqlCursor.fetchall()
        except sqlite3.Error as e:
            print(f"[SQL_STREAM]: {e}")

    def commit(self):
        if self.sqlConnection == None: return
        
        self.sqlConnection.commit()

    def getHostTableName(self):
        return self.host_table

    def select(self, cVal, wVal = None):
        command = f"SELECT {cVal} FROM host_table"

        if wVal: command = f"SELECT {cVal} FROM host_table WHERE {wVal}"

        return self.executeSQL(command, True)

    def createMainTbl(self):
        if self.sqlConnection == None: return

        for rule in self.presetRules:
            self.executeSQL(rule, False)

        return

    def connect(self):
        if self.sqlConnection: return

        try: 
            self.sqlConnection = sqlite3.connect(self.hostFile)
        except sqlite3.Error as e:
            print(f"[SQL_STREAM]: {e}")

        return self.sqlConnection != None

    def disconnect(self):
        if self.sqlConnection: 
            self.sqlConnection.close()
            self.sqlConnection = None

        return self.sqlConnection == None
