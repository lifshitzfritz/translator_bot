import sqlite3


def connect(db_path: str):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    return connection, cursor


def create_users_table(db_path: str):
    connection, cursor = connect(db_path)
    sql = '''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id BIGINT UNIQUE
        );
    '''
    cursor.execute(sql)
    connection.commit()
    print('users table created')


# id
# lang_from
# lang_to
# original
# translated
# user_id


def create_translations_table(db_path: str):
    connection, cursor = connect(db_path)
    sql = '''
    CREATE TABLE IF NOT EXISTS translations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lang_from TEXT,
        lang_to TEXT,
        original TEXT,
        translated TEXT,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    '''
    cursor.execute(sql)
    connection.commit()
    print('translations table created')


def get_user(db_path: str, chat_id: int):
    connection, cursor = connect(db_path)
    sql = 'select id from users where chat_id = ?;'
    cursor.execute(sql, (chat_id,))
    user_id = cursor.fetchone()  # None, (id,)
    if user_id is None:
        return None
    return user_id[0]


def add_user(db_path: str, chat_id: int):
    connection, cursor = connect(db_path)
    sql = 'insert or ignore into users(chat_id) values (?)'
    cursor.execute(sql, (chat_id,))
    connection.commit()
    print('added user with chat_id:', chat_id)


def create_translation_with_user_id(db_path, chat_id):
    connection, cursor = connect(db_path)
    user_id = get_user(db_path, chat_id)  #
    sql = 'insert into translations(user_id) values (?) returning id;'
    if user_id is not None:
        cursor.execute(sql, (user_id,))
        translation_id = cursor.fetchone()
        return translation_id


def get_user_translations(db_path, chat_id: int):
    connection, cursor = connect(db_path)
    user_id = get_user(db_path, chat_id)
    if user_id is not None:
        sql = 'select * from translations where user_id = ?'
        cursor.execute(sql, (user_id,))
        translations = cursor.fetchall()
        return translations
    return []


def add_translation(db_path, lang_from, lang_to, original, translated, chat_id):
    connection, cursor = connect(db_path)
    user_id = get_user(db_path, chat_id)

    sql = """
    insert into translations(lang_from, lang_to, original, translated, user_id)
    values(?,?,?,?,?);
    """
    cursor.execute(sql, (lang_from, lang_to, original, translated, user_id))
    connection.commit()