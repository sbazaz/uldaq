#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    UL call demonstrated:             AoDevice.a_out()

    Purpose:                          Writes to a D/A output channel

    Demonstration:                    Outputs a user-specified voltage
                                      on analog output channel 0

    Steps:
    1. Call the static function get_daq_device_inventory() to get the list of available DAQ devices
    2. Create a DaqDevice object
    3. Call DaqDevice.connect() to connect to the device
    4. Call DaqDevice.get_info() to get the DaqDeviceInfo object for the device
    5. Call DaqDeviceInfo.has_ao_device() to verify that the device has an analog output subsystem
    6. Call DaqDevice.get_ao_device() to get the AoDevice object for the analog output subsystem
    7. Call AoDevice.a_out() to write a value to a D/A output channel
"""
from __future__ import print_function

from uldaq import get_daq_device_inventory, DaqDevice, InterfaceType, Range, AOutFlag


def main():
    interface_type = InterfaceType.USB
    output_channel = 0
    output_range = Range.BIP10VOLTS
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

        if not daq_device_info.has_ao_device():
            raise Exception('Error: The DAQ device does not support analog output')

        ao_device = daq_device.get_ao_device()

        print('\n', descriptor.dev_string, 'ready')
        print('    Channel:', output_channel)
        print('    Range:', output_range.name)
        print('\n*Enter non-numeric value to stop')

        try:
            while True:
                try:
                    out_val = input('    Enter output value (V): ')
                    ao_device.a_out(output_channel, output_range, AOutFlag.DEFAULT, float(out_val))
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
        print('\nDone!')


if __name__ == '__main__':
    main()
