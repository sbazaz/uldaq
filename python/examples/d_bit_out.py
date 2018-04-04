"""
    Wrapper call demonstrated:        dio_device.d_bit_out()

    Purpose:                          Reads the individual bits from
                                      the specified DIO port

    Demonstration:                    Outputs the digital output data for
                                      each bit in the digital port
    Steps:
    1. Call get_daq_device_inventory() to get the list of available DAQ devices
    2. Create a DaqDevice object
    3. Call daq_device.get_info() to get the daq_device_info object for the DAQ device
    4. Verify that the DAQ device has a digital output subsystem
    5. Call daq_device.connect() to establish a UL connection to the DAQ device
    6. Call daq_device.get_dio_device() to get the dio_device object for the digital subsystem
    7. Call dio_device.d_bit_out() to read each bit of the digital port
    8. Display the data for each bit
"""
from __future__ import print_function
from time import sleep
from os import system

from uldaq import get_daq_device_inventory, DaqDevice, InterfaceType, DigitalDirection


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
        if not daq_device_info.has_dio_device():
            raise Exception('Error: The device does not support digital output')

        descriptor = daq_device.get_descriptor()
        print('Connecting to', descriptor.dev_string, '- please wait...')
        daq_device.connect()
        dio_device = daq_device.get_dio_device()
        dio_info = dio_device.get_info()

        # get the port types for the device(Auxport, FirstportA, ...)
        port_types = dio_info.get_port_types()

        # get the port I/O type and the number of bits for the first port
        port_info = dio_info.get_port_info(port_types[0])

        # configure all of the bits for output for the first port
        for i in range(port_info.number_of_bits):
            dio_device.d_config_bit(port_types[0], i, DigitalDirection.OUTPUT)

        print('\n', descriptor.dev_string, 'ready')
        print('    Function demonstrated: dio_device.d_bit_out()')
        print('    Port: ', port_types[0].name)
        print('    Bits: 0 - 3')
        print('\n')

        bits_per_port = dio_info.get_num_bits(port_types[0])
        max_port_value = pow(2.0, bits_per_port) - 1

        while True:
            print('Enter a value  between 0 and ', max_port_value, ':  ')
            data = input()

            system('clear')
            print('Please enter CTRL + ''\\'' to terminate the process\n\n')

            for bit_number in range(bits_per_port):
                bit_value = (int(data) >> bit_number) & 1
                dio_device.d_bit_out(port_types[0], bit_number, bit_value)

                # display the channel's data
                print('Bit(', bit_number, ') Data: ', bit_value)

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
