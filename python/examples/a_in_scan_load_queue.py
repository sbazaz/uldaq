# -*- coding: UTF-8 -*-
"""
    Wrapper call demonstrated:        ai_device.a_in_load_queue()
    
    Purpose:                          Set up the channel gain queue for 4 A/D
                                      channels
    
    Demonstration:                    Initialize the channel gain queue
                                      
    Steps:
    1.  Call get_daq_device_inventory() to get the list of available DAQ devices
    2.  Create a DaqDevice object
    3.  Call daq_device.get_info() to get the daq_device_info object for the DAQ device
    4.  Verify that the DAQ device has an analog input subsystem
    5.  Call daq_device.connect() to establish a UL connection to the DAQ device
    6.  Call daq_device.get_ai_device() to get the ai_device object for the AI subsystem
    7.  Call ai_device.get_info() to get the ai_info object for the AI subsystem
    8.  Call ai_info.get_queue_types() to get the supported queue types for the AI subsystem
    9.  Create the channel array
    10. Call ai_device.a_in_load_queue() to load the channel gain queue
    11. Call ai_device.a_in_scan() to start the scan of A/D input channels
    12. Display the last 5 samples for each channel as long as scan is running
"""
from __future__ import print_function
from time import sleep
from os import system

from uldaq import get_daq_device_inventory, DaqDevice, AInScanFlag, AiInputMode, AiQueueElement
from uldaq import create_float_buffer, ScanOption, ScanStatus, InterfaceType, Range


def main():
    daq_device = None
    ai_device = None
    status = ScanStatus.IDLE

    low_chan = 0
    hi_chan = 3
    input_mode = AiInputMode.SINGLE_ENDED
    voltage_range = Range.BIP10VOLTS
    samples_per_channel = 10000
    rate = 1000
    scan_options = ScanOption.DEFAULTIO | ScanOption.CONTINUOUS
    flags = AInScanFlag.DEFAULT

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
        descriptor = daq_device.get_descriptor()
        print('Connecting to', descriptor.dev_string, '- please wait...')
        daq_device.connect()
        daq_device_info = daq_device.get_info()

        if not daq_device_info.has_ai_device():
            raise Exception('Error: The DAQ device does not support analog input')

        ai_device = daq_device.get_ai_device()
        ai_info = ai_device.get_info()

        if not ai_info.has_pacer():
            raise Exception('Error: The specified DAQ device does not support hardware paced analog input')
        
        queue_types = ai_info.get_queue_types()
        if len(queue_types) == 0:
            raise Exception('Error: The device does not support a gain queue')

        # assign each channel in the gain queue an input mode (SE/DIFF) and a range
        chan_count = hi_chan - low_chan + 1
        channel_gain_array = ai_queue_element_array(chan_count)
        for i in range(chan_count):
            channel_gain_array[i].channel = i
            channel_gain_array[i].input_mode = input_mode
            channel_gain_array[i].range = voltage_range

        # load the gain queue
        ai_device.a_in_load_queue(channel_gain_array)

        number_of_channels = hi_chan - low_chan + 1
        data = create_float_buffer(number_of_channels, samples_per_channel)

        print('\n', descriptor.dev_string, 'ready')
        print('    Function demonstrated: ai_device.a_in_load_queue()\n')
        print('    Channels: ', low_chan, ' - ', hi_chan)
        for i in range(chan_count):
            print('        Channel:', channel_gain_array[i].channel,
                  ', Input mode:', AiInputMode(channel_gain_array[i].input_mode).name,
                  ', Range:', Range(channel_gain_array[i].range).name)
        print('    Samples per channel: ', samples_per_channel)
        print('    Rate: ', rate, ' Hz')
        print('    Scan options:', display_scan_options(ai_info.get_scan_options(), scan_options))
        print('\n')
        input('Hit ENTER to continue\n')

        ai_device.a_in_scan(low_chan, hi_chan, input_mode, voltage_range, 
                            samples_per_channel, rate, scan_options, flags, data)
    
        while True:
    
            status, transfer_status = ai_device.get_scan_status()
    
            # use the currentIndex to display the first 5 samples of data for
            # each channel in the buffer
            if transfer_status.current_index >= 0:
                # clear the display
                system("clear")

                print('Please enter CTRL + ''\\'' to terminate the process\n\n')
    
                print('currentTotalCount = ',  transfer_status.current_total_count)
                print('currentScanCount = ',  transfer_status.current_scan_count)
                print('currentIndex = ',  transfer_status.current_index)

                index = transfer_status.current_index - number_of_channels

                # display the data
                for i in range(number_of_channels):
                    print('chan =',
                          i + low_chan, ': ',
                          '{:.6f}'.format(data[index + i]))

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
            # stop the acquisition if it is still running
            if status == ScanStatus.RUNNING:
                ai_device.scan_stop()
            if daq_device.is_connected():
                daq_device.disconnect()
            daq_device.release()

    print('DONE !!!')


def display_scan_options(supported_options, bit_mask):
    options = []
    if bit_mask == ScanOption.DEFAULTIO:
        options.append(ScanOption.DEFAULTIO.name)
    for so in supported_options:
        if so & bit_mask:
            options.append(so.name)
    return ', '.join(options)


def ai_queue_element_array(size):
    queue_element_array = AiQueueElement * size  # type: type
    return queue_element_array()


if __name__ == '__main__':
    main()
