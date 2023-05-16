import settings
import sqlite3
import read_database

con = sqlite3.connect(settings.PATH_TO_DB)
cur = con.cursor()

data = cur.execute("SELECT * FROM token").fetchall()

print(data)