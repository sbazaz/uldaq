"""
Created on Mar 23 2018

@author: MCC
"""
from .ul_c_interface import lib, TmrInfoItem, TmrInfoItemDbl
from ctypes import c_longlong, byref, c_double
from .ul_exception import ULException
from .ul_enums import TimerType


class TmrInfo:
    """
    Provides information about the capabilities of the timer subsystem.

    Args:
        handle: UL DAQ Device handle.
    """

    def __init__(self, handle):
        self.__handle = handle

    def get_num_tmrs(self):
        # type: () -> int
        """
        Gets the maximum number of timer channels.

        Returns:
            The maximum number of timer channels.

        Raises:
            :class:`ULException`
        """
        number_of_tmrs = c_longlong()
        err = lib.ulTmrGetInfo(self.__handle, TmrInfoItem.NUM_TMRS, 0, byref(number_of_tmrs))
        if err != 0:
            raise ULException(err)
        return number_of_tmrs.value

    def get_timer_type(self, timer_number):
        # type: (int) -> TimerType
        """
        Get the timer type for the specified timer.

        Args:
            timer_number: The timer number.

        Returns:
            The :class:`TimerType` for the specified timer.

        Raises:
            :class:`ULException`
        """
        timer_type = c_longlong()
        err = lib.ulTmrGetInfo(self.__handle, TmrInfoItem.TYPE, timer_number, byref(timer_type))
        if err != 0:
            raise ULException(err)
        return timer_type.value

    def get_min_frequency(self):
        # type: () -> float
        """
        Gets the minimum frequency for the timer subsystem.

        Returns:
            The minimum frequency.

        Raises:
            :class:`ULException`
        """
        min_freq = c_double()
        err = lib.ulTmrGetInfoDbl(self.__handle, TmrInfoItemDbl.MIN_FREQ, 0, byref(min_freq))
        if err != 0:
            raise ULException(err)
        return min_freq.value

    def get_max_frequency(self):
        # type: () -> float
        """Gets the maximum frequency for the timer subsystem.

        Returns:
            The maximum frequency.

        Raises:
            :class:`ULException`
        """
        max_freq = c_double()
        err = lib.ulTmrGetInfoDbl(self.__handle, TmrInfoItemDbl.MAX_FREQ, 0, byref(max_freq))
        if err != 0:
            raise ULException(err)
        return max_freq.value
