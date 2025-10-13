import types


class CustomMeta(type):
    def __new__(cls, name, bases, dct):
        new_dct = {}
        for attr_name, attr_value in dct.items():
            if not attr_name.startswith('__'):
                new_dct['custom_' + attr_name] = attr_value
            else:
                new_dct[attr_name] = attr_value
        return super().__new__(cls, name, bases, new_dct)

    def __setattr__(cls, name, value):
        if not name.startswith('__'):
            super().__setattr__('custom_' + name, value)
        else:
            super().__setattr__(name, value)

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        instance.__dict__ = {
            'custom_' + key if not key.startswith('__') else key: value
            for key, value in instance.__dict__.items()
        }
        return instance