"""
Created on Mar 7 2018

@author: MCC
"""
from ctypes import CDLL, CFUNCTYPE, Structure, c_uint, c_int, c_longlong
from ctypes import POINTER, c_double, c_char, py_object, c_ulonglong, cast
from enum import IntEnum
from .ul_structs import DaqDeviceDescriptor, AiQueueElement, TransferStatus
from .ul_structs import DaqInChanDescriptor, MemDescriptor, DaqOutChanDescriptor
from .ul_enums import DaqEventType

lib = CDLL('libuldaq.so')

#
# Structures
#


class EventParams(Structure):
    _fields_ = [("device", py_object),          # this instance of the DAQ device class
                ("user_data", py_object)]       # the user data


#
# Enums
#


class UlInfoItem (IntEnum):
    """UL version information."""
    VER_STR = 2000,  #: UL version number
    
    
class DevItemInfo (IntEnum):
    """Device information types"""
    HAS_AI_DEV = 1,  #: The DAQ device has an analog input subsystem.
    HAS_AO_DEV = 2,  #: The DAQ device has an analog output subsystem.
    HAS_DIO_DEV = 3,  #: The DAQ device has a Digital I/O subsystem.
    HAS_CTR_DEV = 4,  #: The DAQ device has a counter input subsystem.
    HAS_TMR_DEV = 5,  #: The DAQ device has a timer output subsystem.
    HAS_DAQI_DEV = 6,  #: The DAQ device has a DAQ input subsystem.
    HAS_DAQO_DEV = 7,  #: The DAQ device has an DAQ output subsystem.
    DAQ_EVENT_TYPES = 8,  #: Event types supported by the DAQ device
    MEM_REGIONS = 9,  #: Memory regions supported by the DAQ device
    
    
class AiInfoItem (IntEnum):
    """Use with ulAIGetInfo() to obtain AI subsystem information."""
    RESOLUTION = 1,  #: The A/D resolution in number of bits.
    NUM_CHANS = 2,  #: The number of A/D channels on the specified device.
    NUM_CHANS_BY_MODE = 3,  #: The number of A/D channels for the specified channel mode.
    NUM_CHANS_BY_TYPE = 4,  #: The number of A/D channels for the specified channel type.
    CHAN_TYPES = 5,  #: A bitmask of supported :func:'~ul_daq.AiChanType' values.
    SCAN_OPTIONS = 6,  #: A bitmask of supported :func:'~ul_daq.ScanOption' values.
    HAS_PACER = 7,  #: Paced operations are supported.
    NUM_DIFF_RANGES = 8,  #: A number of supported :func:'~ul_daq.Range' values for differential mode operations.
    NUM_SE_RANGES = 9,  #: A number of supported :func:'~ul_daq.Range' values for single-ended mode operations.
    DIFF_RANGE = 10,  #: The :func:'~ul_daq.Range' for the specified differential range index.
    SE_RANGE = 11,  #: The :func:'~ul_daq.Range' for the specified single-ended range index.
    TRIG_TYPES = 12,  #: A bitmask of supported :func:'~ul_daq.TriggerType' values.
    MAX_QUEUE_LENGTH_BY_MODE = 13,  #: The maximum length of the queue for the specified channel mode.
    QUEUE_TYPES = 14,  #: A bitmask of supported :func:'~ul_daq.AiQueueType' values supported for the specified device.
    QUEUE_LIMITS = 15,  #: A bitmask of supported :func:'~ul_daq.AiChanQueueLimitation' values.
    FIFO_SIZE = 16,  #: FIFO size in bytes.


class AiInfoItemDbl (IntEnum):
    """Use with ulAIGetInfoDbl() to obtain AI subsystem information."""
    MIN_SCAN_RATE = 1000,  #: The minimum scan rate of the specified device.
    MAX_SCAN_RATE = 1001,  #: The maximum scan rate of the specified device.
    MAX_THROUGHPUT = 1002,  #: The maximum throughput in samples per second of the specified device.
    MAX_BURST_RATE = 1003,
    #: The maximum scan rate in samples per second when using :func:'~ul_daq.ScanOption.SO_BURSTIO' mode.
    MAX_BURST_THROUGHPUT = 1004,
    #: The maximum throughput in samples per second when using :func:'~ul_daq.ScanOption.SO_BURSTIO' mode.
    
    
class AiConfigItem (IntEnum):
    """Use with ulSetConfig() and ulGetConfig() to perform configuration operations on the AI subsystem."""
    CHAN_TYPE = 1,  #: The channel type of the specified  channel. Set with :func:'~ul_daq.AiChanType'.
    CHAN_TC_TYPE = 2,  #: he thermocouple type of the specified channel. Set with :func:'~ul_daq.TcType'.
    CHAN_TEMP_UNIT = 3,  #: The temperature unit of the specified channel. Set with :func:'~ul_daq.TempUnit'.
    TEMP_UNIT = 4,  #: The temperature unit for the specified device. Set with :func:'~ul_daq.AiChanType'.
    ADC_TIMING_MODE = 5,  #: The timing mode. Set with :func:'~ul_daq.AdcTimingMode'.
    AUTO_ZERO_MODE = 6,  #: The auto zero mode. Set with :func:'~ul_daq.AutoZeroMode'.
    CAL_DATE = 7,  #: The date when the device was calibrated last.
    CHAN_IEPE_MODE = 8,
    #: The IEPE current excitation mode for the specified channel. Set with :func:'~ul_daq.IepeMode'.
    CHAN_COUPLING_MODE = 9,  #: The coupling mode for the specified device. Set with :func:'~ul_daq.CouplingMode'.


class AiConfigItemDbl  (IntEnum):
    """Use with ulSetConfigDbl() and ulGetConfigDbl() to perform configuration operations on the AI subsystem. """
    CHAN_SLOPE = 1000,  #: The slope of the specified channel.
    CHAN_OFFSET = 1001,  #: The offset of the specified channel.
    CHAN_SENSOR_SENSIVITY = 1002,  #: The sensitivity of the sensor connected to the specified channel.


class DioInfoItem (IntEnum):
    """Use with ulDIOGetInfo() to obtain information about the DIO subsystem."""
    NUM_PORTS = 1,  #: The number of ports on the specified device.
    PORT_TYPE = 2,  #: The port type for the specified port index.
    PORT_IO_TYPE = 3,  #: The #DigitalPortIoType for the specified port index.
    NUM_BITS = 4,  #: The number of bits on the port specified by the port index.
    HAS_PACER = 5,  #: Paced operations are supported for the specified digital direction.
    SCAN_OPTIONS = 6,  #: A bit mask of supported :func:'~ul_daq.ScanOption' values for the specified digital direction.
    TRIG_TYPES = 7,  #: A bitmask of supported :func:'~ul_daq.TriggerType' values for the specified digital direction.
    FIFO_SIZE = 8,  #: FIFO size in bytes for the specified digital direction.


class DioInfoItemDbl (IntEnum):
    """Use with ulDIOGetInfoDbl() to obtain information about the DIO subsystem."""
    MIN_SCAN_RATE = 1000,  #: The minimum scan rate of the specified device.
    MAX_SCAN_RATE = 1001,  #: The maximum scan rate of the specified device.
    MAX_THROUGHPUT = 1002,  #: The maximum scanning throughput of the specified device.


class DioConfigItem  (IntEnum):
    """ Use with ulDIOGetConfig() to obtain information about the DIO subsystem configuration. """
    DIO_CFG_PORT_DIRECTION_MASK = 1,  #: The port direction. Set with :func:'~ul_daq.DigitalDirection'.


class DaqIInfoItem (IntEnum):
    """Use with ulDaqIGetInfo() to obtain DAQ input subsystem information."""
    CHAN_TYPES = 1,  #: A bitmask of supported :func:'~ul_daq.DaqInChanType' values.
    SCAN_OPTIONS = 2,  #: A bit mask of supported :func:'~ul_daq.ScanOption' values.
    TRIG_TYPES = 3,  #: A bitmask of supported :func:'~ul_daq.TriggerType' values.
    FIFO_SIZE = 4,  #: FIFO size in bytes.


class DaqIInfoItemDbl (IntEnum):
    """Use with ulDaqIGetInfoDbl() to obtain information about the counter subsystem."""
    MIN_SCAN_RATE = 1000,  #: The minimum scan rate in samples per second.
    MAX_SCAN_RATE = 1001,  #: The maximum scan rate of the specified device.
    MAX_THROUGHPUT = 1002,  #: The maximum throughput of the specified device.


class AoInfoItem (IntEnum):
    """Use with ulAOGetInfo() to obtain information about the analog output subsystem."""
    RESOLUTION = 1,  #: The D/A resolution.
    NUM_CHANS = 2,  #: The number of D/A channels on the specified device.
    SCAN_OPTIONS = 3,  #: A bit mask of supported :func:'~ul_daq.ScanOption; values.
    HAS_PACER = 4,  #: Paced operations are supported.
    NUM_RANGES = 5,  #: The number of supported :func:'~ul_daq.Range' values for D/A operations.
    RANGE = 6,  #: The :func:'~ul_daq.Range' for the specified range index.
    TRIG_TYPES = 7,  #: A bitmask of supported :func:'~ul_daq.TriggerType' values.
    FIFO_SIZE = 8,  #: FIFO size in bytes.


class AoInfoItemDbl (IntEnum):
    """Use with ulAOGetInfoDbl() to obtain information about the Analog output subsystem."""
    MIN_SCAN_RATE = 1000,  #: The minimum scan rate of the specified device.
    MAX_SCAN_RATE = 1001,  #: The maximum scan rate of the specified device.
    MAX_THROUGHPUT = 1002,  #: The maximum scanning throughput of the specified device.


class DaqoInfoItem (IntEnum):
    """Use with ulDaqOGetInfo() to obtain information about the DAQ output subsystem."""
    CHAN_TYPES = 1,  #: A bit mask of supported :class:`DaqOutChanType` values.
    SCAN_OPTIONS = 2,  #: A bit mask of supported :class:`ScanOption` values.
    TRIG_TYPES = 3,  #: A bit mask of supported :class:`TriggerType` values.
    FIFO_SIZE = 4,  #: FIFO size in bytes.


class DaqoInfoItemDbl (IntEnum):
    """Use with ulDaqOGetInfoDbl() to obtain information about the DAQ output subsystem."""
    MIN_SCAN_RATE = 1000,  #: The minimum scan rate in samples per second.
    MAX_SCAN_RATE = 1001,  #: The maximum scan rate of the specified device.
    MAX_THROUGHPUT = 1002,  #: The maximum throughput of the specified device.


class CtrInfoItem (IntEnum):
    """Use with ulCtrGetInfo() to obtain information about the counter subsystem."""
    NUM_CTRS = 1,  #: The number of counter channels on the specified device.
    MEASUREMENT_TYPES = 2,  #: A bit mask of supported :class:`CounterMeasurementType` values.
    MEASUREMENT_MODES = 3,  #: A bit mask of supported :class:`CounterMeasurementType` values.
    REGISTER_TYPES = 4,  #: A bit mask of supported :class:`CounterRegisterType` values.
    RESOLUTION = 5,  #: The resolution of the specified counter channel.
    HAS_PACER = 6,  #: Paced operations are supported.
    SCAN_OPTIONS = 7,  #: A bit mask of supported :class:`ScanOption` values.
    TRIG_TYPES = 8,  #: A bit mask of supported :class:`TriggerType` values.
    FIFO_SIZE = 9,  #: FIFO size in bytes.


class CtrInfoItemDbl (IntEnum):
    """Use with ulCtrGetInfoDbl() to obtain information about the counter subsystem."""
    MIN_SCAN_RATE = 1000,  #: The minimum scan rate in samples per second.
    MAX_SCAN_RATE = 1001,  #: The maximum scan rate of the specified device.
    MAX_THROUGHPUT = 1002,  #: The maximum throughput of the specified device.


class TmrInfoItem (IntEnum):
    """Use with ulTmrGetInfo() to obtain information about the timer subsystem."""
    NUM_TMRS = 1,  #: The :class:`TimerType` of the specified timer index.
    TYPE = 2,  #: The number of bits on the port specified by the port index.


class TmrInfoItemDbl (IntEnum):
    """Use with ulTmrGetInfoDbl() to obtain information about the timer subsystem."""
    MIN_FREQ = 1000,  #: The minimum frequency of the specified device.
    MAX_FREQ = 1001,  #: The maximum frequency of the specified device.


# Prototypes for callbacks


InterfaceCallbackProcType = CFUNCTYPE(None, c_longlong, c_uint, c_ulonglong, POINTER(EventParams))
CallbackProcType = CFUNCTYPE(None, c_uint, c_ulonglong, py_object)


def interface_event_callback_function(handle, event_type, event_data, event_params):
    # type: (int, DaqEventType, py_object, py_object) -> bool
    """Internal function used for handling event callbacks."""

    event_parameters = cast(event_params, POINTER(EventParams)).contents
    daq_device = event_parameters.device
    user_data = event_parameters.user_data

    event_dictionary = daq_device.get_event_dictionary()
    cb = event_dictionary[event_type]
    cb(event_type, event_data, user_data)
    return True


# Prototypes for DAQ Device
lib.ulDevGetConfigStr.argtypes = (c_longlong, c_uint, c_uint, POINTER(c_char), POINTER(c_longlong))
lib.ulGetDaqDeviceDescriptor.argtypes = (c_longlong, POINTER(DaqDeviceDescriptor))
lib.ulDevGetInfo.argtypes = (c_longlong, c_uint, c_uint, POINTER(c_longlong))
lib.ulGetDaqDeviceInventory.argtypes = (c_uint, POINTER(DaqDeviceDescriptor), POINTER(c_uint))
lib.ulGetDaqDeviceDescriptor.argtypes = (c_longlong, POINTER(DaqDeviceDescriptor))
lib.ulConnectDaqDevice.argtype = c_longlong
lib.ulEnableEvent.argtypes = (c_longlong, c_uint, c_ulonglong, InterfaceCallbackProcType, POINTER(EventParams))
lib.ulDisableEvent.argtypes = (c_longlong, c_uint)
lib.ulMemRead.argtypes = (c_longlong, c_uint, c_uint, POINTER(c_char), c_uint)
lib.ulMemWrite.argtypes = (c_longlong, c_uint, c_uint, POINTER(c_char), c_uint)
lib.ulCreateDaqDevice.argtype = Structure
lib.ulReleaseDaqDevice.argtype = c_longlong
lib.ulIsDaqDeviceConnected.argtype = c_longlong
lib.ulDisconnectDaqDevice.argtype = c_longlong
lib.ulFlashLed.argtypes = (c_longlong, c_int)
# Prototypes for the analog input subsystem
lib.ulAIn.argtypes = (c_longlong, c_uint, c_uint, c_uint, c_longlong, POINTER(c_double))
lib.ulAInScan.argtypes = (c_longlong, c_uint, c_uint, c_uint, c_uint, c_uint, POINTER(c_double), c_uint, c_uint,
                          POINTER(c_double))
lib.ulAInScanWait.argtypes = (c_longlong, c_uint, c_longlong, c_double)
lib.ulAInLoadQueue.argtypes = (c_longlong, POINTER(AiQueueElement), c_uint)
lib.ulAInSetTrigger.argtypes = (c_longlong, c_uint, c_int, c_double, c_double, c_uint)
lib.ulAInScanStatus.argtypes = (c_longlong, POINTER(c_uint), POINTER(TransferStatus))
lib.ulAISetConfig.argtypes = (c_longlong, c_uint, c_uint, c_longlong)
lib.ulAIGetConfig.argtypes = (c_longlong, c_uint, c_uint, POINTER(c_longlong))
lib.ulAISetConfigDbl.argtypes = (c_longlong, c_uint, c_uint, c_double)
lib.ulAIGetConfigDbl.argtypes = (c_longlong, c_uint, c_uint, POINTER(c_double))
lib.ulAIGetInfo.argtypes = (c_longlong, c_uint, c_uint, POINTER(c_longlong))
lib.ulAIGetInfoDbl.argtypes = (c_longlong, c_uint, c_uint, POINTER(c_double))
lib.ulAInScanStop.argtype = c_longlong
# Prototypes for the analog output subsystem
lib.ulAOut.argtypes = (c_longlong, c_int, c_uint, c_uint, c_double)
lib.ulAOutScan.argtypes = (c_longlong, c_int, c_int, c_uint, c_int, POINTER(c_double), c_uint, c_uint,
                           POINTER(c_double))
lib.ulAOutScanWait.argtypes = (c_longlong, c_uint, c_longlong, c_double)
lib.ulAOutScanStatus.argtypes = (c_longlong, POINTER(c_uint), POINTER(TransferStatus))
lib.ulAOutScanStop.argtype = c_longlong
lib.ulAOutSetTrigger.argtypes = (c_longlong, c_uint, c_uint, c_double, c_double, c_uint)
lib.ulAOGetInfo.argtypes = (c_longlong, c_uint, c_uint, POINTER(c_longlong))
lib.ulAOGetInfoDbl.argtypes = (c_longlong, c_uint, c_uint, POINTER(c_double))
# Prototypes for the DAQ input subsystem
lib.ulDaqInSetTrigger.argtypes = (c_longlong, c_uint, DaqInChanDescriptor, c_double, c_double, c_uint)
lib.ulDaqInScan.argtypes = (c_longlong, POINTER(DaqInChanDescriptor), c_int, c_int, POINTER(c_double), c_uint, c_uint,
                            POINTER(c_double))
lib.ulDaqInScanStatus.argtypes = (c_longlong, POINTER(c_uint), POINTER(TransferStatus))
lib.ulDaqInScanStop.argtype = c_longlong
lib.ulDaqIGetInfo.argtypes = (c_longlong, c_uint, c_uint, POINTER(c_longlong))
lib.ulDaqIGetInfoDbl.argtypes = (c_longlong, c_uint, c_uint, POINTER(c_double))
# Prototypes for DIO subsystem
lib.ulDIn.argtypes = (c_longlong, c_uint, POINTER(c_ulonglong))
lib.ulDOut.argtypes = (c_longlong, c_uint, c_ulonglong)
lib.ulDBitIn.argtypes = (c_longlong, c_uint, c_uint, POINTER(c_ulonglong))
lib.ulDBitOut.argtypes = (c_longlong, c_uint, c_uint, c_uint)
lib.ulDInScan.argtypes = (c_longlong, c_uint, c_uint, c_int, POINTER(c_double), c_uint, c_uint, POINTER(c_ulonglong))
lib.ulDOutScan.argtypes = (c_longlong, c_uint, c_uint, c_int, POINTER(c_double), c_uint, c_uint, POINTER(c_ulonglong))
lib.ulDInScanStatus.argtypes = (c_longlong, POINTER(c_uint), POINTER(TransferStatus))
lib.ulDOutScanStatus.argtypes = (c_longlong, POINTER(c_uint), POINTER(TransferStatus))
# prototypes for DAQ output subsystem
lib.ulDaqOutScan.argtypes = (c_longlong, POINTER(DaqOutChanDescriptor), c_int, c_int, POINTER(c_double), c_uint,
                             c_uint, POINTER(c_double))
lib.ulDaqOutScanWait.argtypes = (c_longlong, c_uint, c_longlong, c_double)
lib.ulDaqOutScanStatus.argtypes = (c_longlong, POINTER(c_uint), POINTER(TransferStatus))
lib.ulDaqOutScanStop.argtype = c_longlong
lib.ulDaqOutSetTrigger.argtypes = (c_longlong, c_uint, DaqInChanDescriptor, c_double, c_double, c_uint)
lib.ulDaqOGetInfo.argtypes = (c_longlong, c_uint, c_uint, POINTER(c_longlong))
lib.ulDaqOGetInfoDbl.argtypes = (c_longlong, c_uint, c_uint, POINTER(c_double))
# prototypes for counter subsystem
lib.ulCIn.argtypes = (c_longlong, c_int, POINTER(c_ulonglong))
lib.ulCRead.argtypes = (c_longlong, c_int, c_uint, POINTER(c_ulonglong))
lib.ulCLoad.argtypes = (c_longlong, c_int, c_uint, c_ulonglong)
lib.ulCClear.argtypes = (c_longlong, c_int)
lib.ulCConfigScan.argtypes = (c_longlong, c_int, c_uint, c_uint, c_uint, c_uint, c_uint, c_uint, c_uint)
lib.ulCInScan.argtypes = (c_longlong, c_int, c_int, c_int, POINTER(c_double), c_uint, c_uint, POINTER(c_ulonglong))
lib.ulCInSetTrigger.argtypes = (c_longlong, c_uint, c_int, c_double, c_double, c_uint)
lib.ulCInScanStatus.argtypes = (c_longlong, POINTER(c_uint), POINTER(TransferStatus))
lib.ulCInScanStop.argtype = c_longlong
lib.ulCInScanWait.argtypes = (c_longlong, c_uint, c_longlong, c_double)
lib.ulCtrGetInfo.argtypes = (c_longlong, c_uint, c_uint, POINTER(c_longlong))
lib.ulCtrGetInfoDbl.argtypes = (c_longlong, c_uint, c_uint, POINTER(c_double))
# Prototypes for the time subsystem
lib.ulTmrPulseOutStart.argtypes = (c_longlong, c_int, POINTER(c_double), POINTER(c_double), c_ulonglong,
                                   POINTER(c_double), c_uint, c_uint)
lib.ulTmrPulseOutStop.argtypes = (c_longlong, c_int)
lib.ulTmrPulseOutStatus.argtypes = (c_longlong, c_int, POINTER(c_uint))
lib.ulTmrSetTrigger.argtypes = (c_longlong, c_uint, c_int, c_double, c_double, c_uint)
lib.ulTmrGetInfo.argtypes = (c_longlong, c_uint, c_uint, POINTER(c_longlong))
lib.ulTmrGetInfoDbl.argtypes = (c_longlong, c_uint, c_uint, POINTER(c_double))
# Other Prototypes
lib.ulGetErrMsg.argtype = c_uint
lib.ulDevGetInfo.argtypes = (c_longlong, c_uint, c_uint, POINTER(c_longlong))
lib.ulMemGetInfo.argtypes = (c_longlong, c_uint, POINTER(MemDescriptor))
