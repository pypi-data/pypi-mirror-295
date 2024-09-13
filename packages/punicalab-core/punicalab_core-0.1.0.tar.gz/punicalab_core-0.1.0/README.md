# punicalab-core-sdk
This repo contains core packets and utils



# Using ENUM
print(Status.ACTIVE.value)  # Output: "2"
print(Status.list())  # Output: ['0', '1', '2', ...]

# Using Utils
print(get_status_name("2"))  # Output: "ACTIVE"
print(get_status_value("ACTIVE"))  # Output: "2"

## Installation

You can install the package via pip:

```sh
pip install punicalab_core