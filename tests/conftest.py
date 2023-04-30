import sys
from os.path import abspath
from os.path import dirname as d

root_dir = d(d(abspath(__file__)))
sys.path.append(root_dir)


# https://stackoverflow.com/questions/15753390/how-can-i-mock-requests-and-the-response
# This method will be used by the mock to replace requests.get
