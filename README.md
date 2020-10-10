# python-toothbrush

![stability-wip](https://img.shields.io/badge/stability-work_in_progress-lightgrey.svg)


python-toothbrush is a package that provides a simple interface to connect
to electric toothbrushes via Bluetooth.

## Help Wanted
Any help is appreciated. I'd love to see support for more toothbrushes in the future!

### How to add another toothbrush?
The package assumes that a toothbrush has certain attributes (like routine, intensity, etc.).
These attributes are read via Bluetooth from the toothbrush. The toothbrush exposes these attributes in form of 
certain characteristics. Characteristics can be read via a certain handle (or address).

The package is trying to take care of the communication with the toothbrush, so you can focus on providing the correct
handles:

```python
from toothbrush.base import Toothbrush
from toothbrush.constants import ROUTINE, INTENSITY

class FancyToothbrush(Toothbrush):
    attributes = [ROUTINE, INTENSITY]  # defines which attributes are available
    handles = {                        # defines under which handle the attributes can be read
        INTENSITY: 0x11,
        ROUTINE: 0x12 
    }
```

That's pretty much it. Let's test the implementation!

```python
>>>from toothbrush.fancy import FancyToothbrush
>>>fancy = FancyToothbrush("00:11:22:33:44:55")
>>>fancy.show_attributes()
routine: b'\x01'
intensity: b'\x01'
```

You may have noticed the output of the attribute values is not human readable. So let's change that! Just
add a `parse_{attribute}` method for every attribute you'd like to parse.

```python
import binascii
from toothbrush.base import Toothbrush
from toothbrush.constants import ROUTINE, INTENSITY

class FancyToothbrush(Toothbrush):
    attributes = [ROUTINE, INTENSITY]  # defines which attributes are available
    handles = {                        # defines under which handle the attributes can be read
        INTENSITY: 0x11,
        ROUTINE: 0x12 
    }
    ROUTINE_MAP = {
        0: "simple",
        1: "gum",
        2: "deep clean"
    }

    def parse_intensity(self, raw_data):
        return int(binascii.hexlify(raw_data))

    def parse_routine(self, raw_data):
        return self.ROUTINE_MAP[int(binascii.hexlify(raw_data))]
```

```python
>>>from toothbrush.fancy import FancyToothbrush
>>>fancy = FancyToothbrush("00:11:22:33:44:55")
>>>fancy.show_attributes()
routine: 'simple'
intensity: 1
```

That's it!


## Todos
- [ ] CLI capabilities for better debugging
- [ ] JSON / XML output for toothbrush

## Supported toothbrushes
- [ ] [Philips Sonicare ExpertClean 7300](https://github.com/SteinRobert/python-toothbrush/wiki/Philips-Sonicare-ExpertClean-7300)
