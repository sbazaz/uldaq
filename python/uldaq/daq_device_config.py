"""
Created on Feb 17 2018

@author: MCC
"""

from ctypes import create_string_buffer, c_longlong, byref
from .ul_exception import ULException
from .ul_c_interface import lib, UlInfoItem
from .ul_enums import DevVersionType


class DaqDeviceConfig:
    """
    Provides information about the configuration of the DAQ device.

    Args:
        handle: UL DAQ Device handle.
    """

    def __init__(self, handle):
        self.__handle = handle

    def get_version(self, version_type):
        # type: (DevVersionType) -> str
        """
        Gets the version type for the specified firmware type.

        Args:
            version_type: The firmware version type :class:`DevVersionType`
                being determined.

        Returns:
            The firmware type version.

        Raises:
            :class:`ULException`.
        """
        string_len = c_longlong(100)
        info_str = create_string_buffer(string_len.value)
        err = lib.ulDevGetConfigStr(self.__handle, UlInfoItem.VER_STR, version_type, info_str, byref(string_len))
        if err != 0:
            raise ULException(err)
        return info_str.value.decode('utf-8')
