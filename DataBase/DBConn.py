import psycopg2

class dataBaseConn():
    def __init__(self):
        self.theUser = input("User: ")
        self.thePassword = input("Enter password: ")
        self.theDBName = input("Database name: ")

        theConnection = psycopg2.connect(
            "dbname={} user={}"
                .format(self.theDBName, self.theUser))
        self.theCursor = theConnection.cursor()