import CongreSQLBackend as App
import getpass
import sys

class theApp:
    def __init__(self):
        try:
            theConsole = App.SQLQueries()
        except(Exception, pyodbc.DatabaseError) as error:
            sys.exit
            print(error)

if __name__ == '__main__':
    def runTheApp():
        try:
            theApp()
        except:
            print("[!]ERROR[!]")
    runTheApp()
