# -*- coding: UTF-8 -*-

"""
    Wrapper call demonstrated:        daq_device.enable_event()
    
    Purpose:                          Set up a callback function to process 
                                      events from the UL
    
    Demonstration:                    Uses a callback function to display data 
                                      using the DaqEventType.ON_DATA_AVAILABLE 
                                      event
                                      
    Steps:
    1.  Call get_daq_device_inventory() to get the list of available DAQ devices
    2.  Create a DaqDevice object
    3.  Call daq_device.get_info() to get the daq_device_info object for the DAQ device
    4.  Call daq_device_info.has_ai_device() to verify that the DAQ device has an analog input subsystem
    5.  Call daq_device.connect() to establish a UL connection to the DAQ device
    6.  Call daq_device.get_ai_device() to get the ai_device object for the AI subsystem
    7.  Initialize the ScanEventParameters structure used to pass parameters to the callback function
    8.  Call Daq_Device.enable_event to enable the DE_ON_DATA_AVAILABLE event
    9.  Call ai_device.a_in_scan() to start a finite scan of of 10000 samples
    10. The callback is called each time 1000 samples are available to allow the data to be displayed
    11. Call ai_device.a_in_scan_wait() to wait for the finite scan to complete
"""
from __future__ import print_function
from os import system
from ctypes import c_double, c_int, Structure, POINTER

from uldaq import get_daq_device_inventory, DaqDevice, AInScanFlag, DaqEventType, WaitType, ScanOption
from uldaq import InterfaceType, AiInputMode, Range, create_float_buffer

    
class ScanEventParameters(Structure):
    _fields_ = [("buffer", POINTER(c_double)),  # data buffer
                ("low_chan", c_int),             # first channel in acquisition
                ("high_chan", c_int),            # last channel in acquisition
                ("err", c_int)]                 # UL error returned from callback function


def main():
    daq_device = None
    ai_device = None

    low_chan = 0
    hi_chan = 3
    input_mode = AiInputMode.SINGLE_ENDED
    voltage_range = Range.BIP10VOLTS
    samples_per_channel = 10000
    rate = 1000
    scan_options = ScanOption.DEFAULTIO
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

        number_of_channels = hi_chan - low_chan + 1
        data = create_float_buffer(number_of_channels, samples_per_channel)

        # store the scan event parameters for use in the callback function
        scan_event_parameters = ScanEventParameters()
        scan_event_parameters.buffer = data
        scan_event_parameters.low_chan = low_chan
        scan_event_parameters.high_chan = hi_chan

        # enable the event to be notified every time 100 samples are available
        available_sample_count = 1000
        daq_device.enable_event(DaqEventType.ON_DATA_AVAILABLE, available_sample_count, event_callback_function,
                                scan_event_parameters)

        print('\n', descriptor.dev_string, 'ready')
        print('    Function demonstrated: daq_device.enable_event()\n')
        print('    Channels: ', low_chan, ' - ', hi_chan)
        print('    Input mode: ', input_mode.name)
        print('    Range: ', voltage_range.name)
        print('    Samples per channel: ', samples_per_channel)
        print('    Rate: ', rate, ' Hz')
        print('    Scan options:', display_scan_options(ai_info.get_scan_options(), scan_options))
        print('\n')
        input('Hit ENTER to continue\n')

        ai_device.a_in_scan(low_chan, hi_chan, input_mode, voltage_range, samples_per_channel, rate, scan_options,
                            flags, data)

        # wait forever
        time_to_wait = -1
        ai_device.a_in_scan_wait(WaitType.WAIT_UNTIL_DONE, time_to_wait)

    except KeyboardInterrupt:
        pass
    except (ValueError, NameError, SyntaxError):
        pass
    except Exception as e:
        print('\n', e)
    finally:
        if daq_device:
            # stop the acquisition if it is still running
            if ai_device:
                ai_device.scan_stop()
            if daq_device.is_connected():
                daq_device.disconnect()
            daq_device.release()

    print('DONE !!!')


def event_callback_function(event_type, event_data, user_data):
    scan_event_parameters = user_data
    total_samples = event_data

    print('event_type = ', event_type)
    print('event_data = ', event_data)
    print('user_data = ', user_data)

    # clear the display
    system("clear")

    print('Please enter CTRL + ''\\'' to terminate the process\n\n')

    print('currentTotalCount = ',  total_samples)

    # display the data
    # set index to display the last 5 samples for each channel
    chan_count = scan_event_parameters.high_chan - scan_event_parameters.low_chan + 1
    index = total_samples - chan_count

    for i in range(chan_count):
        print('chan =',
              i + scan_event_parameters.low_chan,
              '{:.6f}'.format(scan_event_parameters.buffer[index + i]))

    return True


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
