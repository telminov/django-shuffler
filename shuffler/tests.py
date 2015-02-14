# coding: utf-8
import unittest

from . import fields


class FieldTestCase(unittest.TestCase):

    def test_get_data_not_implemented(self):
        field = fields.Field()

        self.assertRaises(
            NotImplementedError,
            field.get_data,
            'test_name'
        )


if __name__ == '__main__':
    unittest.main()