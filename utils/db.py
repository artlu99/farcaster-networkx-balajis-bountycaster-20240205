import sqlite3
from utils.constants import SQLITE_DB


def store_follow(fid, target_fid):
    conn = sqlite3.connect(SQLITE_DB)
    c = conn.cursor()

    # create table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS follows (
            fid INTEGER,
            target_fid INTEGER,
            PRIMARY KEY (fid, target_fid)
        )
''')

    # upsert
    c.execute('''
        INSERT INTO follows (fid, target_fid) VALUES (?, ?)
        ON CONFLICT(fid, target_fid) DO NOTHING
''', (fid, target_fid))

    conn.commit()
    conn.close()


def get_list(sql: str, arg1: str):
    conn = sqlite3.connect(SQLITE_DB)
    c = conn.cursor()

    c.execute(sql, (arg1, ))
    rets = c.fetchall()

    # Close the connection
    conn.close()

    return [ret[0] for ret in rets]


def get_follows(fid: int):
    query = '''
        SELECT target_fid 
        FROM follows
        WHERE fid = ?
    '''
    follows = get_list(query, fid)
    return follows


def get_mutuals(fid: int):
    query = '''
        SELECT f1.target_fid 
        FROM follows AS f1
        JOIN follows AS f2 ON f1.fid = f2.target_fid AND f1.target_fid = f2.fid
        WHERE f1.fid = ?
    '''
    mutuals = get_list(query, fid)
    return mutuals


if __name__ == '__main__':
    fid = 37  # fid 37 is balajis.eth
    follows = get_follows(fid)
    mutuals = get_mutuals(fid)

    print("fid:", fid)
    print("n follows:", len(follows))
    print("n mutuals:", len(mutuals))
    print("ratio: {:.2f}".format(len(mutuals) / len(follows)))
