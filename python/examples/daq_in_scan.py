# -*- coding: UTF-8 -*-

"""
    Wrapper call demonstrated:        daqi_device.daq_in_scan()

    Purpose:                          Performs a continuous scan of the
                                      analog, digital, and counter subsystems

    Demonstration:                    Displays the analog, digital, and counter
                                      input data

    Steps:
    1. Call get_daq_device_inventory() to get the list of available DAQ devices
    2. Create a DaqDevice object
    3. Call daq_device.get_info() to get the daq_device_info object for the DAQ device
    4. Verify that the DAQ device has an analog input subsystem
    5. Call daq_device.connect() to establish a UL connection to the DAQ device
    6. Call daq_device.get_daqi_device() to get the input daq_device object for the DAQI subsystem
    7. Create the analog, digital, and counter channel descriptors
    8. Call daq_device.daq_in_scan() to start the scan of daq input channels
    9. Display the last 5 samples for the scanned channels for as long as scan is running
"""
from __future__ import print_function
from time import sleep

from uldaq import InterfaceType, DaqInChanType, DaqInChanDescriptor, DaqInScanFlag, DigitalDirection
from uldaq import CounterMeasurementType, Range, ScanOption, ScanStatus, AiInputMode, get_daq_device_inventory
from uldaq import DaqDevice, create_float_buffer


def main():
    daq_device = None

    samples_per_channel = 10000
    rate = 1000.0
    options = ScanOption.DEFAULTIO | ScanOption.CONTINUOUS
    flags = DaqInScanFlag.DEFAULT

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
        if daq_device_info.has_daqi_device() is False:
            raise Exception('Error: The device does not support daq input subsystem')

        descriptor = daq_device.get_descriptor()
        print('Connecting to', descriptor.dev_string, '- please wait...')
        daq_device.connect()
        daqi_device = daq_device.get_daqi_device()
        daqi_info = daqi_device.get_info()
        
        chan_types_list = daqi_info.get_channel_types()
 
        channel_descriptors = []
        if DaqInChanType.ANALOG_SE in chan_types_list:
            configure_analog_input_channels(daq_device, channel_descriptors, DaqInChanType.ANALOG_SE)

        if DaqInChanType.DIGITAL in chan_types_list:
            configure_digital_input_channels(daq_device, channel_descriptors)

        if DaqInChanType.CTR32 in chan_types_list:
            configure_counter_input_channels(daq_device, channel_descriptors)

        number_of_scan_channels = len(channel_descriptors)

        data = create_float_buffer(number_of_scan_channels, samples_per_channel)

        rate = daqi_device.daq_in_scan(channel_descriptors, samples_per_channel, rate, options, flags, data)

        print('\n', descriptor.dev_string, 'ready')
        print('    Function demonstrated: daqi_device.daq_in_scan()')
        print('    Number of scan channels: ', number_of_scan_channels)
        for i in range(number_of_scan_channels):
            if channel_descriptors[i].type == AiInputMode.SINGLE_ENDED or \
                    channel_descriptors[i].type == AiInputMode.DIFFERENTIAL:
                print('        ScanChannel ', i,
                      ': type = ', DaqInChanType(channel_descriptors[i].type).name,
                      ', channel = ', channel_descriptors[i].channel,
                      ', range = ', Range(channel_descriptors[i].range).name)
            else:
                print('        ScanChannel ', i,
                      ': type = ', DaqInChanType(channel_descriptors[i].type).name,
                      ', channel = ', channel_descriptors[i].channel)
        print('    Samples per channel: ', samples_per_channel)
        print('    Rate: ', rate, ' Hz')
        print('\n')
        input('Hit ENTER to continue\n')

        # get the initial status of the acquisition
        status, transfer_status = daqi_device.get_scan_status()
        
        while status == ScanStatus.RUNNING:
            # get the current status of the acquisition
            status, transfer_status = daqi_device.get_scan_status()
            print('Please enter CTRL + ''\\'' to terminate the process\n\n')
           
            print('currentScanCount = ', transfer_status.current_scan_count)
            print('currentTotalCount = ', transfer_status.current_total_count)
            print('currentIndex = ', transfer_status.current_index)
    
            # set index to display the last 5 samples for each channel
            index = transfer_status.current_index - number_of_scan_channels
           
            # display the data
            for i in range(number_of_scan_channels):
               
                if channel_descriptors[i].type == DaqInChanType.ANALOG_SE \
                        or channel_descriptors[i].type == DaqInChanType.ANALOG_DIFF:
                    print('(Ai', channel_descriptors[i].channel, '): ',
                          '{:.6f}'.format(data[index + i]))

                elif channel_descriptors[i].type == DaqInChanType.DIGITAL:
                    print('(Di', channel_descriptors[i].channel, '): ',
                          '{:d}'.format(int(data[index + i])))

                else:
                    print('(Ci', channel_descriptors[i].channel, '): ',
                          '{:d}'.format(int(data[index + i])))

            # sleep to avoid flicker in the display
            sleep(1)

        # stop the acquisition if it is still running
        if status == ScanStatus.RUNNING:
            daqi_device.scan_stop()

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


def configure_analog_input_channels(daq_device, channel_descriptors, input_mode):
  
    # get the number of analog channels
    ai_device = daq_device.get_ai_device()
    ai_info = ai_device.get_info()
    number_of_channels = ai_info.get_num_chans_by_mode(input_mode)

    # fill a descriptor for each channel
    for chan in range(number_of_channels):
        descriptor = DaqInChanDescriptor(chan, DaqInChanType.ANALOG_SE, Range.BIP10VOLTS)

        channel_descriptors.append(descriptor)


def configure_digital_input_channels(daq_device, channel_descriptors):

    # get the number of analog channels
    dio_device = daq_device.get_dio_device()
    dio_info = dio_device.get_info()
    number_of_ports = dio_info.get_num_ports()

    # get the port types
    port_types = dio_info.get_port_types()

    # fill a descriptor for each channel
    for i in range(number_of_ports):
        # configure the port for input
        dio_device.d_config_port(port_types[i], DigitalDirection.INPUT)

        descriptor = DaqInChanDescriptor(port_types[i], DaqInChanType.DIGITAL)

        channel_descriptors.append(descriptor)


def configure_counter_input_channels(daq_device, channel_descriptors):

    # get the number of analog channels
    ctr_device = daq_device.get_ctr_device()
    ctr_info = ctr_device.get_info()
    number_of_counters = ctr_info.get_num_ctrs()

    # fill a descriptor for each event counter channel
    for ctr in range(number_of_counters):
        # get the measurement types
        measurement_types = ctr_info.get_measurement_types(ctr)

        if CounterMeasurementType.COUNT in measurement_types:
            descriptor = DaqInChanDescriptor(ctr, DaqInChanType.CTR32)

            channel_descriptors.append(descriptor)


if __name__ == '__main__':
    main()
