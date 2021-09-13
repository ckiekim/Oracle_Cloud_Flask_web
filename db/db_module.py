import pymysql, json
with open('./db/mysql.json') as fp:
    config_str = fp.read()
config = json.loads(config_str)

def get_user_info(uid):
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    sql = "SELECT pwd, uname, email, DATE_FORMAT(reg_date, '%%Y-%%m-%%d') AS reg_date FROM users WHERE uid=%s AND is_deleted=0;"
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
