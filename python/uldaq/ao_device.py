"""
Created on Feb 16 2018

@author: MCC
"""
from ctypes import c_uint, byref, c_double
from .ao_info import AoInfo
from .ul_exception import ULException
from .ul_c_interface import lib
from .ul_enums import AOutFlag, Range, ScanStatus, WaitType, TriggerType
from .ul_structs import TransferStatus


class AoDevice:
    """
    Analog output subsystem of the UL DAQ Device.
    
    Args:
        handle: UL DAQ Device handle.
    """

    def __init__(self, handle):
        self.__handle = handle
        self.__ao_info = AoInfo(handle)

    def get_info(self):
        # type: () -> AoInfo
        """
        Get Analog Output Information object for the UL DAQ Device.
        
        Returns:
            :class:`AoInfo` used for getting the capabilities of the analog output subsystem.
        """
        return self.__ao_info
    
    def a_out(self, channel, voltage_range, flags, data):
        # type: (int, Range, AOutFlag, float) -> None
        """Writes the value of a D/A output.
        
        Args:
            channel: Analog output channel number.
            voltage_range: D/A :class:`Range`.
            flags: A bit mask specifying whether to scale and/or calibrate data.
                Possible options are enumerated by :class:`AOutFlag`.
            data: The value to be written.
            
        Raises:
            :class:`ULException`
        """
        err = lib.ulAOut(self.__handle, channel, voltage_range,
                         flags, data)
        if err != 0:
            raise ULException(err)
    
    def a_out_scan(self, low_chan, high_chan, voltage_range, samples_per_channel, rate, options, flags, data):
        # type: (int, int, Range, int, float, int, int, list[float]) -> float
        """
        Writes values to a range of D/A channels.
        
        Args:
            low_chan: First channel in the scan.
            high_chan: Last channel in the scan.
            voltage_range: D/A :class:`Range`.
            samples_per_channel: Number of samples to output.
            rate: Sample output rate in samples per second.
            options: A bit mask specifying scan options.
                Possible options are enumerated by :class:`ScanOption`.
            flags: A bit mask specifying whether to scale and/or calibrate data.
                Possible options are enumerated by :class:`AOutScanFlag`.
            data: The data buffer to be written.

        Returns:
            The actual output scan rate.

        Raises:
            :class:`ULException`
        """
        sample_rate = c_double(rate)
        err = lib.ulAOutScan(self.__handle, low_chan, high_chan, voltage_range, samples_per_channel,
                             byref(sample_rate), options, flags, data)
        if err != 0:
            raise ULException(err)

        return sample_rate.value
    
    def get_scan_status(self):
        # type: () -> tuple[ScanStatus, TransferStatus]
        """
        Gets the current status of the D/A operation.
        
        Returns:
            A tuple containing the :class:`ScanStatus` and :class:`TransferStatus`
            of the analog output background operation.

        Raises:
            :class:`ULException`
        """
        scan_status = c_uint()
        transfer_status = TransferStatus()
        err = lib.ulAOutScanStatus(self.__handle, byref(scan_status), byref(transfer_status))
        if err != 0:
            raise ULException(err)
       
        return ScanStatus(scan_status.value), transfer_status
    
    def scan_stop(self):
        # type: () -> None
        """
        Stops the D/A scan operation.

        Raises:
            :class:`ULException`
        """
        err = lib.ulAOutScanStop(self.__handle)
        if err != 0:
            raise ULException(err)

    def scan_wait(self, wait_type, timeout):
        # type: (WaitType, float) -> None
        """
        Stops a background output operation for a specified time.

        Args:
            wait_type: The :class:`WaitType`.
            timeout: The timeout value in milliseconds (ms).

        Raises:
            :class:`ULException`
        """
        err = lib.ulAOutScanWait(self.__handle, wait_type, None, timeout)
        if err != 0:
            raise ULException(err)

    def set_trigger(self, trigger_type, channel, level, variance, retrigger_count):
        # type: (TriggerType, int, float, float, int) -> None
        """
        Sets the analog output trigger source and parameters.

        Args:
            trigger_type: :class:`TriggerType`
            channel: Analog output channel number.
            level: The level at or around which the trigger event should be detected.
            variance: The degree to which the input signal can vary relative to the level parameter.
            retrigger_count: The number of samples to acquire with each trigger event.

        Raises:
            :class:`ULException`
        """
        trig_level = c_double(level)
        trig_variance = c_double(variance)

        err = lib.ulAOutSetTrigger(self.__handle, trigger_type, channel, trig_level, trig_variance, retrigger_count)
        if err != 0:
            raise ULException(err)
