# -*- coding: UTF-8 -*-

"""
    Wrapper call demonstrated:        dio_device.d_out_scan()

    Purpose:                          Performs continuous output
                                      to the digital port

    Demonstration:                    Writes the digital output data to
                                      the user-specified digital port

    Steps:
    1. Call get_daq_device_inventory() to get the list of available DAQ devices
    2. Create a DaqDevice object
    3. Call daq_device.get_info() to get the daq_device_info object for the DAQ device
    4. Verify that the DAQ device has an analog output subsystem
    5. Call daq_device.connect() to establish a UL connection to the DAQ device
    6. Call daq_device.get_di_device() to get the di_device object for the AI subsystem
    7. Call dio_device.d_out_scan() to start the scan of digital output port
    8. Display the last 5 samples for for the port as long as scan is running
"""
from __future__ import print_function
from time import sleep
from os import system

from uldaq import get_daq_device_inventory, DaqDevice, DigitalDirection, ScanOption, ScanStatus
from uldaq import create_int_buffer, InterfaceType, DOutScanFlag


def main():
    daq_device = None
    dio_device = None
    status = ScanStatus.IDLE

    samples_per_channel = 10000
    rate = 1000
    scan_options = ScanOption.CONTINUOUS
    flags = DOutScanFlag.DEFAULT

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
        if not daq_device_info.has_dio_device():
            raise Exception('Error: The DAQ device does not support digital input')

        dio_device = daq_device.get_dio_device()
        dio_info = dio_device.get_info()

        has_pacer = dio_info.has_pacer(DigitalDirection.INPUT)
        if not has_pacer:
            raise Exception('Error: The specified DAQ device does not support hardware paced digital input')

        descriptor = daq_device.get_descriptor()
        print('Connecting to', descriptor.dev_string, '- please wait...')
        daq_device.connect()

        port_types = dio_info.get_port_types()
        dio_device.d_config_port(port_types[0], DigitalDirection.OUTPUT)

        low_port = port_types[0]
        hi_port = port_types[0]

        number_of_ports = hi_port - low_port + 1
        data = create_int_buffer(number_of_ports, samples_per_channel)

        print('\n', descriptor.dev_string, 'ready')
        print('    Function demonstrated: dio_device.d_out_scan()')
        print('    Port: ', low_port.name)
        print('    Samples per channel: ', samples_per_channel)
        print('    Rate: ', rate, ' Hz')
        print('    Scan options:', display_scan_options(dio_info.get_scan_options(DigitalDirection.OUTPUT),
                                                        scan_options))
        print('\n')
        input('Hit ENTER to continue\n')

        create_output_data(number_of_ports, samples_per_channel, data)

        dio_device.d_out_scan(low_port, hi_port, samples_per_channel, rate, scan_options, flags, data)

        while True:

            status, transfer_status = dio_device.d_out_get_scan_status()

            # use the currentIndex to display the first 5 samples of data for each channel in the buffer
            if transfer_status.current_index >= 0:
                # clear the display
                system("clear")

                print('Please enter CTRL + ''\\'' to terminate the process\n\n')

                print('currentTotalCount = ', transfer_status.current_total_count)
                print('currentScanCount = ', transfer_status.current_scan_count)
                print('currentIndex = ', transfer_status.current_index)

                index = transfer_status.current_index - number_of_ports

                # display the data
                for i in range(number_of_ports):
                    print('port =',
                          port_types[i].name, ': ',
                          '{:d}'.format(data[index + i]))

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
                dio_device.d_out_scan_stop()
            if daq_device.is_connected():
                daq_device.disconnect()
            daq_device.release()

    print('DONE !!!')


def create_output_data(number_of_channels, number_of_samples_per_channel, data_buffer):
    for i in range(number_of_samples_per_channel):
        for j in range(number_of_channels):
            index = (i * number_of_channels) + j

            if i < number_of_samples_per_channel / 2:
                data_buffer[index] = 1
            else:
                data_buffer[index] = 0


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
