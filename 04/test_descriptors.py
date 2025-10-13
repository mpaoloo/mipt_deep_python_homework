import unittest
from descriptors import Data, Integer, String, PositiveInteger


class TestDescriptors(unittest.TestCase):
    def test_valid_data(self):
        data = Data(10, "test", 100)
        self.assertEqual(data.num, 10)
        self.assertEqual(data.name, "test")
        self.assertEqual(data.price, 100)

    def test_invalid_types(self):
        with self.assertRaises(TypeError):
            Data("not_int", "test", 100)
        with self.assertRaises(TypeError):
            Data(10, 123, 100)
        with self.assertRaises(TypeError):
            Data(10, "test", "not_int")

    def test_negative_integer(self):
        with self.assertRaises(ValueError):
            Data(10, "test", -100)

    def test_descriptor_independence(self):
        data1 = Data(1, "first", 10)
        data2 = Data(2, "second", 20)
        
        self.assertEqual(data1.num, 1)
        self.assertEqual(data2.num, 2)
        self.assertEqual(data1.name, "first")
        self.assertEqual(data2.name, "second")


if __name__ == "__main__":
    unittest.main()