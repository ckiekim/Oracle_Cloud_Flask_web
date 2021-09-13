import pymysql, json
with open('./db/mysql.json') as fp:
    config_str = fp.read()
config = json.loads(config_str)

def get_user_info(uid):
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    sql = '''SELECT pwd, uname, email, DATE_FORMAT(reg_date, '%%Y-%%m-%%d') AS reg_date FROM users 
                WHERE uid=%s AND is_deleted=0;'''
    cur.execute(sql, (uid,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row

def insert_user(params):
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    sql = "INSERT INTO users VALUES(%s, %s, %s, %s, default, 0);"
    cur.execute(sql, params)
    conn.commit()
    cur.close()
    conn.close()

def get_bbs_list(offset=0):
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    sql = '''SELECT b.bid, b.uid, u.uname, b.title, b.content, 
                    DATE_FORMAT(b.modTime, '%%Y-%%m-%%d %%H:%%i:%%s') AS modTime,
                    b.viewCount, b.replyCount
                FROM bbs AS b
                JOIN users AS u
                ON b.uid=u.uid
                WHERE b.isDeleted=0
                ORDER BY b.bid DESC 
                LIMIT 10 offset %s;'''
    cur.execute(sql, (offset,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def get_bbs_counts():
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    sql = 'SELECT count(*) AS count FROM bbs WHERE isDeleted=0;'
    cur.execute(sql)
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result[0]

