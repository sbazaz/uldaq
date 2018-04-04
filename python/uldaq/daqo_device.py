"""
Created on Feb 16 2018

@author: MCC
"""
from .daqo_info import DaqoInfo
from ctypes import c_double, c_uint, byref
from .ul_c_interface import lib
from .ul_exception import ULException
from .ul_enums import ScanStatus, WaitType, TriggerType
from .ul_structs import DaqOutChanDescriptor, TransferStatus


def daqo_chan_descriptor_array(size, descriptor_list):
    chan_descriptor_array = DaqOutChanDescriptor * size  # type: type
    return chan_descriptor_array(*descriptor_list)


class DaqoDevice:
    """
    DAQ output subsystem of the UL DAQ Device.

    Args:
        handle: UL DAQ Device handle.
    """

    def __init__(self, handle):
        self.__handle = handle
        self.__daqo_info = DaqoInfo(handle)

    def get_info(self):
        # type: () -> DaqoInfo
        """
        Get DAQ Output Information object for the UL DAQ Device.

        Returns:
            :class:`DaqoInfo` used for getting the capabilities of the DAQ output subsystem.
        """
        return self.__daqo_info

    def daq_out_scan(self, channel_descriptors, samples_per_channel, rate, options, flags, data):
        # type: (list[DaqOutChanDescriptor], int, float, int, int, list[float]) -> float
        """
        Outputs values synchronously to analog output channels and digital output ports.
        This function only works with devices that support synchronous output.

        Args:
            channel_descriptors: A list of :class:`DaqOutChanDescriptor` objects.
            samples_per_channel: The number of samples per channel to output.
            rate: The sample rate in samples per second.
            options: A bit mask specifying scan options.
                Possible options are enumerated by :class:`ScanOption`.
            flags: A bit mask specifying whether to scale and/or calibrate data.
                Possible options are enumerated by :class:`DaqOutScanFlag`.
            data: The data buffer to be written.

        Returns:
            The actual output scan rate.

        Raises:
            :class:`ULException`
        """
        sample_rate = c_double(rate)
        number_of_channels = len(channel_descriptors)
        chan_descriptor_array = daqo_chan_descriptor_array(number_of_channels, channel_descriptors)
        err = lib.ulDaqOutScan(self.__handle, chan_descriptor_array, number_of_channels, samples_per_channel,
                               byref(sample_rate), options, flags, data)
        if err != 0:
            raise ULException(err)

        return sample_rate.value

    def get_scan_status(self):
        # type: () -> tuple[ScanStatus, TransferStatus]
        """
        Gets the current status of the synchronous D/A operation.

        Returns:
            A tuple containing the :class:`ScanStatus` and :class:`TransferStatus`
            of the DAQ output background operation.

        Raises:
            :class:`ULException`
        """
        scan_status = c_uint()
        transfer_status = TransferStatus()
        err = lib.ulDaqOutScanStatus(self.__handle, byref(scan_status), byref(transfer_status))
        if err != 0:
            raise ULException(err)

        return ScanStatus(scan_status.value), transfer_status

    def scan_stop(self):
        # type: () -> None
        """
        Stops the synchronous output scan operation.

        Raises:
            :class:`ULException`
        """
        err = lib.ulDaqOutScanStop(self.__handle)
        if err != 0:
            raise ULException(err)

    def scan_wait(self, wait_type, timeout):
        # type: (WaitType, float) -> None
        """
        Stops a background synchronous output operation for a specified time.

        Args:
            wait_type: The :class:`WaitType`.
            timeout: The timeout value in milliseconds (ms).

        Raises:
            :class:`ULException`
        """
        err = lib.ulDaqOutScanWait(self.__handle, wait_type, None, timeout)
        if err != 0:
            raise ULException(err)

    def set_trigger(self, trigger_type, channel, level, variance, retrigger_count):
        # type: (TriggerType, DaqOutChanDescriptor, float, float, int) -> None
        """
        Sets the DAQ output trigger source and parameters.

        Args:
            trigger_type: :class:`TriggerType`
            channel: A :class:`DaqOutChanDescriptor` object.
            level: The level at or around which the trigger event should be detected.
            variance: The degree to which the input signal can vary relative to the level parameter.
            retrigger_count: The number of samples to acquire with each trigger event.

        Raises:
            :class:`ULException`
        """
        trig_level = c_double(level)
        trig_variance = c_double(variance)

        err = lib.ulDaqOutSetTrigger(self.__handle, trigger_type, channel, trig_level, trig_variance, retrigger_count)
        if err != 0:
            raise ULException(err)
