import sqlite3


class Database:
    """функция добавления аи токенов """
    def __init__(self, db_name):
        self.connect = sqlite3.connect(db_name)
        self.cursor = self.connect.cursor()

    def add_user(self, user_id: int, user_username: str):
        with self.connect:
            data = (int(user_id), user_username, "false", "false", "true")
            self.cursor.execute("INSERT INTO "
                                "profiles(profile_id, profile_username,"
                                " activity, super_user, notifiers)"
                                "VALUES(?,?,?,?,?)", data)
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

    def get_ai(self, user_id: int, token: str) -> bool:
        true_token = self.cursor.execute(f"SELECT activity FROM token WHERE token_id = '{token}'").fetchone()
        if 'false' in true_token:
            self.cursor.execute(f"UPDATE profiles SET activity = ? WHERE profile_id = {user_id}", ('true',))
            self.cursor.execute(f"UPDATE token SET activity = ? WHERE token_id = '{token}'", ('true',))
            return True
        else:
            return False

    def is_ai_assistent(self, user_id: int) -> bool:
        with self.connect:
            artint = self.cursor.execute(f"SELECT activity FROM profiles WHERE profile_id = {user_id}").fetchone()
            if artint[0] == "true":
                return True
            else:
                return False

    def now_tasks_num(self, user_id: int) -> int:
        with self.connect:
            return len(self.how_undone_tasks(user_id))

    def how_undone_tasks(self, user_id):
        with self.connect:
            with self.connect:
                data = self.cursor.execute(f"""SELECT id, text_work 
                                               FROM tasks 
                                               WHERE type_activity = 'false' AND user_id = {user_id}
                                            """).fetchall()
                return data

    def add_task(self, user_id: int, text_task: str):
        with self.connect:
            data = (user_id, text_task, "none", 'false', 'false')
            self.cursor.execute("""INSERT INTO tasks(user_id, text_work, date, type_activity, type_notif) 
                                   VALUES(?, ?, ?, ?, ?) 
                                   """, data)
            self.connect.commit()

    def del_task(self, user_id: int, task_id: int):
        with self.connect:
            temp_bool = False
            data = self.how_undone_tasks(user_id)
            for id_task, text_task in data:
                if id_task == task_id:
                    temp_bool = True
            self.cursor.execute(f"DELETE FROM tasks WHERE user_id = {user_id} AND id = {task_id}")
            self.connect.commit()
            return temp_bool

    def update_notifier(self, user_id: int) -> bool:
        with self.connect:
            notif = self.cursor.execute(f"SELECT notifiers FROM profiles WHERE profile_id = {user_id}").fetchone()
            if "true" in notif:
                self.cursor.execute(f"UPDATE profiles SET notifiers = ? WHERE profile_id = {user_id}", ("false",))
                return False
            else:
                self.cursor.execute(f"UPDATE profiles SET notifiers = ? WHERE profile_id = {user_id}", ("true",))
                return True

    def all_user_to_notifier(self):
        with self.connect:
            data = self.cursor.execute("SELECT profile_id FROM profiles WHERE notifiers = 'true'").fetchall()
            return data

    def all_users(self):
        with self.connect:
            data = self.cursor.execute("SELECT profile_username, activity, notifiers, super_user  FROM profiles").fetchall()
            return data

    def all_tokens(self):
        with self.connect:
            data = self.connect.execute("SELECT token_id, activity FROM token").fetchall()
            return data





