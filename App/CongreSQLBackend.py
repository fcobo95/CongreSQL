import psycopg2


class SQLQueries:
    def __init__(self):
        self.theConnection = None
        try:
            # read the connection parameters
            params = "user='postgres' password='viper1829' host='127.0.0.1' port='5432'"
            # connect to the PostgreSQL server
            self.theConnection = psycopg2.connect(params)
            self.theCursor = self.theConnection.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def createDataBase(self):
        theDBName = input("Enter the new database name: ")

        theQuery = """CREATE DATABASE {}""" \
            .format(theDBName)
        try:
            self.theCursor.execute(theQuery)
            self.theCursor.close()
            self.theConnection.commit()
        except (Exception, psycopg2.DatabaseError) as theError:
            print("Error: {}"
                  .format(theError))
        finally:
            if self.theConnection is not None:
                self.theCursor.close()

    def createTable(self):
        theTableName = input("Enter the table name:\n")
        theAttributes = input("Ignore putting '(' and ')' for the attributes and ';' to finish the command\n"
                              "Example ==> id INTEGER, name VARCHAR(20)\n"
                              "Enter the attributes:\n")
        theQuery = """CREATE TABLE {}({})""".format(theTableName, theAttributes)
        try:
            self.theCursor.execute(theQuery)
            # close communication with the PostgreSQL database server
            self.theCursor.close()
            # commit the changes
            self.theConnection.commit()
        except (Exception, psycopg2.DatabaseError) as theError:
            print("Error: {}"
                  .format(theError))
        finally:
            if self.theConnection is not None:
                self.theConnection.close()


if __name__ == '__main__':
    theApp = SQLQueries()
    theApp.createTable()
