# coding: utf-8
from collections import defaultdict
import random


class Field(object):

    def __init__(self, *args, **kwargs):
        super(Field, self).__init__()


    def get_data(self, name, instance_data=None):
        raise NotImplemented()

    def prepare(self, name=None, queryset=None):
        """
        Выполняет подготовительные операции перед началом изменения данных в базе
        :return:
        """
        pass


class ShuffleField(Field):

    def __init__(self, group_by=None, *args, **kwargs):
        super(ShuffleField, self).__init__(*args, **kwargs)
        self.group_by = group_by

    def prepare(self, name=None, queryset=None):
        assert not name is None
        assert not queryset is None

        if self.group_by:
            self.data_dict = defaultdict(set)
            value_names = list(self.group_by) + [name]
            for data_item in queryset.values(*value_names).distinct():
                value = data_item.pop(name)
                key = self._get_key(data_item)
                self.data_dict[key].add(value)
            for key, value in self.data_dict.items():
                self.data_dict[key] = tuple(value)
        else:
            self.data_set = tuple(queryset.values_list(name, flat=True).distinct())

    def get_data(self, name, instance_data=None):
        assert not instance_data is None

        if self.group_by:
            key = self._get_key(instance_data)
            value = random.choice(self.data_dict[key])
        else:
            value = random.choice(self.data_set)
        return value

    def _get_key(self, data_item):
        return tuple([data_item[k] for k in self.group_by])


class RandomIntField(Field):
    def __init__(self, length, *args, **kwargs):
        super(RandomIntField, self).__init__(*args, **kwargs)
        self.length = int(length)

    def get_data(self, name, instance_data=None):
        min_value = pow(10, self.length - 1)
        max_value = pow(10, self.length) - 1
        return random.randint(min_value, max_value)


class PhoneField(Field):
    PHONE_CODES = ['903', '906', '925', '916', '965', '926', '929', '968', ]

    def __init__(self, prefix=7, codes=None, *args, **kwargs):
        super(PhoneField, self).__init__(*args, **kwargs)
        self.prefix = prefix
        self.codes = codes or self.PHONE_CODES

    def get_data(self, name, instance_data=None):
        phone_end = random.randint(1000000, 9999999)
        phone = '%s%s%s' % (
            self.prefix,
            random.choice(self.codes),
            phone_end,
        )
        return phone