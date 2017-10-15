import psycopg2
import sys
import Reader
import os
import getpass


class SQLQueries:
    def __init__(self):
        self.theConnection = None
        self.theReader = Reader.Reader().theReader
        try:
            theUser = self.theReader['user']
            thePassword = getpass.getpass("Password for {}: ".format(theUser))
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
#               _____                                  _____   ____   _                # 
#              / ____|                                / ____| / __ \ | |               #
#             | |      ___   _ __    __ _  _ __  ___ | (___  | |  | || |               #
#             | |     / _ \ | '_ \  / _` || '__|/ _ \ \___ \ | |  | || |               #
#             | |____| (_) || | | || (_| || |  |  __/ ____) || |__| || |____           #
#              \_____|\___/ |_| |_| \__, ||_|   \___||_____/  \___\_\|______|          #
#                                    __/ |                                             #
#                                   |___/                                              #
#                                 BY ERICK COBO                                        #
########################################################################################
#                              __  __                                                  #
#                             |  \/  |                                                 #
#                             | \  / |  ___  _ __   _   _                              #
#                             | |\/| | / _ \| '_ \ | | | |                             #
#                             | |  | ||  __/| | | || |_| |                             #
#                             |_|  |_| \___||_| |_| \__,_|                             #
########################################################################################
#                                                                                      #
#    1. CREATE DATABASE           2. CREATE TABLE           3. CREATE FUNCTION         #
#    4. CREATE INDEX              5. ALTER TABLE            6. ALTER FUNCTION          #
#    7. ALTER INDEX               8. ALTER KEY              9. UPDATE                  #
#    10. DELETE                   11. DROP DATABASE         12. DROP TABLE             #
#    13. TRUNCATE TABLE           14. SELECT                15. QUIT                   #
#                                                                                      #
########################################################################################
                    """
        self.clearScreen()
        print(theMenu)
        theOption = input(">>>>").replace(" ", "")
        if theOption == "1":
            self.createDataBase()
        elif theOption == "2":
            self.createTable()
        elif theOption == "3":
            self.createFunction()
        elif theOption == "4":
            self.createIndex()
        elif theOption == "5":
            self.alterTable()
        elif theOption == "6":
            self.alterFunction()
        elif theOption == "7":
            self.alterIndex()
        elif theOption == "8":
            self.alterKeys()
        elif theOption == "9":
            self.updateTable()
        elif theOption == "10":
            self.deleteRow()
        elif theOption == "11":
            self.dropDatabase()
        elif theOption == "12":
            self.dropTable()
        elif theOption == "13":
            self.truncateTable()
        elif theOption == "14":
            self.selectTable()
        elif theOption == "15" \
                or theOption == "q" \
                or theOption == "Quit" \
                or theOption == "quit":
            self.clearScreen()
            self.closeApp()

    def createDataBase(self):
        theDBName = input(">>Enter the new database name: ")
        if self.checkForQuit(theDBName):
            self.chooseTheOption()
        else:
            theQuery = """CREATE DATABASE {}""" \
                .format(theDBName)
            try:
                self.theCursor.execute(theQuery)
                print("Succesful creation of database {}".format(theDBName))
                self.theCursor.close()
                self.theConnection.commit()
                theOptions = input(">>Want to do some other thing? [Y/N]")
                if theOptions == "Y" or theOptions == "y":
                    self.chooseTheOption()
            except (Exception, psycopg2.DatabaseError) as theError:
                print(self.formatTheError(theError))
                theMessage = input(">>Want to try again? [Y/N]")
                if theMessage == 'Y' or theMessage == 'y':
                    self.createDataBase()
                else:
                    self.closeApp()
            finally:
                if self.theConnection is not None:
                    self.theCursor.close()

    def createTable(self):

        theTableName = input(">>Enter the table name:\n")
        if self.checkForQuit(theTableName):
            self.chooseTheOption()
        theAttributes = input(">>Ignore putting '(' and ')' for the attributes and ';' to finish the command\n"
                              "Example ==> id INTEGER, name VARCHAR(20)\n"
                              "Enter the attributes:\n")
        if self.checkForQuit(theAttributes):
            self.chooseTheOption()
        else:
            theQuery = """CREATE TABLE {}({})""".format(theTableName, theAttributes)
            try:
                self.theCursor.execute(theQuery)
                print("Succesful creation of table {}".format(theTableName))
                self.theCursor.close()
                self.theConnection.commit()
                theOptions = input(">>Want to do some other thing? [Y/N]")
                if theOptions == "Y" or theOptions == "y":
                    self.chooseTheOption()
            except (Exception, psycopg2.DatabaseError) as theError:
                print(self.formatTheError(theError))
                theMessage = input(">>Want to try again? [Y/N]")
                if theMessage == 'Y' or theMessage == 'y':
                    self.createTable()
                else:
                    self.closeApp()
            finally:
                if self.theConnection is not None:
                    self.theConnection.close()

    def createFunction(self):
        theFunctionName = input(">>Enter the function name you want to create:\n")
        if self.checkForQuit(theFunctionName):
            self.chooseTheOption()

    def createIndex(self):
        theIndexName = input(">>>>Enter the index name:\n")
        if self.checkForQuit(theIndexName):
            self.chooseTheOption()

        theMessage = input(">>Do you want this to be a unique index? [Y/N]")
        if self.checkForQuit(theMessage):
            self.chooseTheOption()

        theTableName = input(">>Specify the table name:\n")
        if self.checkForQuit(theTableName):
            self.chooseTheOption()

        theColumnName = input(">>Enter on which column the index will be created:\n")
        if self.checkForQuit(theColumnName):
            self.chooseTheOption()

        if theMessage == "Y" or "y":
            theQuery = """CREATE UNIQUE INDEX {} ON {}({})""".format(theIndexName, theTableName, theColumnName)
            try:
                self.theCursor.execute(theQuery)
                print("Succesful creation of index {} on table {}, column {}"
                      .format(theIndexName, theTableName, theColumnName))
                self.theCursor.close()
                self.theConnection.commit()
                theOptions = input(">>Want to do some other thing? [Y/N]")
                if theOptions == "Y" or theOptions == "y":
                    self.chooseTheOption()
            except (Exception, psycopg2.DatabaseError) as theError:
                print(self.formatTheError(theError))
                theMessage = input(">>Want to try again? [Y/N]")
                if theMessage == 'Y' or theMessage == 'y':
                    self.createIndex()
                else:
                    self.closeApp()
            finally:
                if self.theConnection is not None:
                    self.theConnection.close()
        elif theMessage == "N" or "n":
            theQuery = """CREATE INDEX {} ON {}({})""".format(theIndexName, theTableName, theColumnName)
            try:
                self.theCursor.execute(theQuery)
                print("Succesful creation of index {} on table {}, column {}"
                      .format(theIndexName, theTableName, theColumnName))
                self.theCursor.close()
                self.theConnection.commit()
                theOptions = input(">>Want to do some other thing? [Y/N]")
                if theOptions == "Y" or theOptions == "y":
                    self.chooseTheOption()
            except (Exception, psycopg2.DatabaseError) as theError:
                print(self.formatTheError(theError))
                theMessage = input(">>Want to try again? [Y/N]")
                if theMessage == 'Y' or theMessage == 'y':
                    self.createIndex()
                else:
                    self.closeApp()
            finally:
                if self.theConnection is not None:
                    self.theConnection.close()
        else:
            print("Invalid option!")

    def alterTable(self):
        pass

    def alterFunction(self):
        pass

    def alterIndex(self):
        pass

    def alterKeys(self):
        pass

    def updateTable(self):
        pass

    def deleteRow(self):
        pass

    def dropDatabase(self):
        pass

    def dropTable(self):
        theTableName = input("Enter the name of the table to be dropped:\n")
        if self.checkForQuit(theTableName):
            self.chooseTheOption()
        else:
            theQuery = """DROP TABLE {} CASCADE CONSTRAINTS""".format(theTableName)
            try:
                self.theCursor.execute(theQuery)
                print("Succesful dropping table {}"
                      .format(theTableName))
                self.theCursor.close()
                self.theConnection.commit()
                theOptions = input(">>Want to do some other thing? [Y/N]")
                if theOptions == "Y" or theOptions == "y":
                    self.chooseTheOption()
            except (Exception, psycopg2.DatabaseError) as theError:
                print(self.formatTheError(theError))
                theMessage = input(">>Want to try again? [Y/N]")
                if theMessage == 'Y' or theMessage == 'y':
                    self.createIndex()
                else:
                    self.closeApp()
            finally:
                if self.theConnection is not None:
                    self.theConnection.close()

    def truncateTable(self):
        print("If you are going to truncate various tables, separate them with commas.")
        theTableName = input("Enter the name of the table you wish to truncate:\n")
        if self.checkForQuit(theTableName):
            self.chooseTheOption()
        else:
            theQuery = """TRUNCATE {}""".format(theTableName)
            try:
                self.theCursor.execute(theQuery)
                print("Succesful truncation on table {}"
                      .format(theTableName))
                self.theCursor.close()
                self.theConnection.commit()
                theOptions = input(">>Want to do some other thing? [Y/N]")
                if theOptions == "Y" or theOptions == "y":
                    self.chooseTheOption()
            except (Exception, psycopg2.DatabaseError) as theError:
                print(self.formatTheError(theError))
                theMessage = input(">>Want to try again? [Y/N]")
                if theMessage == 'Y' or theMessage == 'y':
                    self.createIndex()
                else:
                    self.closeApp()
            finally:
                if self.theConnection is not None:
                    self.theConnection.close()

    #TODO: STILL NEEDS WORK.
    def selectTable(self):
        theArguments = input("Please enter the table columns you are going to query:\n")
        if self.checkForQuit(theArguments):
            self.chooseTheOption()

        theTableName = input("Please specify the table you are querying:\n")
        if self.checkForQuit(theTableName):
            self.chooseTheOption()
        else:
            theQuery = """SELECT {} FROM {}""".format(theArguments, theTableName)
            theMessage = input("Do you need a GROUP BY clause? [Y/N]")
            if theMessage == "Y" or theMessage == "y":
                theHavingArguments = input("Enter the GROUP BY arguments:\n")
                theQuery += """GROUP BY {}""".format(theHavingArguments)
            if theMessage == "Y" or "y":
                pass
            elif theMessage == "N" or "n":
                theMessage = input("Do you want to add a WHERE clause? [Y/N]")
                if theMessage == "Y" or theMessage == "y":
                    print("Just add the condition, avoid the WHERE keyword."
                          "Example ==> a1=b1")
                    theWhereClause = input("Enter the WHERE clause:\n")
                    theQuery += """WHERE {}""".format(theWhereClause)
                else:
                    pass
            else:
                pass

    def checkForQuit(self, theTableName):
        return theTableName == "\quit"

    def clearScreen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def closeApp(self):
        sys.exit()

    def formatTheError(self, theError):
        return "Error: {}".format(theError)
