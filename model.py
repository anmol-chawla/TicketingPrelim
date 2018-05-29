import pymysql.cursors

connection = pymysql.connect(host='localhost',
                                  user='anmol',
                                  password='pass',
                                  db='aadb',
                                  charset='utf8mb4',
                                  cursorclass=pymysql.cursors.DictCursor)


def insert_data(identity, name, reg, mail, phone, college, pay, event, pch_name):
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO Sales VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (int(identity), name, reg, mail, int(phone), college, pay, event, pch_name))
            connection.commit()
    finally:
        connection.close()


def check_user(name, pass_string):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM auth WHERE username=%s"
            cursor.execute(sql, (name))
            result = cursor.fetchall()
            if result[0]['password'] == pass_string:
                return True
            else:
                return False
    finally:
        connection.close()