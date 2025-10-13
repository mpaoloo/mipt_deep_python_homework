import unittest
from custom_meta import CustomClass, CustomMeta


class TestCustomMeta(unittest.TestCase):
    def test_class_attributes(self):
        self.assertEqual(CustomClass.custom_x, 50)
        with self.assertRaises(AttributeError):
            CustomClass.x

    def test_instance_attributes(self):
        inst = CustomClass(99)
        self.assertEqual(inst.custom_val, 99)
        with self.assertRaises(AttributeError):
            inst.val

    def test_methods(self):
        inst = CustomClass(99)
        self.assertEqual(inst.custom_line(), 100)
        with self.assertRaises(AttributeError):
            inst.line()

    def test_magic_methods(self):
        inst = CustomClass(99)
        self.assertEqual(str(inst), "Custom_by_metaclass")

    def test_dynamic_attributes(self):
        inst = CustomClass(99)
        inst.dynamic = "added later"
        self.assertEqual(inst.custom_dynamic, "added later")
        with self.assertRaises(AttributeError):
            inst.dynamic

    def test_class_setattr(self):
        CustomClass.test_attr = "test"
        self.assertEqual(CustomClass.custom_test_attr, "test")
        with self.assertRaises(AttributeError):
            CustomClass.test_attr


if __name__ == "__main__":
    unittest.main()