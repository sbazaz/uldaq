#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    Wrapper call demonstrated:        ai_device.a_in()
    
    Purpose:                          Reads an A/D input channel
    
    Demonstration:                    Displays the analog input data on a
                                      user-specified channel
                                      
    Steps:
    1. Call get_daq_device_inventory() to get the list of available DAQ devices
    2. Create a DaqDevice object
    3. Call daq_device.get_info() to get the daq_device_info object for the DAQ device
    4. Call daq_device_info.has_ai_device() to verify that the DAQ device has an analog input subsystem
    5. Call daq_device.connect() to establish a UL connection to the DAQ device
    6. Call daq_device.get_ai_device() to get the ai_device object for the AI subsystem
    7. Call ai_device.a_in() to read a value from an A/D input channel
    8. Display the data for each channel
"""
from __future__ import print_function
from time import sleep
from os import system

from uldaq import get_daq_device_inventory, DaqDevice, InterfaceType, AiInputMode, Range, AInFlag


def main():
    daq_device = None

    interface_type = InterfaceType.USB

    try:
        devices = get_daq_device_inventory(interface_type)
        number_of_devices = len(devices)

        if number_of_devices == 0:
            raise Exception('Error: No DAQ devices found')

        print('Found', number_of_devices, 'DAQ device(s):')
        for i in range(number_of_devices):
            print('  ', devices[i].product_name, ' (', devices[i].unique_id, ')', sep='')

        daq_device = DaqDevice(devices[0])
        daq_device_info = daq_device.get_info()

        if not daq_device_info.has_ai_device():
            raise Exception('Error: The DAQ device does not support analog input')

        descriptor = daq_device.get_descriptor()
        print('Connecting to', descriptor.dev_string, '- please wait...')
        daq_device.connect()
        ai_device = daq_device.get_ai_device()

        print('\n', descriptor.dev_string, 'ready')
        print('    Function demonstrated: ai_device.a_in()\n')
        print('    Channels: 0 - 3')
        print('    Input mode: AiInputMode.SINGLE_ENDED')
        print('    Range: Range.BIP10VOLTS')
        print('\n')
        input('Hit ENTER to continue\n')

        while True:
            system('clear')
            print('Please enter CTRL + ''\\'' to terminate the process\n\n')
             
            # display data for the first 4 analog input channels
            for channel in range(4):
                data = ai_device.a_in(channel, AiInputMode.SINGLE_ENDED, Range.BIP10VOLTS, AInFlag.DEFAULT)

                # display the channel's data
                print('Channel(', channel, ') Data: ', data)

            # sleep to avoid flicker in the display
            sleep(1)

    except KeyboardInterrupt:
        pass
    except (ValueError, NameError, SyntaxError):
        pass
    except Exception as e:
        print('\n', e)
    finally:
        if daq_device:
            if daq_device.is_connected():
                daq_device.disconnect()
            daq_device.release()

    print('DONE !!!')


if __name__ == '__main__':
    main()
