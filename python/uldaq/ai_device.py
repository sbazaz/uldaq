"""
Created on Feb 16 2018

@author: MCC
"""
from ctypes import c_uint, c_double, byref
from .ul_enums import AiInputMode, AInFlag, AInScanFlag, Range, ScanOption, ScanStatus, TriggerType, WaitType
from .ul_structs import AiQueueElement, TransferStatus
from .ul_exception import ULException
from .ul_c_interface import lib
from .ai_info import AiInfo
from .ai_config import AiConfig


class AiDevice:
    """
    Analog input subsystem of the UL DAQ Device.

    Args:
        handle: UL DAQ Device handle.
    """

    def __init__(self, handle):
        self.__handle = handle
        self.__ai_info = AiInfo(handle)
        self.__ai_config = AiConfig(handle)

    def get_info(self):
        # type: () -> AiInfo
        """
        Get analog input information object for the UL DAQ Device.

        Returns:
            :class:`AiInfo` object used for retrieving configuration
            information about the analog input subsystem of the UL DAQ Device.
        """
        return self.__ai_info
    
    def get_config(self):
        # type: () -> AiConfig
        """
        Get analog input configuration object for the UL DAQ Device.

        Returns:
            :class:`AiConfig` object used for retrieving configuration
            information about the analog input subsystem of the UL DAQ Device.
        """
        return self.__ai_config
    
    def a_in(self, channel, input_mode, voltage_range, flags):
        # type: (int, AiInputMode, Range, AInFlag) -> float
        """
        Reads the value of the A/D channel.

        Args:
            channel: Analog input channel number.
            input_mode: The input mode :class:`AiInputMode` for the A/D
                channel specifying that the channel is SingleEnded or Differential
            voltage_range: The voltage range :class:`Range` for the A/D channel
            flags: A bit mask specifying whether to scale and/or calibrate
                data.  Possible options are enumerated by :class:`AInFlag`.


        Returns:
            The value of the A/D channel.

        Raises:
            :class:`ULException`.
        """
        data = c_double()
        err = lib.ulAIn(self.__handle, channel, input_mode, voltage_range, flags, byref(data))
        if err != 0:
            raise ULException(err)
        return data.value
    
    def a_in_scan(self, low_channel, high_channel, input_mode, voltage_range, samples_per_channel, rate, options, flags,
                  data):
        # type: (int, int, AiInputMode, Range, int, float, ScanOption, AInScanFlag, list[float]) -> float
        """
        Reads values from a range of A/D channels.

        Args:
            low_channel: First channel in the scan.
            high_channel: Last channel in the scan.
            input_mode: The :class:`AiInputMode` object for the A/D channels
                specifying that the channels are SingleEnded or Differential
            voltage_range: A/D range :class:`Range`.
            samples_per_channel: Number of samples to read.
            rate: Sample input rate in samples per second.
            options: A bit mask specifying scan options.  Possible options
                are enumerated by :class:`ScanOption`.
            flags: A bit mask specifying whether to scale and/or calibrate
                data.  Possible options are enumerated by
                :class:`AInScanFlag`.
            data: The data buffer to receive the data being read.

        Returns:
            The actual input scan rate of the scan.

        Raises:
            :class:`ULException`.
        """
        rate = c_double(rate)
        err = lib.ulAInScan(self.__handle, low_channel, high_channel, input_mode, voltage_range,
                            samples_per_channel, byref(rate), options, flags, data)
        if err != 0:
            raise ULException(err)
        return rate.value
    
    def a_in_scan_wait(self, wait_type, timeout):
        # type: (WaitType, int) -> None
        """
        Stops a background input operation when the specified wait type has occurred.

        Args:
            wait_type: A mask of :class:`WaitType` values specifying the event types
                to wait for.
            timeout: The timeout value in milliseconds (ms).

        Raises:
            :class:`ULException`.
        """
        err = lib.ulAInScanWait(self.__handle, wait_type, 0, timeout)
        if err != 0:
            raise ULException(err)
 
    def a_in_load_queue(self, queue):
        # type: (AiQueueElement) -> None
        """
        Loads the A/D queue of a specified device..

        Args:
            queue: An array of :class:`AiQueueElement` objects specifying
                the input mode :class:`AiInputMode` and range
                :class:`Range` for each channel.

        Raises:
            :class:`ULException`.
        """
        num_elements = len(queue)
        err = lib.ulAInLoadQueue(self.__handle, queue, num_elements)
        if err != 0:
            raise ULException(err)
   
    def set_trigger(self, trig_type, trig_chan, level, variance, retrigger_sample_count):
        # type: (TriggerType, int, float, float, int) -> None
        """
        Sets the trigger source and parameters that are used to
        start an analog input scan operation.

        Args:
            trig_type: The type of triggering :class:`TriggerType`
                based on the external trigger source.
            trig_chan: The channel to be used as the trigger.
            level: The voltage level at which the trigger event should be
                detected.
            variance: The amount that the trigger event can vary from the
                level parameter.
            retrigger_sample_count: The number of samples to acquire with
                each trigger.

        Raises:
            :class:`ULException`.
        """
        err = lib.ulAInSetTrigger(self.__handle, trig_type, trig_chan, level, variance,
                                  retrigger_sample_count)
        if err != 0:
            raise ULException(err)
    
    def get_scan_status(self):
        # type: () -> tuple[ScanStatus, TransferStatus]
        """
        Gets the current status of the A/D operation.

        Returns:
            A tuple containing the scan status :class:`ScanStatus`
            and transfer status :class:`TransferStatus` for the
            analog input background operation.

        Raises:
            :class:`ULException`
        """
        status = c_uint()
        transfer_status = TransferStatus()
        err = lib.ulAInScanStatus(self.__handle, byref(status), transfer_status)
        if err != 0:
            raise ULException(err)
        return ScanStatus(status.value), transfer_status
    
    def scan_stop(self):
        # type: () -> None
        """
        Stops the A/D scan operation.

        Raises:
            :class:`ULException`
        """
        err = lib.ulAInScanStop(self.__handle)
        if err != 0:
            raise ULException(err)
