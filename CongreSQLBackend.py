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
#    1. CREATE DATABASE           2. CREATE TABLE           3. CREATE FUNCTION         #
#    4. CREATE INDEX              5. CREATE KEY             6. ALTER TABLE             #
#    7. ALTER FUNCTION            8. ALTER INDEX            9. ALTER KEY               #
#    10. UPDATE                   11. DELETE                12. DROP DATABASE          #
#    13. DROP TABLE               14. TRUNCATE TABLE        15. SELECT                 #
#                                                                                      #
#                                 16. QUIT                                             #
########################################################################################
                    """
        self.clearScreen()
        print(theMenu)
        theOption = input(">>").replace(" ", "")
        if theOption == "1":
            self.createDataBase()
        elif theOption == "2":
            self.createTable()
        elif theOption == "3":
            self.createFunction()
        elif theOption == "4":
            self.createIndex()
        elif theOption == "5":
            self.createKeys()
        elif theOption == "6":
            self.alterTable()
        elif theOption == "7":
            self.alterFunction()
        elif theOption == "8":
            self.alterIndex()
        elif theOption == "9":
            self.alterKeys()
        elif theOption == "10":
            self.updateTable()
        elif theOption == "11":
            self.deleteRow()
        elif theOption == "12":
            self.dropDatabase()
        elif theOption == "13":
            self.dropTable()
        elif theOption == "14":
            self.truncateTable()
        elif theOption == "15":
            self.selectTable()
        elif theOption == "16" \
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

    def createFunction(self):
        pass

    def createIndex(self):
        pass

    def createKeys(self):
        pass

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
        pass

    def truncateTable(self):
        pass

    def selectTable(self):
        pass

    def clearScreen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def closeApp(self):
        sys.exit()

    def formatTheError(self, theError):
        return "Error: {}".format(theError)
