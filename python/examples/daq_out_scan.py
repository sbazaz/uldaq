#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    UL call demonstrated:             DaqoDevice.daq_out_scan()

    Purpose:                          Synchronous output on analog and
                                      digital output channels

    Demonstration:                    Continuously output a sine wave on all
                                      analog output channels and a square wave
                                      on all digital output channels
                                      synchronously

    Steps:
    1.  Call the static function get_daq_device_inventory() to get the list of available DAQ devices
    2. Create a DaqDevice object
    3.  Call DaqDevice.connect() to connect to the device
    4.  Call DaqDevice.get_info() to get the DaqDeviceInfo object for the device
    5.  Call DaqDeviceInfo.has_daqo_device() to verify that the device has a DAQ output subsystem
    6.  Call DaqDevice.get_daqo_device() to get the DaqoDevice object for the DAQ output subsystem
    7.  Call DaqoDevice.daq_out_scan() to output the waveforms
    8.  Call DaqoDevice.get_scan_status() to get the scan status and display the status.
    9.  Call DaqoDevice.scan_stop() to stop the scan
"""
from __future__ import print_function
from math import pi, sin, ceil
from time import sleep
from sys import stdout

from uldaq import get_daq_device_inventory, DaqDevice, create_float_buffer, InterfaceType, DaqOutScanFlag, ScanOption
from uldaq import DigitalDirection, ScanStatus, DaqOutChanType, DaqOutChanDescriptor


def main():
    interface_type = InterfaceType.USB
    sample_rate = 10000  # Hz
    out_waveform_freq = 10  # Hz - sine wave
    out_waveform_amplitude = 1  # Volts peak
    scan_options = ScanOption.CONTINUOUS
    scan_flags = DaqOutScanFlag.DEFAULT
    daq_device = None
    daqo_device = None

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

        if not daq_device_info.has_daqo_device():
            raise Exception('Error: The DAQ device does not support DAQ output')

        daqo_device = daq_device.get_daqo_device()
        daqo_info = daqo_device.get_info()

        samples_per_cycle = int(sample_rate / out_waveform_freq)
        samples_per_channel = int(samples_per_cycle * (ceil(sample_rate * 2 / samples_per_cycle)))

        channel_descriptors = []
        configure_analog_channels(daq_device, channel_descriptors)
        configure_digital_channels(daq_device, channel_descriptors)

        num_channels = len(channel_descriptors)

        out_buffer = create_float_buffer(num_channels, samples_per_channel)
        create_output_data(channel_descriptors, samples_per_channel, samples_per_cycle,
                           out_waveform_amplitude, out_buffer)

        sample_rate = daqo_device.daq_out_scan(channel_descriptors, samples_per_channel, sample_rate,
                                               scan_options, scan_flags, out_buffer)

        print('\n', descriptor.dev_string, 'ready')
        print('    Analog Output Channels:', out_waveform_amplitude, 'V peak,', out_waveform_freq, 'Hz sine wave')
        print('    Digital Output Channels:', out_waveform_freq, 'Hz square wave')
        print('    Sample Rate:', sample_rate, 'Hz')
        print('    Scan options:', display_scan_options(daqo_info.get_scan_options(), scan_options))
        print('\n*Press Ctrl-C to stop scan')

        try:
            while True:
                sleep(0.1)
                scan_status, transfer_status = daqo_device.get_scan_status()
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
            if daqo_device:
                daqo_device.scan_stop()
            if daq_device.is_connected():
                daq_device.disconnect()
            daq_device.release()
        print('\n\nDone!')


def configure_analog_channels(daq_device, channel_descriptors):
    """Add all available analog output channels to the channel_descriptors list."""
    ao_device = daq_device.get_ao_device()
    ao_info = ao_device.get_info()
    output_range = ao_info.get_ranges()[0]  # Select the first supported range
    num_chans = ao_info.get_num_chans()

    for chan in range(num_chans):
        descriptor = DaqOutChanDescriptor(chan, DaqOutChanType.ANALOG, output_range)
        channel_descriptors.append(descriptor)


def configure_digital_channels(daq_device, channel_descriptors):
    """Add all available digital output channels to the channel_descriptors list."""
    dio_device = daq_device.get_dio_device()
    dio_info = dio_device.get_info()
    port_types = dio_info.get_port_types()

    for pt in port_types:
        dio_device.d_config_port(pt, DigitalDirection.OUTPUT)
        descriptor = DaqOutChanDescriptor(pt, DaqOutChanType.DIGITAL)
        channel_descriptors.append(descriptor)


def create_output_data(channel_descriptors, samples_per_channel, samples_per_cycle, amplitude, data_buffer):
    """Populate the buffer with data (sine wave for analog channels, square wave for digital channels)."""
    cycles_per_buffer = int(samples_per_channel / samples_per_cycle)
    i = 0
    for cycle in range(cycles_per_buffer):
        for sample in range(samples_per_cycle):
            for chan in channel_descriptors:
                if chan.type == DaqOutChanType.ANALOG:
                    offset = amplitude if chan.range > 1000 else 0.0
                    data_buffer[i] = amplitude * sin(2 * pi * sample / samples_per_cycle) + offset
                else:
                    data_buffer[i] = round(sample / samples_per_cycle) * float(0xFFFF)
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
