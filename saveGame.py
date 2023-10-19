from decouple import config
import mysql.connector


class saveGame:
    def __init__(self):
        self.db = None
        self.myCursor = None
        self.insert_query = "INSERT INTO User (name, time) VALUES (%s, %s)"
        self.select_query = "SELECT name, time FROM User ORDER BY time LIMIT 5"

    def connect(self):
        try:
            db_host = config("DB_HOST")
            db_user = config("DB_USER")
            db_pass = config("DB_PASS")
            db_name = config("DB_NAME")

            self.db = mysql.connector.connect(
                host=db_host,
                port=3306,  # Replace with the appropriate port number
                user=db_user,
                passwd=db_pass,
                database=db_name,
            )

            if self.db.is_connected():
                self.myCursor = self.db.cursor()
            else:
                print("Database connection is not established.")
        except mysql.connector.Error as err:
            print(f"Error connecting to the database: {err}")

    def close(self):
        if self.myCursor:
            self.myCursor.close()
        if self.db.is_connected():
            self.db.close()

    def saveTime(self, time: int, name: str):
        try:
            self.connect()
            self.myCursor.execute(self.insert_query, (name, time))
            self.db.commit()
            print("Time inserted successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            self.close()

    def getTopFive(self):
        try:
            self.connect()
            self.myCursor.execute(self.select_query)
            times = self.myCursor.fetchall()
            return times
        except mysql.connector.Error as err:
            print(f"Error executing the query: {err}")
        finally:
            self.close()
