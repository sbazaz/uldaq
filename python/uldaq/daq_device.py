"""
Created on Feb 14 2018

@author: MCC
"""
from ctypes import c_bool, c_byte, c_longlong, c_ulonglong, py_object, byref
from .ul_enums import DaqEventType, MemRegion, ULError
from .ul_structs import DaqDeviceDescriptor
from .ul_exception import ULException
from .ul_c_interface import lib, EventParams, CallbackProcType
from .ul_c_interface import InterfaceCallbackProcType, interface_event_callback_function
from .daq_device_info import DaqDeviceInfo
from .daq_device_config import DaqDeviceConfig
from .dev_mem_info import DevMemInfo
from .ai_device import AiDevice
from .ao_device import AoDevice
from .dio_device import DioDevice
from .ctr_device import CtrDevice
from .tmr_device import TmrDevice
from .daqi_device import DaqiDevice
from .daqo_device import DaqoDevice
from .utils import enum_mask_to_list


class DaqDevice:
    """
    UL DAQ Device.

    Args:
        daq_device_descriptor: A :class:`DaqDeviceDescriptor` object.

    Raises:
        :class:`ULException`
    """
    def __init__(self, daq_device_descriptor):
        self._handle = lib.ulCreateDaqDevice(daq_device_descriptor)
        if self._handle == 0:
            raise ULException(ULError.BAD_DESCRIPTOR)

        self.__dev_info = DaqDeviceInfo(self._handle)
        self.__dev_config = DaqDeviceConfig(self._handle)

        self.__ai_device = None
        if self.__dev_info.has_ai_device():
            self.__ai_device = AiDevice(self._handle)

        self.__ao_device = None
        if self.__dev_info.has_ao_device():
            self.__ao_device = AoDevice(self._handle)

        self.__dio_device = None
        if self.__dev_info.has_dio_device():
            self.__dio_device = DioDevice(self._handle)

        self.__ctr_device = None
        if self.__dev_info.has_ctr_device():
            self.__ctr_device = CtrDevice(self._handle)

        self.__tmr_device = None
        if self.__dev_info.has_tmr_device():
            self.__tmr_device = TmrDevice(self._handle)

        self.__daqi_device = None
        if self.__dev_info.has_daqi_device():
            self.__daqi_device = DaqiDevice(self._handle)

        self.__daqo_device = None
        if self.__dev_info.has_daqo_device():
            self.__daqo_device = DaqoDevice(self._handle)

        self.__dev_mem_info = DevMemInfo(self._handle)

        self.__event_params = EventParams()

        # create a dictionary to match event types with callback functions
        self.__event_dictionary = {}

    def __del__(self):
        if self._handle is not None:
            try:
                if self.is_connected():
                    self.disconnect()
            finally:
                self.release()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exe_type, exe_value, exe_traceback):
            self.disconnect()
            self.release()

    def get_descriptor(self):
        # type: () -> DaqDeviceDescriptor
        """
        Gets the DAQ device descriptor.

        Returns:
            :class:`DaqDeviceDescriptor`

        Raises:
            :class:`ULException`
        """
        descriptor = DaqDeviceDescriptor()
        err = lib.ulGetDaqDeviceDescriptor(self._handle, byref(descriptor))
        if err != 0:
            raise ULException(err)
        return descriptor
   
    def connect(self):
        # type: () -> None
        """
        Connects to the DAQ device.

        Raises:
            :class:`ULException`
        """
        err = lib.ulConnectDaqDevice(self._handle)
        if err != 0:
            raise ULException(err)

    def is_connected(self):
        # type: () -> bool
        """
        Gets the DAQ device connection status.

        Returns:
            True if the DAQ device is connected, otherwise False.

        Raises:
            :class:`ULException`
        """
        connected = c_bool()
        err = lib.ulIsDaqDeviceConnected(self._handle, byref(connected))
        if err != 0:
            raise ULException(err)
        return connected
      
    def disconnect(self):
        # type: () -> None
        """
        Disconnects from the DAQ device.

        Raises:
            :class:`ULException`
        """
        err = lib.ulDisconnectDaqDevice(self._handle)
        if err != 0:
            raise ULException(err)

    def flash_led(self, number_of_flashes):
        # type: (int) -> None
        """
        Flashes the LED on the DAQ device.

        Args:
            number_of_flashes: Number of times to flash the LED.

        Raises:
            :class:`ULException`
        """
        err = lib.ulFlashLed(self._handle, number_of_flashes)
        if err != 0:
            raise ULException(err)

    def get_info(self):
        # type: () -> DaqDeviceInfo
        """
        Gets the DAQ device information object.

        Returns: :class:`DaqDeviceInfo` used for getting the capabilities of the DAQ device.
        """
        return self.__dev_info

    def get_config(self):
        # type: () -> DaqDeviceConfig
        """
        Gets the DAQ device configuration object.

        Returns:
            :class:`DaqDeviceConfig` used for getting the configuration of the DAQ device.
        """
        return self.__dev_config

    def get_ai_device(self):
        # type: () -> AiDevice
        """
        Gets the analog input subsystem object.

        Returns:
            :class:`AiDevice`
        """
        return self.__ai_device

    def get_ao_device(self):
        # type: () -> AoDevice
        """
        Gets the analog output subsystem object.

        Returns:
            :class:`AoDevice`
        """
        return self.__ao_device

    def get_dio_device(self):
        # type: () -> DioDevice
        """
        Gets the digital input/output subsystem object.

        Returns:
            :class:`DioDevice`
        """
        return self.__dio_device

    def get_ctr_device(self):
        # type: () -> CtrDevice
        """Gets the counter subsystem object.

        Returns:
            :class:`CtrDevice`
        """
        return self.__ctr_device

    def get_tmr_device(self):
        # type: () -> TmrDevice
        """
        Gets the timer subsystem object.

        Returns:
            :class:`TmrDevice`
        """
        return self.__tmr_device

    def get_daqi_device(self):
        # type: () -> DaqiDevice
        """
        Gets the DAQ input subsystem object.

        Returns:
            :class:`DaqiDevice`
        """
        return self.__daqi_device

    def get_daqo_device(self):
        # type: () -> DaqoDevice
        """Gets the DAQ output subsystem object.

        Returns:
            :class:`DaqoDevice`
        """
        return self.__daqo_device

    def get_mem_info(self):
        # type: () -> DevMemInfo
        """
        Gets the DAQ device memory information object.

        Returns:
            :class:`DevMemInfo`
        """
        return self.__dev_mem_info

    def get_event_dictionary(self):
        # type: () -> {}
        """
        Gets the event dictionary.

        Returns:
            A dictionary of events.
        """
        return self.__event_dictionary

    def enable_event(self, event_types, event_parameter, event_callback_function, user_data):
        # type: (DaqEventType, int, CallbackProcType, py_object) -> None
        """Binds one or more event conditions to a callback function.

        Args:
            event_types: A bit mask containing the event types to which the callback function will be bound.
                Possible options are enumerated by :class:`DaqEventType`.
            event_parameter: Additional data that specifies an event condition
            event_callback_function: The callback function to be executed on the event condition.
            user_data: Data to be passed to the callback function.

        Raises:
            :class:`ULException`
        """
        event_parameter = c_ulonglong(event_parameter)

        event_list = enum_mask_to_list(DaqEventType, event_types)

        for e in event_list:
            self.__event_dictionary[e] = CallbackProcType(event_callback_function)

        event_params = EventParams()
        event_params.device = py_object(self)
        event_params.user_data = py_object(user_data)

        self.__event_params.device = py_object(self)
        self.__event_params.user_data = py_object(user_data)

        err = lib.ulEnableEvent(c_longlong(self._handle),
                                event_types,
                                event_parameter,
                                InterfaceCallbackProcType(interface_event_callback_function),
                                self.__event_params)

        if err != 0:
            raise ULException(err)

    def disable_event(self, event_types):
        # type: (DaqEventType) -> None
        """
        Disables one or more event conditions and unbinds the associated callback function.

        Args:
            event_types: A bit mask containing the event types to disable.
                Possible options are enumerated by :class:`DaqEventType`.

        Raises:
            :class:`ULException`
        """
        err = lib.ulDisableEvent(self._handle, event_types)
        if err != 0:
            raise ULException(err)

    def mem_read(self, mem_region_type, address, count):
        # type: (MemRegion, int, int) -> bytearray
        """
        Reads a block of data from the specified address in the reserved memory area.

        Args:
            mem_region_type: A :class:`MemRegion` to read.
            address: The memory address to read.
            count: The number of bytes to read.

        Raises:
            :class:`ULException`
        """
        mem_buffer = c_byte(count)
        err = lib.ulMemRead(self._handle, mem_region_type, address, mem_buffer, count)
        if err != 0:
            raise ULException(err)
        return mem_buffer

    def mem_write(self, mem_region_type, address, mem_buffer):
        # type: (MemRegion, int, bytearray) -> None
        """
        Writes a block of data to the specified address in the reserve memory area.

        Args:
            mem_region_type: A :class:`MemRegion` to write.
            address: The memory address to write.
            mem_buffer: The data to write.

        Raises:
            :class:`ULException`
        """
        count = len(mem_buffer)
        err = lib.ulMemWrite(self._handle, mem_region_type, address, mem_buffer, count)
        if err != 0:
            raise ULException(err)

    def release(self):
        """
        Releases the DAQ device object.

        Raises:
            :class:`ULException`
        """
        err = lib.ulReleaseDaqDevice(self._handle)
        if err != 0:
            raise ULException(err)
        self._handle = None
