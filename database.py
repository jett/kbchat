import sqlite3

conn = sqlite3.connect('data.sqlite')

sql_command = """
DROP TABLE IF EXISTS kb;
CREATE TABLE kb (
    id INTEGER,
    name VARCHAR,
    PRIMARY KEY (id));
"""

conn.close()
