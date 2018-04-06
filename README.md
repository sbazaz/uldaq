## Universal Library for Linux - Python API

### About
---------
The **uldaq** Python package contains an API (Application Programming Interface)
for interacting with Measurement Computing DAQ devices. The package is implemented
as an object-oriented wrapper around the UL for Linux C API using the [ctypes](https://docs.python.org/2/library/ctypes.html) Python library.

**uldaq** supports CPython 2.7, 3.4+

### Installation
----------------
The **uldaq** Python package is installed automatically for the default python and python3
interpreters as part of the UL for Linux C API installation.  To update or install the
**uldaq** Python package for other Python interpreter versions, get the latest [source](https://github.com/sbazaz/uldaq/tree/master/python) and run:

 ```
    $ python setup.py install
 ```

### Usage
---------
The following is a simple example for reading a single voltage value from each channel in
an analog input subsystem of a Measurement Computing DAQ device.

 ```python
 >>> from uldaq import get_daq_device_inventory, DaqDevice, InterfaceType, AiInputMode, Range, AInFlag
 >>> devices = get_daq_device_inventory(InterfaceType.USB)
 >>> daq_device = DaqDevice(devices[0])
 >>> daq_device.connect()
 >>> ai_device = daq_device.get_ai_device()
 >>> ai_info = ai_device.get_info()
 >>> for channel in range(ai_info.get_num_chans()):
 ...     data = ai_device.a_in(channel, AiInputMode.SINGLE_ENDED, Range.BIP10VOLTS, AInFlag.DEFAULT)
 ...     print('Channel', channel, 'Data:', data)
 ...
 >>> daq_device.disconnect()
 >>> daq_device.release()
 ```

The same example using a with block:

 ```python
 >>> from uldaq import get_daq_device_inventory, DaqDevice, InterfaceType, AiInputMode, Range, AInFlag
 >>> devices = get_daq_device_inventory(InterfaceType.USB)
 >>> with DaqDevice(devices[0]) as daq_device:
 ...     ai_device = daq_device.get_ai_device()
 ...     ai_info = ai_device.get_info()
 ...     for channel in range(ai_info.get_num_chans()):
 ...         data = ai_device.a_in(channel, AiInputMode.SINGLE_ENDED, Range.BIP10VOLTS, AInFlag.DEFAULT)
 ...         print('Channel', channel, 'Data:', data)
 ...
 ```

### Additional Documentation
----------------------------
The complete **uldaq** Python documentation can be found [here](http://www.mccdaq.com).

### License
-----------
The **uldaq** library is licensed under an MIT-style license (see [LICENSE](https://github.com/sbazaz/uldaq/blob/master/LICENSE)).
Other incorporated projects may be licensed under different licenses. All
licenses allow for non-commercial and commercial use.
