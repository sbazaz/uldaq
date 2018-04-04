#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    UL call demonstrated:             AoDevice.a_out_scan()

    Purpose:                          Continuously output a waveform
                                      on a D/A output channel

    Demonstration:                    Outputs a sine wave on the specified
                                      D/A output channels

    Steps:
    1.  Call the static function get_daq_device_inventory() to get the list of available DAQ devices
    2.  Create a DaqDevice object
    3.  Call DaqDevice.connect() to connect to the device
    4.  Call DaqDevice.get_info() to get the DaqDeviceInfo object for the device
    5.  Call DaqDeviceInfo.has_ao_device() to verify that the device has an analog output subsystem
    6.  Call DaqDevice.get_ao_device() to get the AoDevice object for the analog output subsystem
    7.  Call AoInfo.has_pacer() to verify that the analog output subsystem has a hardware pacer.
    8.  Call AoDevice.a_out_scan() to output the waveform to a D/A channel
    9.  Call AoDevice.get_scan_status() to get the scan status and display the status.
    10. Call AoDevice.scan_stop() to stop the scan
"""
from __future__ import print_function
from math import pi, sin, ceil
from time import sleep
from sys import stdout

from uldaq import get_daq_device_inventory, DaqDevice, create_float_buffer
from uldaq import InterfaceType, AOutScanFlag, ScanOption, ScanStatus


def main():
    interface_type = InterfaceType.USB
    low_channel = 0
    num_channels = 1
    sample_rate = 10000  # Hz
    out_waveform_freq = 10  # Hz - sine wave
    out_waveform_amplitude = 1  # Volts peak
    scan_options = ScanOption.CONTINUOUS
    scan_flags = AOutScanFlag.DEFAULT
    daq_device = None
    ao_device = None

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
        ao_info = ao_device.get_info()

        if not ao_info.has_pacer():
            raise Exception('Error: The DAQ device does not support paced analog output')

        chan_string = str(low_channel)
        if num_channels > 1:
            chan_string = ' '.join((chan_string, '-', str(low_channel + num_channels - 1)))

        output_range = ao_info.get_ranges()[0]  # Select the first supported range
        offset = out_waveform_amplitude if output_range > 1000 else 0  # Set an offset if the range is unipolar
        samples_per_cycle = int(sample_rate / out_waveform_freq)
        samples_per_channel = int(samples_per_cycle * (ceil(sample_rate * 2 / samples_per_cycle)))

        out_buffer = create_float_buffer(num_channels, samples_per_channel)
        create_output_data(num_channels, samples_per_channel, samples_per_cycle,
                           out_waveform_amplitude, offset, out_buffer)

        sample_rate = ao_device.a_out_scan(low_channel, low_channel + num_channels - 1, output_range,
                                           samples_per_channel, sample_rate, scan_options, scan_flags, out_buffer)

        print('\n', descriptor.dev_string, 'ready')
        print('    Output:', out_waveform_amplitude, 'V peak,', out_waveform_freq, 'Hz sine wave')
        print('    Channel(s):', chan_string)
        print('    Range:', output_range.name)
        print('    Sample Rate:', sample_rate, 'Hz')
        print('    Scan options:', display_scan_options(ao_info.get_scan_options(), scan_options))
        print('\n*Press Ctrl-C to stop scan')

        try:
            while True:
                sleep(0.1)
                scan_status, transfer_status = ao_device.get_scan_status()
                if scan_status != ScanStatus.RUNNING:
                    break
                print('\r    Output sample count:', transfer_status.current_scan_count, end='')
                stdout.flush()
        except KeyboardInterrupt:
            pass

    except Exception as e:
        print('\n', e)

    finally:
        if daq_device:
            if ao_device:
                ao_device.scan_stop()
            if daq_device.is_connected():
                daq_device.disconnect()
            daq_device.release()
        print('\n\nDone!')


def create_output_data(number_of_channels, samples_per_channel, samples_per_cycle, amplitude, offset, data_buffer):
    """Populate the buffer with sine wave data for the specified number of channels."""
    cycles_per_buffer = int(samples_per_channel / samples_per_cycle)
    i = 0
    for cycle in range(cycles_per_buffer):
        for sample in range(samples_per_cycle):
            for chan in range(number_of_channels):
                data_buffer[i] = amplitude * sin(2 * pi * sample / samples_per_cycle) + offset
                i += 1


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
