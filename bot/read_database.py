import sqlite3


class Database:
    def __init__(self, db_name):
        self.connect = sqlite3.connect(db_name)
        self.cursor = self.connect.cursor()

    def add_user(self, user_id: int, user_username: str):
        with self.connect:
            data = (int(user_id), user_username, "false", "false")
            self.cursor.execute("INSERT INTO "
                                "profiles(profile_id, profile_username,"
                                " activity, super_user)"
                                "VALUES(?,?,?,?)", data)
            self.connect.commit()

    def quest_user_in_db(self, user_id: int) -> bool:
        with self.connect:
            all_profiles = self.cursor.execute(f"SELECT profile_id FROM profiles").fetchall()
            if (user_id,) in all_profiles:
                return True
            else:
                return False

    def add_admin(self, user_id: int):
        with self.connect:
            self.cursor.execute(f"UPDATE profiles SET super_user = ? WHERE profile_id = '{user_id}'", ('true',))
            self.connect.commit()

    def is_admin(self, user_id: int) -> bool:
        with self.connect:
            admin_user = self.cursor.execute(f"SELECT super_user FROM profiles WHERE profile_id = {user_id}").fetchone()
            if admin_user[0] == "true":
                return True
            else:
                return False


