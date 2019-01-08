import pyodbc
import sys
import Reader
import os
import getpass


class SQLQueries:
    def __init__(self):

        self.theConnection = None
        self.readThe = Reader.Reader().theReader

        try:
            theUser = input(">>Enter the username:\n")
            thePassword = getpass.getpass(">>Password for {}: ".format(theUser))
            
            theServer = self.readThe['server']
            thePort = self.readThe['port']
            theDriver = self.readThe['driver']
            
            theDBName = input(">>Enter the database you want to connect to:\n")
            if theDBName == " " or "":
                theDBName = self.readThe['defaultDB']
            theConnectionString = "DRIVER={};SERVER={};PORT={};DATABASE={};UID={};PWD={}".format(theDriver, theServer,
                                                                                                 thePort, theDBName,
                                                                                                 theUser, thePassword)
            self.theConnection = pyodbc.connect(theConnectionString, autocommit=True)
            print(theConnectionString)
            self.theCursor = self.theConnection.cursor()
            self.chooseTheOption()
        except (Exception, pyodbc.DatabaseError) as error:
            self.formatTheError(error)
            sys.exit()

    def chooseTheOption(self):

        theMenu = """
########################################################################################
#                                                                                      #
#   @@@@@@   @@@@@@@@  @@@  @@@  @@@@@@@   @@@@@@@@   @@@@@@    @@@@@@    @@@          #
#  @@@@@@@@  @@@@@@@@  @@@  @@@  @@@@@@@@  @@@@@@@@  @@@@@@@   @@@@@@@@   @@@          #
#  @@!  @@@       @@!  @@!  @@@  @@!  @@@  @@!       !@@       @@!  @@@   @@!          #
#  !@!  @!@      !@!   !@!  @!@  !@!  @!@  !@!       !@!       !@!  @!@   !@!          #
#  @!@!@!@!     @!!    @!@  !@!  @!@!!@!   @!!!:!    !!@@!!    @!@  !@!   @!!          #
#  !!!@!!!!    !!!     !@!  !!!  !!@!@!    !!!!!:     !!@!!!   !@!  !!!   !!!          #
#  !!:  !!!   !!:      !!:  !!!  !!: :!!   !!:            !:!  !!:!!:!:   !!:          #
#  :!:  !:!  :!:       :!:  !:!  :!:  !:!  :!:           !:!   :!: :!:     :!:         #
#  ::   :::   :: ::::  ::::: ::  ::   :::   :: ::::  :::: ::   ::::: :!    :: ::::     #
#   :   : :  : :: : :   : :  :    :   : :  : :: ::   :: : :     : :  :::  : :: : :     #
#                                                                                      #
#                              BY FERNANDO COBO                                        #
########################################################################################
#                              __  __                                                  #
#                             |  \/  |                                                 #
#                             | \  / |  ___  _ __   _   _                              #
#                             | |\/| | / _ \| '_ \ | | | |                             #
#                             | |  | ||  __/| | | || |_| |                             #
#                             |_|  |_| \___||_| |_| \__,_|                             #
########################################################################################
#                                                                                      #
#    1.  CREATE DATABASE          2.  CREATE TABLE           3. CREATE FUNCTION        #
#    4.  CREATE INDEX             5.  ALTER                  6. UPDATE                 #
#    7.  DELETE                   8.  DROP DATABASE          9. DROP TABLE             #
#    10. TRUNCATE TABLE           11. SELECT                12. INSERT                 #
#                                                                                      #
#                                                                                      #
#                                 13. QUIT                                             #
#                                                                                      #
########################################################################################
                    """
        self.clearScreen()

        print(theMenu)
        theOption = input(">>").lstrip().rstrip()
        if self.checkForQuit(theOption):
            self.closeApp()

        else:
            theFunctionRouter = {
                "1": self.createDataBase,
                "2": self.createTable,
                "3": self.createFunction,
                "4": self.createIndex,
                "5": self.alterTable,
                "6": self.updateTableColumn,
                "7": self.deleteRow,
                "8": self.dropDatabase,
                "9": self.dropTable,
                "10": self.truncateTable,
                "11": self.selectTable,
                "12": self.insertValues,
                "13": self.closeApp
                }

            if theOption == "1":
                theFunctionRouter["1"]()
            elif theOption == "2":
                theFunctionRouter["2"]()
            elif theOption == "3":
                theFunctionRouter["3"]()
            elif theOption == "4":
                theFunctionRouter["4"]()
            elif theOption == "5":
                theFunctionRouter["5"]()
            elif theOption == "6":
                theFunctionRouter["6"]()
            elif theOption == "7":
                theFunctionRouter["7"]()
            elif theOption == "8":
                theFunctionRouter["8"]()
            elif theOption == "9":
                theFunctionRouter["9"]()
            elif theOption == "10":
                theFunctionRouter["10"]()
            elif theOption == "11":
                theFunctionRouter["11"]()
            elif theOption == "12":
                theFunctionRouter["12"]()
            elif theOption == "13" or "\quit" or "quit()" or "quit":
                theFunctionRouter["13"]()
            elif theOption is None or " " or "":
                self.chooseTheOption()

    def createDataBase(self):

        theDBName = input(">>Enter the new database name:\n")
        if self.checkForQuit(theDBName):
            self.chooseTheOption()

        else:
            theQuery = """CREATE DATABASE {};""" \
                .format(theDBName)
            print(theQuery)

            try:
                self.theCursor.execute(theQuery)

                print("Succesful creation of database {}".format(theDBName))

                self.theConnection.commit()

                theOptions = self.checkForMoreInputs()

                if theOptions == 'Y' or theOptions == 'y':
                    self.chooseTheOption()

            except (Exception, pyodbc.DatabaseError) as theError:
                print(self.formatTheError(theError))

                theMessage = self.checkForTryAgain()

                if theMessage == 'Y' or theMessage == 'y':
                    self.createDataBase()

                else:
                    self.closeApp()

            finally:
                if self.theConnection is not None:
                    self.theConnection.close()

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

                self.theConnection.commit()

                theOptions = self.checkForMoreInputs()

                if theOptions == 'Y' or theOptions == 'y':
                    self.chooseTheOption()

            except (Exception, pyodbc.DatabaseError) as theError:
                print(self.formatTheError(theError))

                theMessage = self.checkForTryAgain()

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

        theFunctionParameters = input(">>Enter the function parameters:\n")
        if self.checkForQuit(theFunctionParameters):
            self.chooseTheOption()

        theAs = input(">>Enter the AS option you want:\n")
        if self.checkForQuit(theAs):
            self.chooseTheOption()

        else:

            theFunction = \
                """
                CREATE OR REPLACE FUNCTION {}({}) 
                AS '{}'
                LANGUAGE SQL;
                """.format(theFunctionName, theFunctionParameters, theAs)

            try:
                self.theCursor.execute(theFunction)
                print("Succesful creation of function {}"
                      .format(theFunctionName))

                self.theConnection.commit()

                theOptions = self.checkForMoreInputs()

                if theOptions == 'Y' or theOptions == 'y':
                    self.chooseTheOption()

            except (Exception, pyodbc.DatabaseError) as theError:
                print(self.formatTheError(theError))

                theMessage = self.checkForTryAgain()

                if theMessage == 'Y' or theMessage == 'y':
                    self.createFunction()

                else:
                    self.closeApp()

            finally:
                if self.theConnection is not None:
                    self.theConnection.close()

    def createIndex(self):

        theIndexName = input(">>Enter the index name:\n")
        if self.checkForQuit(theIndexName):
            self.chooseTheOption()

        theMessage = input(">>Do you want this to be a unique index? [Y/N]\n")
        if self.checkForQuit(theMessage):
            self.chooseTheOption()

        theTableName = input(">>Specify the table name:\n")
        if self.checkForQuit(theTableName):
            self.chooseTheOption()

        theColumnName = input(">>Enter on which column the index will be created:\n")
        if self.checkForQuit(theColumnName):
            self.chooseTheOption()

        if theMessage == 'Y' or 'Y':
            theQuery = """CREATE UNIQUE INDEX {} ON {}({})""".format(theIndexName, theTableName, theColumnName)

            try:
                self.theCursor.execute(theQuery)
                print("Succesful creation of index {} on table {}, column {}"
                      .format(theIndexName, theTableName, theColumnName))

                self.theConnection.commit()

                theOptions = self.checkForMoreInputs()

                if theOptions == 'Y' or theOptions == 'y':
                    self.chooseTheOption()

            except (Exception, pyodbc.DatabaseError) as theError:
                print(self.formatTheError(theError))

                theMessage = self.checkForTryAgain()

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

                self.theConnection.commit()

                theOptions = self.checkForMoreInputs()

                if theOptions == 'Y' or theOptions == 'y':
                    self.chooseTheOption()

            except (Exception, pyodbc.DatabaseError) as theError:
                print(self.formatTheError(theError))

                theMessage = self.checkForTryAgain()
                if theMessage == 'Y' or theMessage == 'y':
                    self.createIndex()

                else:
                    self.closeApp()

            finally:
                if self.theConnection is not None:
                    self.theConnection.close()
        else:
            print("Invalid option!")

    def alterOptions(self):
        theMenu = \
            """
            ###########################################
            #+++++++++++++++++++++++++++++++++++++++++#
            #+ Please choose an option from the menu +#
            #+++++++++++++++++++++++++++++++++++++++++#
            ###########################################
            ## 1. TABLE                              ##
            ## 2. ROLE                               ##
            ###########################################
            """
        print(theMenu)

        theOptions = input(">>Enter option from the menu:\n")

        if theOptions == "1":
            self.alterTable()

        elif theOptions == "2":
            self.alterRole()

    def alterTable(self):
        theMenu = \
            """
            ###########################################
            #+++++++++++++++++++++++++++++++++++++++++#
            #+ Please choose an option from the menu +#
            #+++++++++++++++++++++++++++++++++++++++++#
            ###########################################
            ## 1. ADD COLUMN                         ##
            ## 2. DROP COLUMN                        ##
            ## 3. ADD CONSTRAINT                     ##
            ## 4. DROP CONSTRAINT                    ##
            ## 5. ALTER COLUMN                       ##
            ###########################################
            """
        print(theMenu)
        theTableOptions = input(">>Enter the option you want from the menu:\n")
        if theTableOptions == "1":
            self.alterOptionsAddColumn()

        elif theTableOptions == "2":
            self.alterOptionsDropColumn()

        elif theTableOptions == "3":
            self.alterOptionsAddConstraint()

        elif theTableOptions == "4":
            self.alterOptionsDropConstraint()

        elif theTableOptions == "5":
            self.alterOptionsTableColumn()

    def alterRole(self):
        theRoleName = input(">>Enter the role name:\n")
        if self.checkForQuit(theRoleName):
            self.chooseTheOption()
        theChange = input(">>Make sure to enter the proper options. Enter what you want to change:\n")
        if self.checkForQuit(theChange):
            self.chooseTheOption()
        theQuery = """ALTER ROLE {} {}""".format(theRoleName, theChange)
        try:
            self.theCursor.execute(theQuery)
            print("Succesful alter of role {}"
                  .format(theRoleName))

            self.theConnection.commit()

            theOptions = self.checkForMoreInputs()

            if theOptions == 'Y' or theOptions == 'y':
                self.chooseTheOption()

        except (Exception, pyodbc.DatabaseError) as theError:
            print(self.formatTheError(theError))

            theMessage = self.checkForTryAgain()
            if theMessage == 'Y' or theMessage == 'y':
                self.alterRole()

            else:
                self.closeApp()

        finally:
            if self.theConnection is not None:
                self.theConnection.close()

    def alterOptionsTableColumn(self):
        theTableName = input(">>Enter the new column that you wish to modify:\n")
        if self.checkForQuit(theTableName):
            self.chooseTheOption()
        theColumnName = input(">>Enter the new column's name:\n")
        if self.checkForQuit(theColumnName):
            self.chooseTheOption()
        theQuery = """ALTER TABLE {} ALTER COLUMN {}""" \
            .format(theTableName, theColumnName)
        try:
            self.theCursor.execute(theQuery)
            print("Succesful alter of table {}"
                  .format(theTableName))

            self.theConnection.commit()

            theOptions = self.checkForMoreInputs()

            if theOptions == 'Y' or theOptions == 'y':
                self.chooseTheOption()

        except (Exception, pyodbc.DatabaseError) as theError:
            print(self.formatTheError(theError))

            theMessage = self.checkForTryAgain()
            if theMessage == 'Y' or theMessage == 'y':
                self.alterOptionsTableColumn()

            else:
                self.closeApp()

        finally:
            if self.theConnection is not None:
                self.theConnection.close()

    def alterOptionsDropConstraint(self):

        theTableName = input(">>Enter the table name that you are trying to query:\n")
        if self.checkForQuit(theTableName):
            self.chooseTheOption()

        theColumnName = input(">>Enter the constraint's name you wish to drop:\n")
        if self.checkForQuit(theColumnName):
            self.chooseTheOption()

        theQuery = """ALTER TABLE {} DROP CONSTRAINT {}""" \
            .format(theTableName, theColumnName)
        try:
            self.theCursor.execute(theQuery)
            print("Succesful alter of table {}"
                  .format(theTableName))

            self.theConnection.commit()

            theOptions = self.checkForMoreInputs()

            if theOptions == 'Y' or theOptions == 'y':
                self.chooseTheOption()

        except (Exception, pyodbc.DatabaseError) as theError:
            print(self.formatTheError(theError))

            theMessage = self.checkForTryAgain()
            if theMessage == 'Y' or theMessage == 'y':
                self.alterOptionsDropConstraint()

            else:
                self.closeApp()

        finally:
            if self.theConnection is not None:
                self.theConnection.close()

    def alterOptionsAddConstraint(self):

        theTableName = input(">>Enter the name of the table that you wish to alter:\n")
        if self.checkForQuit(theTableName):
            self.chooseTheOption()

        theColumnName = input(">>Enter the new constraint's name:\n")
        if self.checkForQuit(theColumnName):
            self.chooseTheOption()

        theQuery = """ALTER TABLE {} ADD CONSTRAINT {}""" \
            .format(theTableName, theColumnName)

        try:
            self.theCursor.execute(theQuery)
            print("Succesful alter of table {}"
                  .format(theTableName))

            self.theConnection.commit()

            theOptions = self.checkForMoreInputs()

            if theOptions == 'Y' or theOptions == 'y':
                self.chooseTheOption()

        except (Exception, pyodbc.DatabaseError) as theError:
            print(self.formatTheError(theError))

            theMessage = self.checkForTryAgain()
            if theMessage == 'Y' or theMessage == 'y':
                self.alterOptionsAddConstraint()

            else:
                self.closeApp()

        finally:
            if self.theConnection is not None:
                self.theConnection.close()

    def alterOptionsDropColumn(self):

        theTableName = input(">>Enter the name of the table that you wish to alter:\n")
        if self.checkForQuit(theTableName):
            self.chooseTheOption()

        theColumnName = input(">>Enter the column name that you wish to drop:\n")
        if self.checkForQuit(theColumnName):
            self.chooseTheOption()

        theQuery = """ALTER TABLE {} DROP COLUMN {}""" \
            .format(theTableName, theColumnName)

        try:
            self.theCursor.execute(theQuery)
            print("Succesful alter of table {}"
                  .format(theTableName))

            self.theConnection.commit()

            theOptions = self.checkForMoreInputs()

            if theOptions == 'Y' or theOptions == 'y':
                self.chooseTheOption()

        except (Exception, pyodbc.DatabaseError) as theError:
            print(self.formatTheError(theError))

            theMessage = self.checkForTryAgain()
            if theMessage == 'Y' or theMessage == 'y':
                self.alterOptionsDropColumn()

            else:
                self.closeApp()

        finally:
            if self.theConnection is not None:
                self.theConnection.close()

    def alterOptionsAddColumn(self):

        theTableName = input(">>Enter the table that you wish to alter:\n")
        if self.checkForQuit(theTableName):
            self.chooseTheOption()

        theColumnName = input(">>Enter the new column's name and dataype:\n")
        if self.checkForQuit(theColumnName):
            self.chooseTheOption()

        theQuery = """ALTER TABLE {} ADD COLUMN {}""" \
            .format(theTableName, theColumnName)

        try:
            self.theCursor.execute(theQuery)
            print("Succesful alter of table {}"
                  .format(theTableName))

            self.theConnection.commit()

            theOptions = self.checkForMoreInputs()

            if theOptions == 'Y' or theOptions == 'y':
                self.chooseTheOption()

        except (Exception, pyodbc.DatabaseError) as theError:
            print(self.formatTheError(theError))

            theMessage = self.checkForTryAgain()
            if theMessage == 'Y' or theMessage == 'y':
                self.alterOptionsAddColumn()

            else:
                self.closeApp()

        finally:
            if self.theConnection is not None:
                self.theConnection.close()

    def deleteRow(self):

        theTableName = input(">>Enter the table you will delete records from:\n")
        if self.checkForQuit(theTableName):
            self.chooseTheOption()

        theCondition = input(">>Enter the condition to delete:\n")
        if self.checkForQuit(theCondition):
            self.chooseTheOption()

        theQuery = """DELETE FROM {} WHERE {}""".format(theTableName, theCondition)

        try:
            self.theCursor.execute(theQuery)
            print("Succesful deletion in table {}"
                  .format(theTableName))

            self.theConnection.commit()

            theOptions = self.checkForMoreInputs()

            if theOptions == 'Y' or theOptions == 'y':
                self.chooseTheOption()

        except (Exception, pyodbc.DatabaseError) as theError:
            print(self.formatTheError(theError))

            theMessage = self.checkForTryAgain()
            if theMessage == 'Y' or theMessage == 'y':
                self.deleteRow()

            else:
                self.closeApp()

        finally:
            if self.theConnection is not None:
                self.theConnection.close()

    def updateTableColumn(self):

        theTableName = input(">>Enter the table name:\n")
        if self.checkForQuit(theTableName):
            self.chooseTheOption()

        theColumnName = input(">>Enter the column name you wanto to update:\n")
        if self.checkForQuit(theColumnName):
            self.chooseTheOption()

        print("Make sure to write the column name and the new value\nFor example ==> plate=123456\n")

        theNewValue = input(">>Enter the new value:\n")
        if self.checkForQuit(theNewValue):
            self.chooseTheOption()

        print("Make sure to write the condition to update\nFor example ==> model='accent'\n")

        theCondition = input(">>Enter the update condition:\n")
        if self.checkForQuit(theCondition):
            self.chooseTheOption()

        else:
            theQuery = """UPDATE {} SET {} WHERE {}""" \
                .format(theTableName, theNewValue, theCondition)

            try:
                self.theCursor.execute(theQuery)
                print("Succesful update table {} column {}"
                      .format(theTableName, theColumnName))

                print("The new value is {}".format(theNewValue))
                self.theConnection.commit()

                theOptions = self.checkForMoreInputs()

                if theOptions == 'Y' or theOptions == 'y':
                    self.chooseTheOption()

            except (Exception, pyodbc.DatabaseError) as theError:
                print(self.formatTheError(theError))

                theMessage = self.checkForTryAgain()

                if theMessage == 'Y' or theMessage == 'y':
                    self.updateTableColumn()

                else:
                    self.closeApp()

            finally:
                if self.theConnection is not None:
                    self.theConnection.close()

    def dropDatabase(self):

        theDBName = input(">>Enter the database to be dropped:\n")
        if self.checkForQuit(theDBName):
            self.chooseTheOption()

        else:
            theQuery = """DROP DATABASE {}""".format(theDBName)

            try:
                self.theCursor.execute(theQuery)
                print("Succesful dropping table {}"
                      .format(theDBName))

                self.theConnection.commit()

                theOptions = self.checkForMoreInputs()

                if theOptions == 'Y' or theOptions == 'y':
                    self.chooseTheOption()

            except (Exception, pyodbc.DatabaseError) as theError:
                print(self.formatTheError(theError))

                theMessage = self.checkForTryAgain()
                if theMessage == 'Y' or theMessage == 'y':
                    self.dropDatabase()

                else:
                    self.closeApp()

            finally:
                if self.theConnection is not None:
                    self.theConnection.close()

    def dropTable(self):

        theTableName = input(">>Enter the name of the table to be dropped:\n")
        if self.checkForQuit(theTableName):
            self.chooseTheOption()

        else:
            theQuery = """DROP TABLE {} CASCADE CONSTRAINTS""".format(theTableName)

            try:
                self.theCursor.execute(theQuery)
                print("Succesful dropping table {}"
                      .format(theTableName))

                self.theConnection.commit()

                theOptions = self.checkForMoreInputs()

                if theOptions == 'Y' or theOptions == 'y':
                    self.chooseTheOption()

            except (Exception, pyodbc.DatabaseError) as theError:
                print(self.formatTheError(theError))

                theMessage = self.checkForTryAgain()
                if theMessage == 'Y' or theMessage == 'y':
                    self.dropTable()

                else:
                    self.closeApp()

            finally:
                if self.theConnection is not None:
                    self.theConnection.close()

    def truncateTable(self):

        print("If you are going to truncate various tables, separate them with commas.")

        theTableName = input(">>Enter the name of the table you wish to truncate:\n")
        if self.checkForQuit(theTableName):
            self.chooseTheOption()
        else:
            theQuery = """TRUNCATE {}""".format(theTableName)

            try:
                self.theCursor.execute(theQuery)
                print("Succesful truncation on table {}"
                      .format(theTableName))

                self.theConnection.commit()

                theOptions = self.checkForMoreInputs()

                if theOptions == 'Y' or theOptions == 'y':
                    self.chooseTheOption()

            except (Exception, pyodbc.DatabaseError) as theError:
                print(self.formatTheError(theError))

                theMessage = self.checkForTryAgain()
                if theMessage == 'Y' or theMessage == 'y':
                    self.truncateTable()

                else:
                    self.closeApp()

            finally:
                if self.theConnection is not None:
                    self.theConnection.close()

    def insertValues(self):

        theTableName = input(">>Enter the table you are trying to query:\n")
        if self.checkForQuit(theTableName):
            self.chooseTheOption()

        theMessage = "Please ignore adding parentheses.\nSeparate the values with commas.\n"
        print(theMessage)

        theValues = input(">>Enter the values:\n")
        if self.checkForQuit(theValues):
            self.chooseTheOption()

        else:
            theQuery = """INSERT INTO {} VALUES({})""".format(theTableName, theValues)

            try:
                self.theCursor.execute(theQuery)
                print("Succesful insert into table {}"
                      .format(theTableName))

                self.theConnection.commit()

                theOptions = self.checkForMoreInserts()
                if theOptions == 'Y' or theOptions == 'y':
                    self.insertValues()

                elif theOptions == 'N' or theOptions == 'n':
                    self.chooseTheOption()

            except (Exception, pyodbc.DatabaseError) as theError:
                print(self.formatTheError(theError))

                theMessage = self.checkForTryAgain()
                if theMessage == 'Y' or theMessage == 'y':
                    self.insertValues()

                else:
                    self.closeApp()

            finally:
                if self.theConnection is not None:
                    self.theConnection.close()

    def selectTable(self):

        theOption = input(">>Are you going to execute a function? [Y/N]\n")

        if theOption == 'N' or theOption == 'n':
            theArguments = input(">>Please enter the table columns you are going to query:\n")
            if self.checkForQuit(theArguments):
                self.chooseTheOption()

            theTableName = input(">>Please specify the table you are querying:\n")
            if self.checkForQuit(theTableName):
                self.chooseTheOption()

            else:
                theMessage = input(">>Is this all you are going to query? [Y/N]\n")

                if theMessage == 'Y' or theMessage == 'y':
                    theQuery = """SELECT {} FROM {}""".format(theArguments, theTableName)

                    try:
                        self.theCursor.execute(theQuery)
                        print("Succesful SELECT on table {}"
                              .format(theTableName))
                        theSelectValues = self.theCursor.fetchall()

                        theColumns = theArguments.replace(",", " | ")

                        print(theColumns)
                        print("++++++++++++++++++++++++++++++++++++++")

                        for each_item in theSelectValues:
                            theValues = str(each_item)
                            theValue = str(theValues).replace("(", "").replace(")", "").replace(",", " | ")
                            print(theValue + "\n")
                        self.theConnection.commit()

                        theOptions = self.checkForMoreInputs()
                        if theOptions == 'Y' or theOptions == 'y':
                            self.chooseTheOption()

                    except (Exception, pyodbc.DatabaseError) as theError:
                        print(self.formatTheError(theError))

                        theMessage = self.checkForTryAgain()
                        if theMessage == 'Y' or theMessage == 'y':
                            self.selectTable()

                        else:
                            self.closeApp()

                    finally:
                        if self.theConnection is not None:
                            self.theConnection.close()

                elif theMessage == 'N' or theMessage == 'n':
                    theMessage = "Please make sure to use the ON statement."
                    print(theMessage)

                    theJoinMessage = input(">>Do you need to add a JOIN?[Y/N]\n")
                    if theJoinMessage == 'Y' or theJoinMessage == 'y':
                        theJoinOptionsMenu = \
                            """
                            1. LEFT JOIN
                            2. INNER JOIN
                            3. RIGHT JOIN
                            4. FULL OUTER JOIN
                            5. JOIN
                            """
                        print(theJoinOptionsMenu)

                        theJoinOption = input(">>Please choose the JOIN type that you want to use:\n")
                        if theJoinOption == "1":
                            theJoinOption = "LEFT OUTER JOIN"

                        elif theJoinOption == "2":
                            theJoinOption = "INNER JOIN"

                        elif theJoinOption == "3":
                            theJoinOption = "RIGHT JOIN"

                        elif theJoinOption == "4":
                            theJoinOption = "FULL OUTER JOIN"

                        else:
                            theJoinOption = "JOIN"
                        theOtherTable = input(">>Enter the table you are going to use for the JOIN:\n")
                        theJoinCondition = input(">>Enter the JOIN condition:\n")
                        theQuery = """SELECT {} FROM {} {} {} ON {}""" \
                            .format(theArguments, theTableName, theJoinOption, theOtherTable, theJoinCondition)

                        try:
                            self.theCursor.execute(theQuery)
                            print("Succesful SELECT on table {}"
                                  .format(theTableName))

                            theSelectValues = self.theCursor.fetchall()

                            theColumns = theArguments.replace(",", " | ")
                            print(theColumns)

                            for each_item in theSelectValues:
                                theValues = str(each_item)
                                print(theValues + "\n")

                            self.theConnection.commit()
                            theOptions = self.checkForMoreInputs()

                            if theOptions == 'Y' or theOptions == 'y':
                                self.chooseTheOption()

                        except (Exception, pyodbc.DatabaseError) as theError:
                            print(self.formatTheError(theError))

                            theMessage = self.checkForTryAgain()
                            if theMessage == 'Y' or theMessage == 'y':
                                self.selectTable()

                            else:
                                self.closeApp()

                        finally:
                            if self.theConnection is not None:
                                self.theConnection.close()

                    theWhereMessage = input(">>Do you need to add a WHERE CLAUSE? [Y/N]\n")

                    if theWhereMessage == 'Y' or theWhereMessage == 'y':
                        theWhereClause = input(">>Enter the WHERE CLAUSE:\n")
                        theQuery = "SELECT {} FROM {} WHERE {}".format(theArguments, theTableName, theWhereClause)

                        try:
                            self.theCursor.execute(theQuery)
                            print("Succesful SELECT on table {}"
                                  .format(theTableName))

                            theSelectValues = self.theCursor.fetchall()

                            theColumns = theArguments.replace(",", " | ")
                            print(theColumns)

                            for each_item in theSelectValues:
                                theValues = str(each_item)
                                print(theValues + "\n")

                            self.theConnection.commit()
                            theOptions = self.checkForMoreInputs()

                            if theOptions == 'Y' or theOptions == 'y':
                                self.chooseTheOption()

                        except (Exception, pyodbc.DatabaseError) as theError:
                            print(self.formatTheError(theError))

                            theMessage = self.checkForTryAgain()
                            if theMessage == 'Y' or theMessage == 'y':
                                self.selectTable()

                            else:
                                self.closeApp()

                        finally:
                            if self.theConnection is not None:
                                self.theConnection.close()

        elif theOption == 'Y' or theOption == 'y':

            theFunctionName = input(">>Enter the function name:\n")
            if self.checkForQuit(theFunctionName):
                self.chooseTheOption()

            theFunctionParameters = input(">>Enter the function parameter values:\n")
            if self.checkForQuit(theFunctionParameters):
                self.chooseTheOption()

            else:
                theQuery = \
                    """
                    SELECT {}({})
                    """.format(theFunctionName, theFunctionParameters)
                try:
                    self.theCursor.execute(theQuery)
                    print("Succesful FUNCTION {}"
                          .format(theFunctionName))

                    theSelectValues = self.theCursor.fetchall()

                    theColumns = theFunctionParameters.replace(",", " | ")
                    print(theColumns)

                    for each_item in theSelectValues:
                        theValues = str(each_item)
                        print(theValues + "\n")

                    self.theConnection.commit()
                    theOptions = self.checkForMoreInputs()

                    if theOptions == 'Y' or theOptions == 'y':
                        self.chooseTheOption()

                except (Exception, pyodbc.DatabaseError) as theError:
                    print(self.formatTheError(theError))

                    theMessage = self.checkForTryAgain()

                    if theMessage == 'Y' or theMessage == 'y':
                        self.selectTable()

                    else:
                        self.closeApp()

                finally:
                    if self.theConnection is not None:
                        self.theConnection.close()

    @staticmethod
    def checkForTryAgain():
        return input(">>Want to try again? [Y/N]\n")

    @staticmethod
    def checkForMoreInputs():
        return input(">>Do you want to keep using the app? [Y/N]\n")

    @staticmethod
    def checkForMoreInserts():
        return input(">>Do you want to insert more values?[Y/N]\n")

    @staticmethod
    def checkForQuit(theOption):
        return theOption == "\quit"

    @staticmethod
    def clearScreen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def closeApp():
        sys.exit()

    @staticmethod
    def formatTheError(theError):
        return "Error: {}".format(theError)
