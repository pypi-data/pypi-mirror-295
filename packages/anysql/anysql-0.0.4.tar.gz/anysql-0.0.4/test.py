import logging
from anysql import Database

logging.basicConfig(level=logging.DEBUG)

def test():
    db = Database('postgres://test-user:test-password@localhost/test')
    db.connect()
    db.execute('CREATE TABLE Test (Name VARCHAR(20))')
    db.execute("INSERT INTO Test VALUES ('a'), ('b'), ('c')")

    for rec in db.fetch_yield('SELECT * FROM Test'):
        now = db.fetch_one('SELECT now()')
        print(rec, now)

    db.disconnect()

test()
