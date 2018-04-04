#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    UL call demonstrated:             TmrDevice.pulse_out_start()

    Purpose:                          Continuous timer pulse output

    Demonstration:                    Generates a pulse output on the
                                      specified timer

    Steps:
    1.  Call the static function get_daq_device_inventory() to get the list of available DAQ devices
    2.  Create a DaqDevice object
    3.  Call DaqDevice.connect() to connect to the device
    4.  Call DaqDevice.get_info() to get the DaqDeviceInfo object for the device
    5.  Call DaqDeviceInfo.has_tmr_device() to verify that the device has an timer subsystem
    6.  Call DaqDevice.get_tmr_device() to get the TmrDevice object for the timer subsystem
    7.  Call TmrDevice.pulse_out_start() to start the pulse output.
    8.  Call TmrDevice.get_pulse_out_status() to get the pulse output status and display the status.
    9.  Call TmrDevice.pulse_out_stop() to stop the pulse output.
"""
from __future__ import print_function
from time import sleep
from sys import stdout

from uldaq import get_daq_device_inventory, DaqDevice, InterfaceType, TmrIdleState, PulseOutOption


def main():
    timer_number = 0
    frequency = 1000.0  # Hz
    duty_cycle = 0.5  # 50 percent
    pulse_count = 0  # Continuous
    initial_delay = 0.0
    idle_state = TmrIdleState.LOW
    options = PulseOutOption.PO_DEFAULT
    interface_type = InterfaceType.USB
    daq_device = None
    tmr_device = None

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

        if not daq_device_info.has_tmr_device():
            raise Exception('Error: The DAQ device does not support analog output')

        tmr_device = daq_device.get_tmr_device()

        frequency, duty_cycle, initial_delay = tmr_device.pulse_out_start(timer_number, frequency, duty_cycle,
                                                                          pulse_count, initial_delay, idle_state,
                                                                          options)

        print('\n', descriptor.dev_string, 'ready')
        print('    Timer:', timer_number)
        print('    Frequency:', frequency, 'Hz')
        print('    Duty cycle:', duty_cycle)
        print('    Initial delay:', initial_delay)
        print('\n*Press Ctrl-C to stop scan')

        count = 0
        try:
            while True:
                sleep(0.5)
                print('\r    Running', end='')
                for i in range(count % 4):
                    print('.', end='')
                print('   ', end='')
                count += 1
                stdout.flush()
        except KeyboardInterrupt:
            pass

    except Exception as e:
        print('\n', e)

    finally:
        if daq_device:
            if tmr_device:
                tmr_device.pulse_out_stop(timer_number)
                print('\r    Stopped.  ', end='')
            if daq_device.is_connected():
                daq_device.disconnect()
            daq_device.release()
        print('\n\nDone!')


if __name__ == '__main__':
    main()
