import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="JyoungSks092203",
    database="game_time"
)

mycursor = db.cursor()

#mycursor.execute("CREATE TABLE User (user_id int PRIMARY KEY AUTO_INCREMENT, username VARCHAR(50), password VARCHAR(50), time smallint UNSIGNED )")

#mycursor.execute("INSERT INTO User (username, password) VALUES (%s, %s)", ("test", "testing"))
#db.commit()

mycursor.execute("SELECT * FROM User")

for x in mycursor:
    print(x)
