import CongreSQLBackend as App
import sys
import pyodbc


class theApp:
    def __init__(self):
        try:
            App.SQLQueries()
        except(Exception, pyodbc.DatabaseError) as error:
            print(error)
            sys.exit()


if __name__ == '__main__':
    def runTheApp():
        try:
            theApp()
        except Exception as error:
            print("[!]ERROR[!] Please check: {}".format(error))
    runTheApp()
