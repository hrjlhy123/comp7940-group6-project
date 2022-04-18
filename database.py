import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(user='doadmin', password='AVNS_IZcLYrdx6q27Ry2',
                              host='db-mysql-sgp1-31144-do-user-11210025-0.b.db.ondigitalocean.com',
                              port='25060',
                              database='defaultdb')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
connection.close()