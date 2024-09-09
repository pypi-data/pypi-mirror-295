import unittest
from ahmpy import first


class TestFirst(unittest.TestCase):
    def test_ahm_first(self):
        self.assertEqual(first.ahm_first(
        ), 'welcome to ahm_first function in first.py file of ahmpy package.')


if __name__ == '__main__':
    unittest.main()
