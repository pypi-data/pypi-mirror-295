from enum import Enum

class Status(str, Enum):
    NONE = "0"
    INIT = "1"
    ACTIVE = "2"
    INACTIVE = "3"
    FAILED = "4"
    LOCKED = "5"
    HIDDEN = "6"
    PENDING = "7"
    DELETING = "8"
    DELETED = "9"
    HARDDELETED = "10"
    FINALIZED = "11"
    UNSPECIFIED = "12"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
