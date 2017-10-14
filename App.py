import CongreSQLBackend as App
import getpass

class theApp:
    def __init__(self):
        App.SQLQueries().chooseTheOption()





if __name__ == '__main__':
    def runTheApp():
        theConnection = input("Want to connect? [Y/N]")
        if theConnection == "Y" or theConnection == "y":
            theApp()
        else:
            print("See you later, {}".format(getpass.getuser()))

    runTheApp()
