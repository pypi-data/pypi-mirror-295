from enums.status_enum import Status

def get_status_name(value: str) -> str:
    """
    Given a status value, return its name.
    """
    try:
        return Status(value).name
    except ValueError:
        return "Invalid Status Value"

def get_status_value(name: str) -> str:
    """
    Given a status name, return its value.
    """
    try:
        return Status[name].value
    except KeyError:
        return "Invalid Status Name"
