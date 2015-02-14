# coding: utf-8
from . import fields as shuffler_fields
from collections import OrderedDict
from django.forms import model_to_dict

class ShuffleException(Exception): pass

def _get_declared_fields(bases, attrs):
    """
    :param bases: базовые классы нашего класса
    :param attrs: атрибуты класса (который использует наш мета класс)
    :return: сортированный словарь полей класса, как собственных, так и доставшихся от родителей
    """
    # из атрибутов класса вытащим те, которые являются полями
    fields = [(field_name, attrs.pop(field_name))
              for field_name, obj in attrs.items()
              if isinstance(obj, shuffler_fields.Field)]

    # дополним список полей нашего класса, полями из базовых классов
    # так, чтобы поля родительских классов шли перед наследниками
    for base in bases[::-1]:
        if hasattr(base, 'base_fields'):
            fields = list(base.base_fields.items()) + fields

    # составим сортированный словарь полей, при этом поля которые были переопределены в наследниках затрут базовые
    return OrderedDict(fields)

class BaseShufflerMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs['fields'] = _get_declared_fields(bases, attrs)
        return super(BaseShufflerMetaclass, cls).__new__(cls, name, bases, attrs)

class BaseShufflerOptions(object):
    def __init__(self, meta):
        self.model = getattr(meta, 'model')
        self.filters = getattr(meta, 'filters', None)
        self.shuffle_fields = getattr(meta, 'shuffle_fields', None)

class BaseShuffler(object):
    __metaclass__ = BaseShufflerMetaclass
    _options_class = BaseShufflerOptions

    class Meta:
        pass

    def __init__(self):
        super(BaseShuffler, self).__init__()
        self.opts = self._options_class(self.Meta)

        # добавим ShuffleField для указанных в shuffle_fields полей
        if self.opts.shuffle_fields:
            for field_name in self.opts.shuffle_fields:
                if field_name not in self.fields:
                    self.fields[field_name] = shuffler_fields.ShuffleField()

        # проверим что все поля есть среди полей модели
        model_fields = set([f.name for f in self.opts.model._meta.fields])
        for field_name in self.fields:
            if field_name not in model_fields:
                raise ShuffleException(
                    'Field "%s" not found in model "%s" (model fields: %s)' % (
                    field_name,
                    self.opts.model,
                    ', '.join(model_fields)
                ))

    def shuffle(self):
        """
        оснонвой метод для изменения данных в базе
        :return:
        """
        self.prepare()

        # пройдемся по табличке
        qs = self.get_queryset()
        for instance in qs:
            # сгенерим данные для объекта
            values = {}
            for field_name, field in self.fields.items():
                instance_data = model_to_dict(instance)
                value = field.get_data(field_name, instance_data)
                values[field_name] = value
            # обновим значение в базе
            self.opts.model.objects.filter(pk=instance.pk).update(**values)

    def get_queryset(self):
        if self.opts.filters:
            return self.opts.model.objects.filter(**self.opts.filters)
        else:
            return self.opts.model.objects.all()

    def prepare(self):
        for field, field_instance in self.fields.items():
            field_instance.prepare(field, self.opts.model.objects.all())