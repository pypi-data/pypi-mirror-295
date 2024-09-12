import os

def grab_path(filename):
    this_path = os.path.abspath(__file__)
    data_path = os.path.dirname(this_path) + "/data/" + filename
    return data_path
