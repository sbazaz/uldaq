"""
Created on Feb 16 2018

@author: MCC
"""
from .ctr_info import CtrInfo
from .ul_c_interface import lib
from ctypes import byref, c_double, c_uint, c_ulonglong
from .ul_exception import ULException
from .ul_enums import CounterRegisterType, CounterDebounceMode, CounterDebounceTime, CounterEdgeDetection
from .ul_enums import CounterMeasurementMode, CounterMeasurementType, CounterTickSize, CConfigScanFlag, TriggerType
from .ul_enums import ScanStatus
from .ul_structs import TransferStatus


class CtrDevice:
    """
    Counter subsystem of the UL DAQ Device.

    Args:
        handle: UL DAQ Device handle.
    """

    def __init__(self, handle):
        self.__handle = handle
        self.__ctr_info = CtrInfo(handle)

    def get_info(self):
        # type: () -> CtrInfo
        """
        Get counter subsystem information object for the UL DAQ Device.

        Returns:
            :class:`CtrInfo` used for getting the capabilities of the counter subsystem.
        """
        return self.__ctr_info

    def c_in(self, counter_number):
        # type: (int) -> int
        """
        Reads a single value from the specified counter.

        Args:
            counter_number: The number of the counter to be sampled.

        Returns:
            The value read from the counter.

        Raises:
            :class:`ULException`
        """
        data = c_ulonglong()
        err = lib.ulCIn(self.__handle, counter_number, byref(data))
        if err != 0:
            raise ULException(err)
        return data.value

    def c_load(self, counter_number, register_type, load_value):
        # type: (int, CounterRegisterType, int) -> None
        """
        Loads a value into the specified counter register.

        Args:
            counter_number: The number of the counter to be loaded.
            register_type: The :class:`CounterRegisterType` value.
            load_value: The value be loaded into the specified counter.

        Raises:
            :class:`ULException`
        """
        load = c_ulonglong(load_value)
        err = lib.ulCLoad(self.__handle, counter_number, register_type, load)
        if err != 0:
            raise ULException(err)

    def c_clear(self, counter_number):
        # type: (int) -> None
        """
        Clears a specified counter (sets it to 0).

        Args:
            counter_number: The number of the counter to be cleared.

        Raises:
            :class:`ULException`
        """
        err = lib.ulCCLear(self.__handle, counter_number)
        if err != 0:
            raise ULException(err)

    def c_read(self, counter_number, register_type):
        # type: (int, CounterRegisterType) -> int
        """
        Reads the value of the specified counter register.

        Args:
            counter_number: The number of the counter to be read.
            register_type: The :class:`CounterRegisterType` value.

        Returns:
            The value of the counter register.

        Raises:
            :class:`ULException`
        """
        data = c_ulonglong()
        err = lib.ulCRead(self.__handle, counter_number, register_type, byref(data))
        if err != 0:
            raise ULException(err)
        return data.value

    def c_in_scan(self, low_channel, high_channel, samples_per_channel, rate, options, flags, data):
        # type: (int, int, int, float, int, int, list[int]) -> float
        """
        Reads a series of values from a range of counter channels.

        Args:
            low_channel: The first channel in the scan (zero-based).
            high_channel: The last channel in the scan (zero-based).
            samples_per_channel: The number of samples to read.
            rate: The rate at which samples are acquired in samples per second.
            options: A bit mask specifying scan options.
                Possible options are enumerated by :class:`ScanOption`.
            flags: A bit mask specifying whether to scale and/or calibrate data.
                Possible options are enumerated by :class:`CInScanFlag`.
            data: The data buffer to receive the data being read.
                Use :func:`~buffer_manager.BufferManager.create_int_buffer` to create.

        Returns:
            The actual input scan rate.

        Raises:
            :class:`ULException`
        """
        rate = c_double(rate)
        err = lib.ulCInScan(self.__handle, low_channel, high_channel, samples_per_channel, byref(rate),
                            options, flags, data)
        if err != 0:
            raise ULException(err)
        return rate.value

    def c_config_scan(self,
                      counter_number,  # type: int
                      measurement_type,  # type: CounterMeasurementType
                      measurement_mode,  # type: CounterMeasurementMode
                      edge_detection,  # type: CounterEdgeDetection
                      tick_size,  # type: CounterTickSize
                      debounce_mode,  # type: CounterDebounceMode
                      debounce_time,  # type: CounterDebounceTime
                      flags=CConfigScanFlag.DEFAULT  # type: int
                      ):  # type: ()-> None
        """
        Configures a counter channel.

        Args:
            counter_number: The number of the counter to be configured.
            measurement_type: The :class:`CounterMeasurementType` value.
            measurement_mode: A bit mask of :class:`CounterMeasurementMode` values.
            edge_detection: The :class:`CounterEdgeDetection` value.
            tick_size: The :class:`CounterTickSize` value.
            debounce_mode: The :class:`CounterDebounceMode` value.
            debounce_time: The :class:`CounterDebounceTime` value.
            flags (optional): A bit mask specifying the counter scan option.
                Possible options are enumerated by :class:`CConfigScanFlag`.
                Default is CConfigScanFlag.DEFAULT.

        Raises:
            :class:`ULException`
        """
        err = lib.ulCConfigScan(self.__handle, counter_number, measurement_type, measurement_mode, edge_detection,
                                tick_size, debounce_mode, debounce_time, flags)
        if err != 0:
            raise ULException(err)

    def set_trigger(self, trig_type, trig_chan, level, variance, retrigger_count):
        # type: (TriggerType, int, float, float, int) -> None
        """
        Sets the counter trigger source and its parameters.

        Args:
            trig_type: A :class:`TriggerType` value.
            trig_chan: The number of the counter to be set as the trigger source.
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

    def get_scan_status(self):
        # type: () -> tuple[ScanStatus, TransferStatus]
        """
        Gets the current status of the counter input operation.

        Returns:
            A tuple containing the :class:`ScanStatus` and :class:`TransferStatus`
            of the analog output background operation.

        Raises:
            :class:`ULException`
        """
        scan_status = c_uint()
        transfer_status = TransferStatus()

        err = lib.ulCInScanStatus(self.__handle, byref(scan_status), byref(transfer_status))
        if err != 0:
            raise ULException(err)

        return ScanStatus(scan_status.value), transfer_status

    def scan_stop(self):
        # type: () -> None
        """Stops the counter input operation.

        Raises:
            :class:`ULException`
        """
        err = lib.ulCInScanStop(self.__handle)
        if err != 0:
            raise ULException(err)
