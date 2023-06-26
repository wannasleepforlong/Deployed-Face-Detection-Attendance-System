import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="sh221b777",
    password="12345",
    database="attendance"
)

cursor = conn.cursor()

select_query = "SELECT * FROM attendance"
cursor.execute(select_query)

rows = cursor.fetchall()

for row in rows:
    print(row)





