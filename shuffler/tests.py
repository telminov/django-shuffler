# coding: utf-8
import unittest
from django.test import TestCase

import fields


class FieldTestCase(unittest.TestCase):

    def test_get_data_not_implemented(self):
        field = fields.Field()

        self.assertRaises(
            NotImplementedError,
            field.get_data,
            'test_name'
        )


class ShuffleFieldTestCase(TestCase):
    def setUp(self):
        pass

    def test_prepare(self):
        field = fields.ShuffleField()
        self.assertRaises(
            AssertionError,
            field.prepare,
            name='test_name'
        )
        self.assertRaises(
            AssertionError,
            field.prepare,
            queryset='test_queryset'
        )




if __name__ == '__main__':
    unittest.main()



from django.db import models


class TestModel(models.Model):
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    birth = models.DateField()
    phone = models.IntegerField()