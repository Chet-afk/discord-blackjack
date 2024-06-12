from sqlite3 import Cursor, Connection, connect
from os.path import exists as os_exists

connection = Connection
cursor = Cursor

def init_setup():
    global connection, cursor

    db_exists = os_exists("./chips.db")
    connection = connect("chips.db")
    cursor = connection.cursor()

    if not db_exists:
        cursor.execute("""CREATE TABLE chips(
                       id INTEGER PRIMARY KEY, 
                       value INTEGER)""")

def register(id: int):
    global connection, cursor
    cursor = cursor.execute(f"""
    SELECT id
    FROM chips
    WHERE id = {id}""")

    if cursor.fetchone() == None:
        cursor.execute(f"""
            INSERT INTO chips (id, value)
            VALUES ({id}, 1000)""")

        connection.commit()

def exists(id: int):
    global connection, cursor
    cursor = cursor.execute(f"""
    SELECT id
    FROM chips
    WHERE id = {id}""")

    if cursor.fetchone() == None:
        return False
    else:
        return True

def update(id: int, difference: int):
    global connection, cursor

    original_val = cursor.execute(f"""
                    SELECT value
                    FROM chips
                    WHERE id = {id}""").fetchone()[0]

    cursor.execute(f"""
                    UPDATE chips
                    SET value = {original_val + difference}
                    WHERE id = {id}""")

    connection.commit()

def get_chips(id: int)->int:
    global cursor
    return cursor.execute(f"""
    SELECT value
    FROM chips
    WHERE id = {id}""").fetchone()[0]

def close():
    global cursor, connection
    cursor.close()
    connection.close()

if __name__ == "__main__":
    init_setup()
    close()