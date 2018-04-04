"""
Created on Feb 12 2018

@author: MCC
"""
from ctypes import c_uint, byref, c_ulonglong, c_double
from .ul_enums import InterfaceType
from .ul_structs import DaqDeviceDescriptor
from .ul_exception import ULException
from .ul_c_interface import lib


def get_daq_device_inventory(interface_type, number_of_devices=100):
    # type: (InterfaceType) -> list[DaqDeviceDescriptor]
    """
    Gets a list of available DAQ devices.

    Returns:
        A list of :class:`DaqDeviceDescriptor` objects.

    Raises:
        :class:`ULException`
    """
    device_descriptors = daq_device_descriptor_array(number_of_devices)
    number_of_devices = c_uint(number_of_devices)
    err = lib.ulGetDaqDeviceInventory(interface_type, device_descriptors, byref(number_of_devices))
    if err != 0:
        raise ULException(err)

    devices_list = [device_descriptors[i] for i in range(number_of_devices.value)]
    return devices_list


def create_float_buffer(number_of_channels, samples_per_channel):
    # type: () -> list[float]
    """
    Create a buffer for double precision floating point sample values.

    Args:
        number_of_channels: Number of channels in the scan.
        samples_per_channel: Number samples per channel to be stored in the buffer.

    Returns:
        An array of size number_of_channels * samples_per_channel
    """
    dbl_array = c_double * (number_of_channels * samples_per_channel)  # type: type
    return dbl_array()


def create_int_buffer(number_of_channels, samples_per_channel):
    # type: () -> list[int]
    """
    Create a buffer for 64-bit unsigned integer sample values.

    Args:
        number_of_channels: Number of channels in the scan.
        samples_per_channel: Number samples per channel to be stored in the buffer.

    Returns:
        An array of size number_of_channels * samples_per_channel
    """
    ull_array = c_ulonglong * (number_of_channels * samples_per_channel)  # type: type
    return ull_array()


def daq_device_descriptor_array(size):
    descriptors_array = DaqDeviceDescriptor * size  # type: type
    return descriptors_array()


def enum_mask_to_list(enum_type, mask):
    enum_value_list = []
    for opt in enum_type:
        if opt & mask:
            enum_value_list.append(opt)
    return enum_value_list
