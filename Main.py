import CongreSQLBackend as App
import sys

if __name__ == '__main__':
    while True:
        theConnection = input(">>")
        if theConnection == "conn" or "connect":
            CongreSQL = App
            theApp = CongreSQL.SQLQueries().chooseTheOption()
        elif theConnection == "disconn" or "disconnect":
            sys.exit()
        else:
            print("Something happened. Hmmm.")