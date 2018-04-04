"""
Created on Feb 17 2018

@author: MCC
"""

from ctypes import c_longlong, byref
from .ul_exception import ULException
from .ul_c_interface import lib, DioInfoItem, DioConfigItem
from .ul_enums import DigitalDirection, ULError


class DioConfig:
    """Provides information about the configuration of the digital I/O subsystem.

    Args:
        handle: UL DAQ Device handle.
    """

    def __init__(self, handle):
        self.__handle = handle

    def get_port_direction(self, port_type):
        # type: (int) -> DigitalDirection
        """
        Gets the current direction the port type is configured for.

        Args:
            port_type: The port type :class:`DigitalPortType` whose
                direction is being determined.

        Returns:
            The direction :class:`DigitalDirection` of the port.

        Raises:
            :class:`ULException`.
        """
        port_direction = c_longlong()
        port_types_list = []
        number_of_ports = c_longlong()

        err = lib.ulDIOGetInfo(self.__handle, DioInfoItem.NUM_PORTS, 0, byref(number_of_ports))
        if err != 0:
            raise ULException(err)

        # get the supported port types
        type_of_port = c_longlong()
        for i in range(number_of_ports.value):
            err = lib.ulDIOGetInfo(self.__handle, DioInfoItem.PORT_TYPE, i, byref(type_of_port))
            if err != 0:
                raise ULException(err)
            port_types_list.append(type_of_port.value)

        # get the index for the port type
        if port_type in port_types_list:
            port_index = port_types_list.index(port_type)

            err = lib.ulDIOGetInfo(self.__handle, DioConfigItem.DIO_CFG_PORT_DIRECTION_MASK, port_index,
                                   byref(port_direction))
            if err != 0:
                raise ULException(err)
        else:
            raise ULException(ULError.BAD_PORT_TYPE)

        return DigitalDirection(port_direction)
