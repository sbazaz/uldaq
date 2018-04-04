#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    UL call demonstrated:             CtrDevice.ctr_in()

    Purpose:                          Reads a single counter value

    Demonstration:                    Read a single value from each
                                      counter input channel

    Steps:
    1.  Call the static function get_daq_device_inventory() to get the list of available DAQ devices
    2.  Create a DaqDevice object
    3.  Call DaqDevice.connect() to connect to the device
    4.  Call DaqDevice.get_info() to get the DaqDeviceInfo object for the device
    5.  Call DaqDeviceInfo.has_ctr_device() to verify that the device has an counter subsystem
    6.  Call DaqDevice.get_ctr_device() to get the CtrDevice object for the counter subsystem
    7.  Call BufferManager.create_int_buffer() to create an output buffer.
    8.  Call CtrDevice.c_load() to reset the count to zero.
    9.  Call CtrDevice.c_in_scan() to start a scan for the specified number of counters
    10. Call CtrDevice.get_scan_status() in a loop and display the last
        value in the buffer from each counter
"""
from __future__ import print_function
from time import sleep
from sys import stdout

from uldaq import get_daq_device_inventory, DaqDevice, create_int_buffer, InterfaceType
from uldaq import CInScanFlag, CounterRegisterType, ScanStatus, ScanOption


def main():
    low_counter = 0
    high_counter = 1
    sample_rate = 10000.0  # Hz
    samples_per_channel = int(sample_rate * 2.0)  # 2 second buffer
    scan_options = ScanOption.CONTINUOUS
    scan_flags = CInScanFlag.DEFAULT
    interface_type = InterfaceType.USB
    daq_device = None
    ctr_device = None

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

        print('\n', descriptor.dev_string, 'ready')
        print('    Function demonstrated: CtrDevice.c_in_scan')
        print('    Counter(s):', low_counter, '-', high_counter)
        print('    Sample rate:', sample_rate, 'Hz')
        print('    Scan options:', display_scan_options(ctr_info.get_scan_options(), scan_options))
        print('\n*Press Ctrl-C to stop scan')

        print('\n  ', end='')
        for counter_number in range(low_counter, high_counter + 1):
            ctr_device.c_load(counter_number, CounterRegisterType.LOAD, 0)
            print('   Counter', str(counter_number).rjust(2), sep='', end='')
        print('')

        data = create_int_buffer((high_counter - low_counter + 1), samples_per_channel)
        ctr_device.c_in_scan(low_counter, high_counter, samples_per_channel,
                             sample_rate, scan_options, scan_flags, data)

        try:
            while True:
                try:
                    print('\r  ', end='')
                    for counter_number in range(low_counter, high_counter + 1):
                        scan_status, transfer_status = ctr_device.get_scan_status()
                        if scan_status != ScanStatus.RUNNING:
                            break
                        counter_value = data[transfer_status.current_index - counter_number]
                        print(str(counter_value).rjust(12), end='')
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
            if ctr_device:
                ctr_device.scan_stop()
            if daq_device.is_connected():
                daq_device.disconnect()
            daq_device.release()
        print('\n\nDone!')

    return


def display_scan_options(supported_options, bit_mask):
    options = []
    if bit_mask == ScanOption.DEFAULTIO:
        options.append(ScanOption.DEFAULTIO.name)
    for so in supported_options:
        if so & bit_mask:
            options.append(so.name)
    return ', '.join(options)


if __name__ == '__main__':
    main()
