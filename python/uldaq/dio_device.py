"""
Created on Feb 16 2018

@author: MCC
"""
from ctypes import c_double, byref, c_bool, c_uint, c_ulonglong
from .ul_exception import ULException
from .ul_c_interface import lib
from .ul_enums import DigitalPortType, DigitalDirection, DInScanFlag, DOutScanFlag, ScanOption, ScanStatus, TriggerType
from .ul_structs import TransferStatus

from .dio_info import DioInfo
from .dio_config import DioConfig


class DioDevice:
    """
    Digital I/O subsystem of the UL DAQ Device.

    Args:
        handle: UL DAQ Device handle.
    """

    def __init__(self, handle):
        self.__handle = handle
        self.__dio_info = DioInfo(handle)
        self.__dio_config = DioConfig(handle)

    def get_info(self):
        # type: () -> DioInfo
        """
        Get Digital I/O Information object for the UL DAQ Device.

        Returns:
            A :class:`DioInfo` object used for retrieving information about the
            digital I/O subsystem of the UL DAQ Device.
        """
        return self.__dio_info

    def get_config(self):
        # type: () -> DioConfig
        """
        Get Digital I/O Configuration object for the UL DAQ Device.

        Returns:
            A :class:`DioConfig` object used for retrieving configuration
            information about the digital I/O subsystem of the UL DAQ Device.
        """
        return self.__dio_config

    def d_config_port(self, port_type, direction):
        # type: (DigitalPortType, DigitalDirection) -> None
        """
        Configure the digital port type for input or output.

        Args:
            port_type: The port type :class:`DigitalPortType` to
                configure.
            direction: The direction :class:`DigitalDirection` to
                configure the port.

        Raises:
            :class:`ULException`.
        """

        err = lib.ulDConfigPort(self.__handle, port_type, direction)
        if err != 0:
            raise ULException(err)

    def d_config_bit(self, port_type, bit_number, direction):
        # type: (DigitalPortType, int, DigitalDirection) -> None
        """
        Configure a bit within the digital port type for for input
        or output.

        Args:
            port_type: The port type :class:`DigitalPortType`
                containing the bit to configure.
            bit_number: The bit position within the port to configure.
            direction: The direction :class:`DigitalDirection` to
                configure the bit.

        Raises:
            :class:`ULException`.
        """
        err = lib.ulDConfigBit(self.__handle, port_type, bit_number, direction)
        if err != 0:
            raise ULException(err)

    def d_in(self, port_type):
        # type: (DigitalPortType) -> int
        """
        Reads the value of the digital port type.

        Args:
            port_type: Digital port type :class:`DigitalPortType` to
                read.

        Returns:
            The value of the digital port type.

        Raises:
            :class:`ULException`.
        """
        data = c_ulonglong()

        err = lib.ulDIn(self.__handle, port_type, byref(data))
        if err != 0:
            raise ULException(err)
        return data.value

    def d_out(self, port_type, data):
        # type: (DigitalPortType, int) -> None
        """
        Writes the value to the digital port type.

        Args:
            port_type: Digital port type :class:`DigitalPortType` to
                write.
            data: The value to be written.

        Raises:
            :class:`ULException`.
        """
        err = lib.ulDOut(self.__handle, port_type, data)
        if err != 0:
            raise ULException(err)

    def d_bit_in(self, port_type, bit_number):
        # type: (DigitalPortType, int) -> int
        """
        Reads the value of the bit within the digital port type.

        Args:
            port_type: Digital port type :class:`DigitalPortType`
                containing the bit to be read.
            bit_number: The bit position within the port to read.

        Returns:
            The value of the digital bit.

        Raises:
            :class:`ULException`.
        """
        data = c_ulonglong()

        err = lib.ulDBitIn(self.__handle, port_type, bit_number, byref(data))
        if err != 0:
            raise ULException(err)
        return c_bool(data).value

    def d_bit_out(self, port_type, bit_number, data):
        # type: (DigitalPortType, int, int) -> None
        """
        Writes the value to the bit within the digital port type.

        Args:
            port_type: Digital port type :class:`DigitalPortType`
                containing the bit to be written.
            bit_number: The bit position within the port to write.
            data: The value to be written.

        Raises:
            :class:`ULException`.
        """
        err = lib.ulDBitOut(self.__handle, port_type, bit_number, data)
        if err != 0:
            raise ULException(err)

    def d_in_scan(self, low_port_type, high_port_type, samples_per_port, rate, options, flags, data):
        # type: (DigitalPortType, DigitalPortType, int, float, ScanOption, DInScanFlag, list[int]) -> float
        """
        Reads values from a range of digital port types.

        Args:
            low_port_type: First port :class:`DigitalPortType` in the
                scan.
            high_port_type: Last port :class:`DigitalPortType` in the
                scan.
            samples_per_port: The number of samples to read for each port type.
            rate: Sample input rate in samples per second.
            options: A bit mask specifying scan options. Possible options are
                enumerated by :class:`ScanOption`.
            flags: A bit mask specifying data options for the scan.  Possible
                options are enumerated by :class:`DInScanFlag`.
            data: The buffer to receive the digital data.

        Returns:
            The actual sample input rate of the scan.

        Raises:
            :class:`ULException`.
        """
        rate = c_double(rate)
        err = lib.ulDInScan(self.__handle, low_port_type, high_port_type,  samples_per_port, byref(rate),
                            options, flags, data)
        if err != 0:
            raise ULException(err)
        return rate.value

    def d_out_scan(self, low_port_type, high_port_type, samples_per_port, rate, options, flags, data):
        # type: (DigitalPortType, DigitalPortType, int, float, ScanOption, DOutScanFlag, list[int]) -> float
        """
        Writes values to a range of digital port types.

        Args:
            low_port_type: First port :class:`DigitalPortType` in the
                scan.
            high_port_type: Last port :class:`DigitalPortType` in the
                scan.
            samples_per_port: The number of samples to write for each port type.
            rate: Sample output rate in samples per second.
            options: A bit mask specifying scan options.  Possible options are
                enumerated by :class:`ScanOption`.
            flags: A bit mask specifying data options for the scan.  Possible
                options are enumerated by :class:`DInScanFlag`.
            data: The data buffer to be written.

        Returns:
            The actual sample output rate of the scan.

        Raises:
            :class:`ULException`.
        """
        rate = c_double(rate)
        err = lib.ulDOutScan(self.__handle, low_port_type, high_port_type, samples_per_port, byref(rate),
                             options, flags, data)
        if err != 0:
            raise ULException(err)
        return rate.value

    def d_in_set_trigger(self, trig_type, trig_chan, level, variance, retrigger_sample_count):
        # type: (TriggerType, int, float, float, int) -> None
        """
        Sets the trigger source and parameters that are used to
        start a digital input scan operation.

        Args:
            trig_type: The type :class:`TriggerType` of triggering
                based on the external trigger source.
            trig_chan: The channel to be used as the trigger.
            level: The voltage level at which the trigger event should be
                detected.
            variance: The amount that the trigger event can vary from the
                level parameter.
            retrigger_sample_count: The number of samples to acquire with each
                trigger.

        Raises:
            :class:`ULException`.
        """
        err = lib.ulDInSetTrigger(self.__handle, trig_type, trig_chan, level, variance, retrigger_sample_count)
        if err != 0:
            raise ULException(err)

    def d_out_set_trigger(self, trig_type, trig_chan, level, variance, retrigger_sample_count):
        # type: (TriggerType, int, float, float, int) -> None
        """
        Sets the trigger source and parameters that are used to
        start a digital output scan operation.

        Args:
            trig_type: The type :class:`TriggerType` of triggering
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
        err = lib.ulDOutSetTrigger(self.__handle, trig_type, trig_chan, level, variance, retrigger_sample_count)
        if err != 0:
            raise ULException(err)

    def d_in_get_scan_status(self):
        # type: () -> tuple[ScanStatus, TransferStatus]
        """
        Gets the current status of the digital input operation.

        Returns:
            A tuple containing the scan status :class:`ScanStatus`
            and transfer status :class:`TransferStatus` of the
            digital input background operation.

        Raises:
            :class:`ULException`.
        """
        status = c_uint()
        transfer_status = TransferStatus()

        err = lib.ulDInScanStatus(self.__handle, byref(status), transfer_status)
        if err != 0:
            raise ULException(err)
        return ScanStatus(status.value), transfer_status

    def d_out_get_scan_status(self):
        # type: () -> tuple[ScanStatus, TransferStatus]
        """
        Gets the current status of the digital output operation.

        Returns:
            A tuple containing the scan status :class:`ScanStatus`
            and transfer status :class:`TransferStatus` of the
            digital output background operation.

        Raises:
            :class:`ULException`.
        """
        status = c_uint()
        transfer_status = TransferStatus()

        err = lib.ulDOutScanStatus(self.__handle, byref(status), transfer_status)
        if err != 0:
            raise ULException(err)
        return ScanStatus(status.value), transfer_status

    def d_in_scan_stop(self):
        # type: () -> None
        """
        Stops the digital input operation.

        Raises:
            :class:`ULException`.
        """
        err = lib.ulDInScanStop(self.__handle)
        if err != 0:
            raise ULException(err)

    def d_out_scan_stop(self):
        # type: () -> None
        """
        Stops the digital output operation.

        Raises:
            :class:`ULException`.
        """
        err = lib.ulDOutScanStop(self.__handle)
        if err != 0:
            raise ULException(err)
