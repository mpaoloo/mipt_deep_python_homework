from abc import ABC, abstractmethod


class BaseDescriptor(ABC):
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        self.validate(value)
        instance.__dict__[self.name] = value

    @abstractmethod
    def validate(self, value):
        pass


class Integer(BaseDescriptor):
    def validate(self, value):
        if not isinstance(value, int):
            raise TypeError(f"Expected int for {self.name}")


class String(BaseDescriptor):
    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError(f"Expected str for {self.name}")


class PositiveInteger(BaseDescriptor):
    def validate(self, value):
        if not isinstance(value, int):
            raise TypeError(f"Expected int for {self.name}")
        if value <= 0:
            raise ValueError(f"Expected positive value for {self.name}")


class Data:
    num = Integer()
    name = String()
    price = PositiveInteger()

    def __init__(self, num, name, price):
        self.num = num
        self.name = name
        self.price = price