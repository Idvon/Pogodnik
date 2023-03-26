import sys
from json import dumps
from os.path import abspath
from os.path import dirname as d

root_dir = d(d(abspath(__file__)))
sys.path.append(root_dir)


# https://stackoverflow.com/questions/15753390/how-can-i-mock-requests-and-the-response
# This method will be used by the mock to replace requests.get


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def text(self):
        return dumps(self.json_data)
