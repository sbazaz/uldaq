"""
Created on Feb 17 2018

@author: MCC
"""
from ctypes import c_longlong, c_bool, c_double, byref
from .ul_enums import DigitalPortType, DigitalPortIoType, ScanOption, TriggerType, ULError
from .ul_structs import DioPortInfo
from .ul_exception import ULException
from .ul_c_interface import lib, DioInfoItem, DioInfoItemDbl
from .utils import enum_mask_to_list


class DioInfo:
    """
    Provides information about the capabilities of the digital I/O subsystem.

    Args:
        handle: UL DAQ Device handle.
    """

    def __init__(self, handle):
        self.__handle = handle

    def get_num_ports(self):
        # type: () -> int
        """
        Gets the number of digital I/O ports for the digital I/O subsystem.

        Returns:
            The number of digital I/O ports.

        Raises:
            :class:`ULException`.
        """
        number_of_ports = c_longlong()
        err = lib.ulDIOGetInfo(self.__handle, DioInfoItem.NUM_PORTS, 0, byref(number_of_ports))
        if err != 0:
            raise ULException(err)
        return number_of_ports.value

    def get_port_types(self):
        # type: () -> list[DigitalPortType]
        """
        Gets the port types supported by the digital I/O subsystem.

        Returns:
            A list of supported :class:`DigitalPortType` values.

        Raises:
            :class:`ULException`.
        """
        port_type = c_longlong()
        port_types_list = []

        number_of_ports = self.get_num_ports()
        for i in range(number_of_ports):
            err = lib.ulDIOGetInfo(self.__handle, DioInfoItem.PORT_TYPE, i, byref(port_type))
            if err != 0:
                raise ULException(err)

            for d_port_type in DigitalPortType:
                if port_type.value == d_port_type:
                    port_types_list.append(d_port_type)

        return port_types_list

    def get_port_info(self, port_type):
        # type: (DigitalPortType) -> DioPortInfo
        """
        Gets the port I/O type and the number of bits for the digital port
        type.

        Args:
            port_type: The port type :class:`DigitalPortType` whose
                number of bits is being determined.

        Returns:
            A :class:`DioPortInfo` object containing the port I/O type
            and the number of bits in the port.

        Raises:
            :class:`ULException`.
        """
        number_of_bits = c_longlong()
        port_io_type = c_longlong()

        port_types_list = self.get_port_types()
        if port_type in port_types_list:
            port_index = port_types_list.index(port_type)
            err = lib.ulDIOGetInfo(self.__handle, DioInfoItem.NUM_BITS, port_index, byref(number_of_bits))
            if err != 0:
                raise ULException(err)
            err = lib.ulDIOGetInfo(self.__handle, DioInfoItem.PORT_IO_TYPE, port_index, byref(port_io_type))
            if err != 0:
                raise ULException(err)
        else:
            raise ULException(ULError.BAD_PORT_TYPE)

        port_info = DioPortInfo()
        port_info.port_type = port_type
        port_info.number_of_bits = number_of_bits.value
        port_info.port_io_type = port_io_type.value
        return port_info

    def get_num_bits(self, port_type):
        # type: (DigitalPortType) -> int
        """
        Gets the number of bits for the digital port type.

        Args:
            port_type: The port type :class:`DigitalPortType` whose
                number of bits is being determined.

        Returns:
            The number of bits in the port.

        Raises:
            :class:`ULException`.
        """
        number_of_bits = c_longlong()

        port_types_list = self.get_port_types()
        if port_type in port_types_list:
            port_index = port_types_list.index(port_type)
            err = lib.ulDIOGetInfo(self.__handle, DioInfoItem.NUM_BITS, port_index, byref(number_of_bits))
            if err != 0:
                raise ULException(err)
        else:
            raise ULException(ULError.BAD_PORT_TYPE)
        return number_of_bits.value

    def get_port_io_type(self, port_type):
        # type: (DigitalPortType) -> DigitalPortIoType
        """
        Gets the port I/O type for the digital port type.

        Args:
            port_type: The port type :class:`DigitalPortType` whose
                port I/O type is being determined.

        Returns:
            The port I/O type :class:`DigitalPortIoType`.

        Raises:
            :class:`ULException`.
        """
        port_io_type = c_longlong()

        port_types_list = self.get_port_types()
        if port_type in port_types_list:
            port_index = port_types_list.index(port_type)
            err = lib.ulDIOGetInfo(self.__handle, DioInfoItem.PORT_IO_TYPE, port_index, byref(port_io_type))
            if err != 0:
                raise ULException(err)
        else:
            raise ULException(ULError.BAD_PORT_TYPE)
        return port_io_type.value

    def has_pacer(self, direction):
        # type: () -> bool
        """
        Determines whether or not the digital I/O subsystem has a
        hardware pacer.

        Args:
            direction: The direction :class:`DigitalDirection` whose
                pacer support is being determined.

        Returns:
            True if the device has an analog output hardware pacer.
            False if the device does not have an analog output hardware pacer.

        Raises:
            :class:`ULException`.
        """
        has_pacer = c_longlong()
        err = lib.ulDIOGetInfo(self.__handle, DioInfoItem.HAS_PACER, direction, byref(has_pacer))
        if err != 0:
            raise ULException(err)
        return c_bool(has_pacer).value

    def get_min_scan_rate(self, direction):
        # type: () -> float
        """
        Gets the minimum scan rate for the digital I/O subsystem.

        Args:
            direction: The direction :class:`DigitalDirection` whose
                minimum scan rate is being determined.

        Returns:
            The minimum scan rate.

        Raises:
            :class:`ULException`.
        """
        min_scan_rate = c_double()
        err = lib.ulDIOGetInfoDbl(self.__handle, DioInfoItemDbl.MIN_SCAN_RATE, direction,
                                  byref(min_scan_rate))
        if err != 0:
            raise ULException(err)
        return min_scan_rate.value

    def get_max_scan_rate(self, direction):
        # type: () -> float
        """
        Gets the maximum scan rate for the digital I/O subsystem.

        Args:
            direction: The direction :class:`DigitalDirection` whose
                maximum scan rate is being determined.

        Returns:
            The maximum scan rate.

        Raises:
            :class:`ULException`.
        """
        max_scan_rate = c_double()
        err = lib.ulDIOGetInfoDbl(self.__handle, DioInfoItemDbl.MAX_SCAN_RATE, direction,
                                  byref(max_scan_rate))
        if err != 0:
            raise ULException(err)
        return max_scan_rate.value

    def get_max_throughput(self, direction):
        # type: () -> float
        """
        Gets the maximum throughput for the digital I/O subsystem.

        Args:
            direction: The direction :class:`DigitalDirection` whose
                maximum throughput is being determined.

        Returns:
            The maximum throughput.

        Raises:
            :class:`ULException`.
        """
        max_throughput = c_double()
        err = lib.ulDIOGetInfoDbl(self.__handle, DioInfoItemDbl.MAX_THROUGHPUT, direction,
                                  byref(max_throughput))
        if err != 0:
            raise ULException(err)
        return max_throughput.value

    def get_fifo_size(self, direction):
        # type: () -> int
        """
        Gets the size of the FIFO for the digital I/O subsystem.

        Args:
            direction: The direction :class:`DigitalDirection` whose
                fifo size is being determined.

        Returns:
            The FIFO size.

        Raises:
            :class:`ULException`.
        """
        fifo_size = c_longlong()
        err = lib.ulDIOGetInfo(self.__handle, DioInfoItem.FIFO_SIZE, direction, byref(fifo_size))
        if err != 0:
            raise ULException(err)
        return fifo_size.value

    def get_scan_options(self, direction):
        # type: () -> list[ScanOption]
        """
        Gets the scan options for the digital I/O subsystem.

        Args:
            direction: The direction :class:`DigitalDirection` whose
                scan options is being determined.

        Returns:
            A list of supported :class:`ScanOption` values.

        Raises:
            :class:`ULException`.
        """
        scan_options_mask = c_longlong()
        err = lib.ulDIOGetInfo(self.__handle, DioInfoItem.SCAN_OPTIONS, direction, byref(scan_options_mask))
        if err != 0:
            raise ULException(err)
        return enum_mask_to_list(ScanOption, scan_options_mask.value)

    def get_trigger_types(self, direction):
        # type: () -> list[TriggerType]
        """
        Gets the supported trigger types of the digital I/O subsystem.

        Args:
            direction: The direction :class:`DigitalDirection` whose
                trigger types is being determined.

        Returns:
            A list of supported :class:`TriggerType` values.

        Raises:
            :class:`ULException`.
        """
        trigger_types_mask = c_longlong()
        err = lib.ulDIOGetInfo(self.__handle, DioInfoItem.TRIG_TYPES, direction, byref(trigger_types_mask))
        if err != 0:
            raise ULException(err)
        return enum_mask_to_list(TriggerType, trigger_types_mask.value)
