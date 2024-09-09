import sqlite3
from pathlib import Path


class SqlDatabase:
    """A generic SQL database class"""
    def __init__(self, local_db='sql_db.db') -> None:
        self.local_db = local_db

    def __enter__(self):
        self.conn = sqlite3.connect(self.local_db)
        return self.conn.cursor()

    def __exit__(self, *args):
        self.conn.commit()
        self.conn.close()
        # return True



if __name__ == '__main__':

    sql = SqlDatabase()
    
    with sql as s:
        s.execute('''CREATE TABLE IF NOT EXISTS test_table(this INTEGER PRIMARY KEY, that TEXT, other TEXT)''')
        s.execute('''INSERT INTO test_table VALUES(1, 'hello', 'nope')''')
        
    # with sql:
    #     sql.conn.cursor().execute('''CREATE TABLE IF NOT EXISTS test_table(this INTEGER PRIMARY KEY, that TEXT, other TEXT)''')
    #     sql.conn.cursor().execute('''INSERT INTO test_table VALUES(1, 'hello', 'nope')''')
    
    print(vars(sql))
    