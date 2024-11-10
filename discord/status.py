from enum import Enum

class Status(Enum):
    OK = 0
    KO = 1
    NA = 2

_STATUS = Status.OK

def set_status(new_status: Status):
    global _STATUS
    _STATUS = new_status

def get_status():
    return _STATUS