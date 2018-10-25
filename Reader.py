import json

class Reader:
    """
    :returns theReader
    """

    def __init__(self):
        with open('ConnString.json') as theReader:
            self.theReader = json.load(theReader)