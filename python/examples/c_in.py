#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    UL call demonstrated:             CtrDevice.ctr_in()

    Purpose:                          Reads a single counter value

    Demonstration:                    Read a single value from each
                                      counter input channel

    Steps:
    1. Call the static function get_daq_device_inventory() to get the list of available DAQ devices
    2. Create a DaqDevice object
    3. Call DaqDevice.connect() to connect to the device
    4. Call DaqDevice.get_info() to get the DaqDeviceInfo object for the device
    5. Call DaqDeviceInfo.has_ctr_device() to verify that the device has an counter subsystem
    6. Call DaqDevice.get_ctr_device() to get the CtrDevice object for the counter subsystem
    7. Call CtrDevice.c_load() to reset the count to zero
    8. Call CtrDevice.c_in() to read a single value from the specified counter
"""
from __future__ import print_function
from time import sleep
from sys import stdout

from uldaq import get_daq_device_inventory, DaqDevice, InterfaceType, CounterRegisterType


def main():
    counter_number = 0
    interface_type = InterfaceType.USB
    daq_device = None

    try:
        devices = get_daq_device_inventory(interface_type)
        number_of_devices = len(devices)

        if number_of_devices == 0:
            raise Exception('Error: No DAQ devices found')

        print('Found', number_of_devices, 'DAQ device(s):')
        for i in range(number_of_devices):
            print('    ', devices[i].product_name, ' (', devices[i].unique_id, ')', sep='')

        daq_device = DaqDevice(devices[0])
        descriptor = daq_device.get_descriptor()
        print('Connecting to', descriptor.dev_string, '- please wait...')
        daq_device.connect()
        daq_device_info = daq_device.get_info()

        if not daq_device_info.has_ctr_device():
            raise Exception('Error: The DAQ device does not support counters')

        ctr_device = daq_device.get_ctr_device()
        ctr_info = ctr_device.get_info()
        dev_num_counters = ctr_info.get_num_ctrs()
        if counter_number > dev_num_counters:
            counter_number = dev_num_counters

        print('\n', descriptor.dev_string, 'ready')
        print('    Function demonstrated: CtrDevice.c_in')
        print('\n*Press Ctrl-C to stop')

        ctr_device.c_load(counter_number, CounterRegisterType.LOAD, 0)
        try:
            while True:
                try:
                    counter_value = ctr_device.c_in(counter_number)
                    print('\r    Counter ', counter_number, ':', repr(counter_value).rjust(12), sep='', end='')
                    stdout.flush()
                    sleep(1)
                except (ValueError, NameError, SyntaxError):
                    break
        except KeyboardInterrupt:
            pass

    except Exception as e:
        print('\n', e)

    finally:
        if daq_device:
            if daq_device.is_connected():
                daq_device.disconnect()
            daq_device.release()
        print('\n\nDone!')


if __name__ == '__main__':
    main()
