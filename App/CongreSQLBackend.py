import psycopg2
import sys
from Readers import Reader


class SQLQueries:
    def __init__(self):
        self.theConnection = None
        self.theReader = Reader.Reader().theReader
        try:
            theUser = self.theReader['user']
            thePassword = self.theReader['password']
            theHost = self.theReader['host']
            thePort = self.theReader['port']
            theConnectionString = str(
                """
                user={}
                password={}
                host={}
                port={}
                """
                    .format(theUser, thePassword, theHost, thePort))
            self.theConnection = psycopg2.connect(theConnectionString)
            self.theCursor = self.theConnection.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.closeApp()

    def chooseTheOption(self):

        theMenu = """
                    ########################################################################################
                                                        CongreSQL
                         THE BEST CHOICE FOR MANAGING YOUR POSTGRES DATABASE FROM A TERMINAL ENVIRONMENT!


                                                          MENU
                    ########################################################################################
                        1. CREATE DATABASE           2. CREATE TABLE           3. CREATE FUNCTION\n
                        4. CREATE INDEX              5. CREATE KEY             6. ALTER TABLE\n
                        7. ALTER FUNCTION            8. ALTER INDEX            9. ALTER KEY\n
                        10. UPDATE                   11. DELETE                12. \n
                    """
        print(theMenu)
        theOption = input(">>").replace(" ", "")
        if theOption == "1":
            self.createDataBase()
        elif theOption == "2":
            self.createTable()
        elif theOption == "3":
            pass
        elif theOption == "Q" \
                or theOption == "q" \
                or theOption == "Quit" \
                or theOption == "quit":
            self.closeApp()

    def createDataBase(self):
        theDBName = input("Enter the new database name: ")
        if theDBName == "\quit":
            self.chooseTheOption()
        else:
            theQuery = """CREATE DATABASE {}""" \
                .format(theDBName)
            try:
                self.theCursor.execute(theQuery)
                self.theCursor.close()
                self.theConnection.commit()
            except (Exception, psycopg2.DatabaseError) as theError:
                print(self.formatTheError(theError))
                theMessage = input("Want to try again? [Y/N]")
                if theMessage == 'Y' or theMessage == 'y':
                    self.createTable()
                else:
                    self.closeApp()
            finally:
                if self.theConnection is not None:
                    self.theCursor.close()

    def createTable(self):

        theTableName = input("Enter the table name:\n")
        if theTableName == "\quit":
            self.chooseTheOption()
        theAttributes = input("Ignore putting '(' and ')' for the attributes and ';' to finish the command\n"
                              "Example ==> id INTEGER, name VARCHAR(20)\n"
                              "Enter the attributes:\n")
        if theAttributes == "\quit":
            self.chooseTheOption()
        else:
            theQuery = """CREATE TABLE {}({})""".format(theTableName, theAttributes)
            try:
                self.theCursor.execute(theQuery)
                print("Succesful creation of table {}".format(theTableName))
                self.theCursor.close()
                self.theConnection.commit()
                theOptions = input("Want to do some other thing? [Y/N]")
                if theOptions == "Y" or theOptions == "y":
                    self.chooseTheOption()
            except (Exception, psycopg2.DatabaseError) as theError:
                print(self.formatTheError(theError))
                theMessage = input("Want to try again? [Y/N]")
                if theMessage == 'Y' or theMessage == 'y':
                    self.createTable()
                else:
                    self.closeApp()
            finally:
                if self.theConnection is not None:
                    self.theConnection.close()

    def closeApp(self):
        sys.exit()

    def formatTheError(self, theError):
        return "Error: {}".format(theError)


if __name__ == '__main__':
    theApp = SQLQueries()
    theApp.chooseTheOption()
