"""
Created on Mar 5, 2018

@author: MCC
"""
from .ul_c_interface import lib, AoInfoItem, AoInfoItemDbl
from .ul_exception import ULException
from ctypes import c_longlong, byref, c_double, c_bool
from .ul_enums import ScanOption, Range, TriggerType
from .utils import enum_mask_to_list


class AoInfo:
    """
    Provides information about the capabilities of the analog output subsystem.
    
    Args:
        handle: UL DAQ Device handle.
    """    
    
    def __init__(self, handle):
        self.__handle = handle
        
    def get_num_chans(self):
        # type: () -> int
        """
        Gets the number of analog output channels.
        
        Returns:
            The number of analog output channels.

        Raises:
            :class:`ULException`
        """
        number_of_channels = c_longlong()
        err = lib.ulAOGetInfo(self.__handle, AoInfoItem.NUM_CHANS, 0, byref(number_of_channels))
        if err != 0:
            raise ULException(err)
        return number_of_channels.value

    def get_resolution(self):
        # type: () -> int
        """
        Gets the number of bits of resolution for an analog output samples.

        Returns:
            The number of bits per analog output sample.

        Raises:
            :class:`ULException`
        """
        resolution = c_longlong()
        err = lib.ulAOGetInfo(self.__handle, AoInfoItem.RESOLUTION, 0, byref(resolution))
        if err != 0:
            raise ULException(err)
        return resolution.value

    def get_min_scan_rate(self):
        # type: () -> float
        """
        Gets the minimum scan rate for the analog output subsystem.

        Returns:
            The minimum scan rate.

        Raises:
            :class:`ULException`
        """
        min_scan_rate = c_double()
        err = lib.ulAOGetInfoDbl(self.__handle, AoInfoItemDbl.MIN_SCAN_RATE, 0, byref(min_scan_rate))
        if err != 0:
            raise ULException(err)
        return min_scan_rate.value

    def get_max_scan_rate(self):
        # type: () -> float
        """
        Gets the maximum scan rate for the analog output subsystem.

        Returns:
            The maximum scan rate.

        Raises:
            :class:`ULException`
        """
        max_scan_rate = c_double()
        err = lib.ulAOGetInfoDbl(self.__handle, AoInfoItemDbl.MAX_SCAN_RATE, 0, byref(max_scan_rate))
        if err != 0:
            raise ULException(err)
        return max_scan_rate.value

    def get_max_throughput(self):
        # type: () -> float
        """
        Gets the maximum throughput for the analog output subsystem.

        Returns:
            The maximum throughput.

        Raises:
            :class:`ULException`
        """
        max_throughput = c_double()
        err = lib.ulAOGetInfoDbl(self.__handle, AoInfoItemDbl.MAX_THROUGHPUT, 0, byref(max_throughput))
        if err != 0:
            raise ULException(err)
        return max_throughput.value

    def get_fifo_size(self):
        # type: () -> int
        """
        Gets the size of the FIFO for the analog output subsystem.

        Returns:
            The FIFO size.

        Raises:
            :class:`ULException`
        """
        fifo_size = c_longlong()
        err = lib.ulAOGetInfo(self.__handle, AoInfoItem.FIFO_SIZE, 0, byref(fifo_size))
        if err != 0:
            raise ULException(err)
        return fifo_size.value

    def get_scan_options(self):
        # type: () -> list[ScanOption]
        """
        Gets the scan options for the analog output subsystem.

        Returns:
            A list of supported :class:`ScanOption` objects.

        Raises:
            :class:`ULException`
        """
        scan_options_mask = c_longlong()
        err = lib.ulAOGetInfo(self.__handle, AoInfoItem.SCAN_OPTIONS, 0, byref(scan_options_mask))
        if err != 0:
            raise ULException(err)
        return enum_mask_to_list(ScanOption, scan_options_mask.value)

    def has_pacer(self):
        # type: () -> bool
        """
        Determines whether or not the analog output subsystem has a hardware pacer.

        Returns:
            True if the device has an analog output hardware pacer.
            False if the device does not have an analog output hardware pacer.

        Raises:
            :class:`ULException`
        """
        has_pacer = c_longlong()
        err = lib.ulAOGetInfo(self.__handle, AoInfoItem.HAS_PACER, 0, byref(has_pacer))
        if err != 0:
            raise ULException(err)
        return c_bool(has_pacer).value

    def get_ranges(self):
        # type: () -> list[Range]
        """
        Gets the ranges supported by the device.

        Returns:
            A list of supported :class:`Range` objects.

        Raises:
            :class:`ULException`
        """
        num_ranges = c_longlong()
        ao_range = c_longlong()
        ao_range_list = []

        err = lib.ulAOGetInfo(self.__handle, AoInfoItem.NUM_RANGES, 0, byref(num_ranges))
        if err != 0:
            raise ULException(err)

        for i in range(num_ranges.value):
            err = lib.ulAOGetInfo(self.__handle, AoInfoItem.RANGE, i, byref(ao_range))
            if err != 0:
                raise ULException(err)
            ao_range_list.append(Range(ao_range.value))

        return ao_range_list

    def get_trigger_types(self):
        # type: () -> list[TriggerType]
        """
        Gets the supported trigger types of the analog output subsystem.

        Returns:
            A list of supported :class:`TriggerType` objects.

        Raises:
            :class:`ULException`
        """
        trigger_types_mask = c_longlong()
        err = lib.ulAOGetInfo(self.__handle, AoInfoItem.TRIG_TYPES, 0, byref(trigger_types_mask))
        if err != 0:
            raise ULException(err)
        return enum_mask_to_list(TriggerType, trigger_types_mask.value)
