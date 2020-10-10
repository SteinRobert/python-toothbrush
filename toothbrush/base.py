from bluepy.btle import Peripheral

from toothbrush.constants import ATTRIBUTE_MAP_VERBOSE_NAME
from toothbrush.exceptions import HandleNotDefined


class Toothbrush:
    attributes = []
    handles = []

    def __init__(self, address, interface=0):
        self.address = address
        self.interface = interface
        self.update()

    @property
    def peripheral(self):
        return Peripheral(self.address, "public")

    def update(self):
        peripheral = self.peripheral
        for attribute in self.attributes:
            val = peripheral.readCharacteristic(self.get_handle(attribute))
            self.update_attribute(attribute, val)
        peripheral.disconnect()

    def update_attribute(self, attr, attr_value):
        name = ATTRIBUTE_MAP_VERBOSE_NAME[attr]
        try:
            parse_func = getattr(self, "parse_{}".format(name))
            setattr(self, name, parse_func(attr_value))
        except AttributeError:
            setattr(self, name, attr_value)

    def get_handle(self, attribute):
        try:
            return self.handles[attribute]
        except KeyError:
            raise HandleNotDefined(
                "{} is not defined in `handles`.".format(
                    ATTRIBUTE_MAP_VERBOSE_NAME[attribute]
                )
            )

    def show_attributes(self, update=False):
        if update:
            self.update()
        for attr in self.attributes:
            name = ATTRIBUTE_MAP_VERBOSE_NAME[attr]
            print("{}: {}".format(name, getattr(self, name)))
