
from ctypes import c_longlong, c_double, byref
from .ul_enums import DaqInChanType, ScanOption, TriggerType
from .ul_exception import ULException
from .ul_c_interface import lib, DaqIInfoItem, DaqIInfoItemDbl
from .utils import enum_mask_to_list


class DaqiInfo:
    """
    Provides information about the capabilities of the DAQ input subsystem.

    Args:
        handle: UL DAQ Device handle.
    """

    def __init__(self, handle):
        self.__handle = handle

    def get_channel_types(self):
        # type: () -> list[DaqInChanType]
        """
        Gets a the supported channel types for the DAQ Input subsystem.

        Returns:
            A list of supported :class:`DaqInChanType` objects

        Raises:
            :class:`ULException`
        """
        chan_types_mask = c_longlong()
        err = lib.ulDaqIGetInfo(self.__handle, DaqIInfoItem.CHAN_TYPES, 0, byref(chan_types_mask))
        if err != 0:
            raise ULException(err)
        return enum_mask_to_list(DaqInChanType, chan_types_mask.value)

    def get_min_scan_rate(self):
        # type: () -> float
        """
        Gets the minimum scan rate for the DAQ input subsystem.

        Returns:
            The minimum scan rate.

        Raises:
            :class:`ULException`
        """
        min_scan_rate = c_double()
        err = lib.ulDaqIGetInfoDbl(self.__handle, DaqIInfoItemDbl.MIN_SCAN_RATE, 0, byref(min_scan_rate))
        if err != 0:
            raise ULException(err)
        return min_scan_rate.value

    def get_max_scan_rate(self):
        # type: () -> float
        """
        Gets the maximum scan rate for the DAQ input subsystem.

        Returns:
            The maximum scan rate.

        Raises:
            :class:`ULException`
        """
        max_scan_rate = c_double()
        err = lib.ulDaqIGetInfoDbl(self.__handle, DaqIInfoItemDbl.MAX_SCAN_RATE, 0, byref(max_scan_rate))
        if err != 0:
            raise ULException(err)
        return max_scan_rate.value

    def get_max_throughput(self):
        # type: () -> float
        """
        Gets the maximum throughput for the DAQ input subsystem.

        Returns:
            The maximum throughput.

        Raises:
            :class:`ULException`
        """
        max_throughput = c_double()
        err = lib.ulDaqIGetInfoDbl(self.__handle, DaqIInfoItemDbl.MAX_THROUGHPUT, 0, byref(max_throughput))
        if err != 0:
            raise ULException(err)
        return max_throughput.value

    def get_fifo_size(self):
        # type: () -> int
        """
        Gets the size of the FIFO for the DAQ input subsystem.

        Returns:
            The FIFO size.

        Raises:
            :class:`ULException`
        """
        fifo_size = c_longlong()
        err = lib.ulDaqIGetInfo(self.__handle, DaqIInfoItem.FIFO_SIZE, 0, byref(fifo_size))
        if err != 0:
            raise ULException(err)
        return fifo_size.value

    def get_scan_options(self):
        # type: () -> list[ScanOption]
        """
        Gets the scan options for the DAQ input subsystem.

        Returns:
            A list of supported :class:`ScanOption` objects.

        Raises:
            :class:`ULException`
        """
        scan_options_mask = c_longlong()
        err = lib.ulDaqIGetInfo(self.__handle, DaqIInfoItem.SCAN_OPTIONS, 0, byref(scan_options_mask))
        if err != 0:
            raise ULException(err)
        return enum_mask_to_list(ScanOption, scan_options_mask.value)
       
    def get_trigger_types(self):
        # type: () -> list[TriggerType]
        """
        Gets the supported trigger types of the DAQ input subsystem.

        Returns:
            A list of supported :class:`TriggerType` objects.

        Raises:
            :class:`ULException`
        """
        trigger_types_mask = c_longlong()
        err = lib.ulDaqIGetInfo(self.__handle, DaqIInfoItem.TRIG_TYPES, 0, byref(trigger_types_mask))
        if err != 0:
            raise ULException(err)
        return enum_mask_to_list(TriggerType, trigger_types_mask.value)
