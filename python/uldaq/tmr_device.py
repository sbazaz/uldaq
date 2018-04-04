"""
Created on Feb 16 2018

@author: MCC
"""
from .tmr_info import TmrInfo
from .ul_enums import TmrIdleState, PulseOutOption, TmrStatus, TriggerType
from ctypes import c_double, byref, c_uint
from .ul_c_interface import lib
from .ul_exception import ULException


class TmrDevice:
    """
    Timer subsystem of the UL DAQ Device.

    Args:
        handle: UL DAQ Device handle.
    """

    def __init__(self, handle):
        self.__handle = handle
        self.__tmr_info = TmrInfo(handle)

    def get_info(self):
        # type: () -> TmrInfo
        """Get timer subsystem information object for the UL DAQ Device.

        Returns:
            :class:`TmrInfo` used for getting the capabilities of the timer subsystem.
        """
        return self.__tmr_info

    def pulse_out_start(self, timer_number, frequency, duty_cycle, pulse_count, initial_delay, idle_state, options):
        # type: (int, float, float, int, float, TmrIdleState, PulseOutOption) -> tuple[float, float, float]
        """
        Starts a timer to generate digital pulses at a specified frequency and duty cycle.

        Args:
            timer_number: The timer number.
            frequency: The frequency of the digital pulses.
            duty_cycle: The duty cycle of the digital pulses.
            pulse_count: The number of pulses to generate.
            initial_delay: The amount of time in seconds to wait before the timer output.
            idle_state: The :class:`TmrIdleState` value when idle.
            options: A bit mask of :class:`PulseOutOption` values.

        Returns:
            A tuple containing the actual frequency, duty cycle, and initial delay values.

        Raises:
            :class:`ULException`
        """
        pulse_frequency = c_double(frequency)
        pulse_duty_cycle = c_double(duty_cycle)
        pulse_initial_delay = c_double(initial_delay)

        err = lib.ulTmrPulseOutStart(self.__handle, timer_number, byref(pulse_frequency), byref(pulse_duty_cycle),
                                     pulse_count, byref(pulse_initial_delay), idle_state, options)
        if err != 0:
            raise ULException(err)

        return pulse_frequency.value, pulse_duty_cycle.value, pulse_initial_delay.value

    def pulse_out_stop(self, timer_number):
        """
        Stops the timer output.

        Args:
            timer_number: The timer number.

        Raises:
            :class:`ULException`
        """
        err = lib.ulTmrPulseOutStop(self.__handle, timer_number)
        if err != 0:
            raise ULException(err)

    def get_pulse_out_status(self, timer_number):
        # type: (int) -> TmrStatus
        """
        Gets the status of the timer output operation.

        Args:
            timer_number: The timer number.

        Returns:
            A :class:`TmrStatus` value.

        Raises:
            :class:`ULException`
        """
        tmr_status = c_uint()
        err = lib.ulTmrPulseOutStatus(self.__handle, timer_number, byref(tmr_status))
        if err != 0:
            raise ULException(err)
        return TmrStatus(tmr_status.value)

    def set_trigger(self, trig_type, trig_chan, level, variance, retrigger_count):
        # type: (TriggerType, int, float, float, int) -> None
        """
        Sets the timer trigger source and its parameters.

        Args:
            trig_type: A :class:`TriggerType` value.
            trig_chan: The timer number to be set as the trigger source.
            level: The level at or around which the trigger event should be detected.
            variance: The degree to which the input signal can vary relative to the level parameter.
            retrigger_count: The number of samples to acquire with each trigger event.

        Raises:
            :class:`ULException`
        """
        trig_level = c_double(level)
        trig_variance = c_double(variance)

        err = lib.ulCInSetTrigger(self.__handle, trig_type, trig_chan, trig_level, trig_variance, retrigger_count)
        if err != 0:
            raise ULException(err)
