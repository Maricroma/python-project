#Más info en https://realpython.com/python-mysql/#installing-mysql-connectorpython
#https://www.w3schools.com/sql/default.asp   

import mysql.connector

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "1234",
            database = "escuela",
        )
        self.cursor = self.connection.cursor()

