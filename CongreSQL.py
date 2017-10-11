from flask import Flask
import psycopg2

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


class dataBaseConn():

    def __init__(self, user, password, dbname):
        self.user = user
        self.password = password
        self.dbname = dbname

    def dbConnection(self):
        self.user = input("User: ")
        self.password = input("Enter password: ")
        self.dbname = input("Database name: ")

        theConnection = True

        return theConnection

    def createTable(self, **kwargs):
        pass

    def createDataBase(self):
        pass


if __name__ == '__main__':
    app.run()
