import pymysql, json
import hashlib, base64

with open('mysql.json') as fp:
    config_str = fp.read()
config = json.loads(config_str)

conn = pymysql.connect(**config)
cur = conn.cursor()

# 사용자 테이블 생성
sql = '''
    CREATE TABLE if NOT exists users (
        uid VARCHAR(20) NOT NULL PRIMARY KEY, 
        pwd CHAR(44) NOT NULL, 
        uname VARCHAR(20) DEFAULT 'Guest', 
        email VARCHAR(40) NOT NULL,
        reg_date DATETIME DEFAULT CURRENT_TIMESTAMP, 
        is_deleted INT DEFAULT 0 
    );
'''
cur.execute(sql)

# 관리자 등록
#pwd = '********'
pwd_sha256 = hashlib.sha256(pwd.encode())
hashed_pwd = base64.b64encode(pwd_sha256.digest()).decode('utf-8')
sql = "INSERT INTO users(uid, pwd, uname, email) VALUES('admin', %s, '관리자', 'admin@ckworld.com');"
cur.execute(sql, (hashed_pwd,))
conn.commit()

cur.close()
conn.close()