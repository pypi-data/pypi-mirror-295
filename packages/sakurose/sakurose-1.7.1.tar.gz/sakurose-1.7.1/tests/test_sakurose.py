import unittest
from sakurose import save, get, remove, random_number, random_string

class TestSakuRose(unittest.TestCase):

    def test_save_and_get(self):
        save("key:value")
        self.assertEqual(get("key"), "value")

    def test_remove(self):
        save("key:value")
        remove("key")
        self.assertIsNone(get("key"))

    def test_random_number(self):
        num = random_number(1, 10)
        self.assertTrue(1 <= num <= 10)

    def test_random_string(self):
        rand_str = random_string(5)
        self.assertEqual(len(rand_str), 5)

if __name__ == '__main__':
    unittest.main()