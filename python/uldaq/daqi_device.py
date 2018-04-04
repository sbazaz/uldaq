"""
Created on Feb 16 2018

@author: MCC
"""


from ctypes import c_uint, c_double, byref
from .ul_enums import TriggerType, ScanStatus
from .ul_structs import DaqInChanDescriptor, TransferStatus
from .ul_exception import ULException
from .ul_c_interface import lib
from .daqi_info import DaqiInfo


def daqi_chan_descriptor_array(size, descriptor_list):
    chan_descriptor_array = DaqInChanDescriptor * size  # type: type
    return chan_descriptor_array(*descriptor_list)


class DaqiDevice:
    """
    Daq Input subsystem of the UL DAQ Device.

    Args:
        handle: UL DAQ Device handle.
    """

    def __init__(self, handle):
        self.__handle = handle
        self.__daqi_info = DaqiInfo(handle)

    def get_info(self):
        # type: () -> DaqiInfo
        """
        Get daq input information object for the UL DAQ Device.

        Returns:
            A :class:`DaqiInfo` object used for retrieving
            information about the analog input subsystem of the UL DAQ Device.
        """
        return self.__daqi_info
    
    def set_trigger(self, trig_type, trig_chan, level, variance, retrigger_sample_count):
        # type: (TriggerType, int, float, float, int) -> None
        """
        Sets the trigger source and parameters that are used to
        start an daq input scan operation.

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
        err = lib.ulDaqInSetTrigger(self.__handle, trig_type, trig_chan, level, variance, retrigger_sample_count)
        if err != 0:
            raise ULException(err)
    
    def daq_in_scan(self, channel_descriptors, samples_per_channel, rate, options, flags, data):
        # type: (list[DaqInChanDescriptor], int, float, int, int, list[float]) -> float
        """
        Reads a series of values for the channels specified in the DAQ descriptors.

        Args:
            channel_descriptors: A list of :class:`DaqInChanDescriptor` objects.
            samples_per_channel: Number of samples to read.
            rate: Sample input rate in samples per second.
            options: A bit mask specifying scan options.  Possible options
                are enumerated by :class:`ScanOption`.
            flags: A bit mask specifying whether to scale and/or calibrate
                data.  Possible options are enumerated by
                :class:`DaqInScanFlag`.
            data: The data buffer to receive the data being read.

        Returns:
            The actual input scan rate of the scan.

        Raises:
            :class:`ULException`.
        """
        num_channels = len(channel_descriptors)
        rate = c_double(rate)
        chan_descriptor_array = daqi_chan_descriptor_array(num_channels, channel_descriptors)
        err = lib.ulDaqInScan(self.__handle, chan_descriptor_array, num_channels, samples_per_channel, byref(rate),
                              options, flags, data)
        if err != 0:
            raise ULException(err)
        return rate.value
        
    def get_scan_status(self):
        # type: () -> tuple[ScanStatus, TransferStatus]
        """
        Gets the current status of the synchronous Daq Input operation.

        Returns:
            A tuple containing the scan status :class:`ScanStatus`
            and transfer status :class:`TransferStatus` for the
            daq input background operation.

        Raises:
            :class:`ULException`
        """
        status = c_uint()
        transfer_status = TransferStatus()
        err = lib.ulDaqInScanStatus(self.__handle, byref(status), transfer_status)
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
        err = lib.ulDaqInScanStop(self.__handle)
        if err != 0:
            raise ULException(err)
