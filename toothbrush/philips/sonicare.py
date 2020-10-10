import binascii
from toothbrush.base import Toothbrush
from toothbrush.constants import *

HANDLE_MODE = 0x12
HANDLE_PROGRESS = 0x15
HANDLE_ROUTINE_LENGTH = 0x18
HANDLE_INTENSITY = 0x1F
HANDLE_DEVICE_NAME = 0x3
HANDLE_BATTERY_LEVEL = 0x3D
HANDLE_MANUFACTURER_NAME = 0x42
HANDLE_MODEL = 0x44
HANDLE_SERIAL_NUMBER = 0x46
HANDLE_HARDWARE_REVISION = 0x48
HANDLE_FIRMWARE_VERSION = 0x4A
HANDLE_SOFTWARE_REVISION = 0x4C
HANDLE_BRUSH_HEAD = 0x89

MODE_MAP = {
    b"00": "clean",
    b"01": "gum health",
    b"02": "deep clean"
}

class Sonicare(Toothbrush):
    attributes = [
        ROUTINE,
        ROUTINE_LENGTH,
        INTENSITY,
        BATTERY,
        BRUSHING_TIME,
        #PRESSURE,
        MANUFACTURER,
        MODEL_NUMBER,
        SERIAL_NUMBER,
        FIRMWARE_REVISION,
        SOFTWARE_REVISION,
        HARDWARE_REVISION,
    ]

    handles = {
        ROUTINE: HANDLE_MODE,
        ROUTINE_LENGTH: HANDLE_ROUTINE_LENGTH,
        INTENSITY: HANDLE_INTENSITY,
        BATTERY: HANDLE_BATTERY_LEVEL,
        BRUSHING_TIME: HANDLE_PROGRESS,
        MODEL_NUMBER: HANDLE_MODEL,
        FIRMWARE_REVISION: HANDLE_FIRMWARE_VERSION,
        MANUFACTURER: HANDLE_MANUFACTURER_NAME,
        SERIAL_NUMBER: HANDLE_SERIAL_NUMBER,
        HARDWARE_REVISION: HANDLE_HARDWARE_REVISION,
        SOFTWARE_REVISION: HANDLE_SOFTWARE_REVISION
    }

    def parse_routine(self, raw_data):
        return MODE_MAP[binascii.hexlify(raw_data)]

    def parse_battery(self, raw_data):
        return int(binascii.hexlify(raw_data), 16) / 100

    def parse_routine_length(self, raw_data):
        return int(binascii.hexlify(raw_data)[:2], 16)

    def parse_intensity(self, raw_data):
        return int(binascii.hexlify(raw_data))

    def parse_brushing_time(self, raw_data):
        return int(binascii.hexlify(raw_data)[:2], 16)


