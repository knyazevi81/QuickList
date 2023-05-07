import sqlite3


class Database:
    def __init__(self, db_name):
        self.connect = sqlite3.connect(db_name)
        self.cursor = self.connect.cursor()

    def add_clinet(self, client_id: int, clint_username: str):
        with self.connect:
            data = (int(client_id), clint_username, "false", "false")
            self.cursor.execute("INSERT INTO "
                                "profiles(profile_id, profile_username,"
                                " activity, super_user)"
                                "VALUES(?,?,?,?)", data)
            self.connect.commit()

    def quest_user_in_db(self, user_id: int):
        with self.connect:
            all_profiles = self.cursor.execute(f"SELECT profile_id FROM profiles").fetchall()
            if (user_id,) in all_profiles:
                return True
            else:
                return False
