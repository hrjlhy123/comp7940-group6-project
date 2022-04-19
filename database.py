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

"""Send a message when the command /movie is issued."""
try:

    cnx = mysql.connector.connect(user='doadmin', 
                                password='AVNS_IZcLYrdx6q27Ry2',
                                host='db-mysql-sgp1-31144-do-user-11210025-0.b.db.ondigitalocean.com',
                                port='25060',
                                database='defaultdb')
    cursor = cnx.cursor()
    print("Works well!1")
    query = ("SELECT Title, Content FROM MOVIES WHERE Content ='" + input()+ "'")
    print("Works well!2")
    cursor.execute(query)
    print("Works well!3")
    print(len(cursor))
    for (i) in cursor:
        print("Movie: {}".format(i[0]))
        print("Works well!for")
    cursor.close()
    cnx.close()
    print("Works well!end")
except (IndexError, ValueError):
# User: Give me horor movie/ Shows me horor movie. User: /movie horor
    print('Usage: /movie <keyword>')