import mysql.connector

mydb = mysql.connector.connect(
    host="sql12.freesqldatabase.com",
    user="sql12594236",
    password="Shz3DdFEW1",
    database="sql12594236"
)

db_Info = mydb.get_server_info()
print("Connected to MySQL Server version ", db_Info)
cursor = mydb.cursor()
cursor.execute("select database();")

record = cursor.fetchone()
print("You're connected to database: ", record)

sql_select_Query = "select * from crypto_db"
cursor = mydb.cursor()
cursor.execute(sql_select_Query)
# get all records
records = cursor.fetchall()
print("Total number of rows in table: ", cursor.rowcount)

print(records)