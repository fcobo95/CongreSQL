from DataBase import DBConn as DB


def createTable():
    theCursor = DB.dataBaseConn().theCursor

    theColumns = input(
        "CREATE TABLE/DATABASE FORMAT ==> columnN0 datatype(#), columnN1 datatype(#), columnN-1 datatype(#)"
        "\nExample ==> id number(6) PRIMARY KEY, name varchar(20) NOT NULL, lastname varchar(20) NOT NULL"
        "\nEnter the table columns and types: ")

    theTableName = input("Enter the table name: ")
    theCursor.execute("""CREATE TABLE {}({});""".format(theTableName, theColumns))


def createDataBase(self):
    pass

if __name__ == '__main__':
    createTable()
