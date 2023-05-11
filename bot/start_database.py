import sqlite3
import settings


def main():
    connect = sqlite3.connect('telegram_base.db')
    cursor = connect.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS profiles(
    id INTEGER PRIMARY KEY,
    profile_id INTEGER,
    profile_username TEXT,
    activity TEXT,
    super_user TEXT,
    notifiers TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    text_work TEXT,
    date TEXT,
    type_activity TEXT,
    type_notif TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS token(
    id INTEGER PRIMARY KEY,
    token_id TEXT,
    activity TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS teems(
    id INTEGER PRIMARY KEY,
    token_id TEXT,
    activity TEXT
    )
    ''')

    have_keys = cursor.execute('SELECT * FROM token').fetchall()

    if not have_keys:
        for key in settings.test_tokens:
            data = (key, 'false')
            cursor.execute('INSERT INTO token(token_id, activity) VALUES(?,?)', data)

    connect.commit()
    connect.close()


if __name__ == '__main__':
    main()
    print('The database was created successfully!')