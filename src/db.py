import mysql.connector

def connect_to_db():
  try:
    mydb = mysql.connector.connect(
      host="your_mysql_host",
      user="your_username",
      password="your_password",
      database="your_database"
    )
    return mydb
  except mysql.connector.Error as err:
    print(f"Error connecting to MySQL database: {err}")
    return None