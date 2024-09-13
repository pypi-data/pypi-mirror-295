import unittest
from punicalab_core.enums.status_enum import Status
from punicalab_core.utils.enum_utils import get_status_name, get_status_value

class TestEnumUtils(unittest.TestCase):

    def test_status_enum(self):
        self.assertEqual(Status.ACTIVE.value, "2")
        self.assertIn("0", Status.list())

    def test_get_status_name(self):
        self.assertEqual(get_status_name("2"), "ACTIVE")
        self.assertEqual(get_status_name("100"), "Invalid Status Value")

    def test_get_status_value(self):
        self.assertEqual(get_status_value("ACTIVE"), "2")
        self.assertEqual(get_status_value("UNKNOWN"), "Invalid Status Name")

if __name__ == "__main__":
    unittest.main()
