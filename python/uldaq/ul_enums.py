"""
Created on Mar 29 2018

@author: MCC
"""
from enum import IntEnum


class ULError(IntEnum):
    """Error codes for Universal Library."""
    NO_ERROR = 0,  #: No error has occurred
    UNHANDLED_EXCEPTION = 1,  #: Unhandled internal exception
    BAD_DEV_HANDLE = 2,  #: Invalid device handle
    BAD_DEV_TYPE = 3,  #: This function cannot be used with this device
    USB_DEV_NO_PERMISSION = 4,  #: Insufficient permission to access this device
    USB_INTERFACE_CLAIMED = 5,  #: USB interface is already claimed
    DEV_NOT_FOUND = 6,  #: Device not found
    DEV_NOT_CONNECTED = 7,  #: Device not connected or connection lost
    DEAD_DEV = 8,  #: Device no longer responding
    BAD_BUFFER_SIZE = 9,  #: Buffer too small for operation
    BAD_BUFFER = 10,  #: Invalid buffer
    BAD_MEM_TYPE = 11,  #: Invalid memory type
    BAD_MEM_REGION = 12,  #: Invalid memory region
    BAD_RANGE = 13,  #: Invalid range
    BAD_AI_CHAN = 14,  #: Invalid analog input channel specified
    BAD_INPUT_MODE = 15,  #: Invalid input mode specified
    ALREADY_ACTIVE = 16,  #: A background process is already in progress
    BAD_TRIG_TYPE = 17,  #: Invalid trigger type specified
    OVERRUN = 18,  #: FIFO overrun, data was not transferred from device fast enough
    UNDERRUN = 19,  #: FIFO underrun, data was not transferred to device fast enough
    TIMEDOUT = 20,  #: Operation timed out
    BAD_OPTION = 21,  #: Invalid option specified
    BAD_RATE = 22,  #: Invalid sampling rate specified
    BAD_BURSTIO_COUNT = 23,  #: Sample count cannot be greater than FIFO size for BURSTIO scans
    CONFIG_NOT_SUPPORTED = 24,  #: Configuration not supported
    BAD_CONFIG_VAL = 25,  #: Invalid configuration value
    BAD_AI_CHAN_TYPE = 26,  #: Invalid analog input channel type specified
    ADC_OVERRUN = 27,  #: ADC overrun occurred
    BAD_TC_TYPE = 28,  #: Invalid thermocouple type specified
    BAD_UNIT = 29,  #: Invalid unit specified
    BAD_QUEUE_SIZE = 30,  #: Invalid queue size
    BAD_CONFIG_ITEM = 31,  #: Invalid config item specified
    BAD_INFO_ITEM = 32,  #: Invalid info item specified
    BAD_FLAG = 33,  #: Invalid flag specified
    BAD_SAMPLE_COUNT = 34,  #: Invalid sample count specified
    INTERNAL = 35,  #: Internal error
    BAD_COUPLING_MODE = 36,  #: Invalid coupling mode
    BAD_SENSOR_SENSITIVITY = 37,  #: Invalid sensor sensitivity
    BAD_IEPE_MODE = 38,  #: Invalid IEPE mode
    BAD_AI_CHAN_QUEUE = 39,  #: Invalid channel queue specified
    BAD_AI_GAIN_QUEUE = 40,  #: Invalid gain queue specified
    BAD_AI_MODE_QUEUE = 41,  #: Invalid mode queue specified
    FPGA_FILE_NOT_FOUND = 42,  #: FPGA file not found
    UNABLE_TO_READ_FPGA_FILE = 43,  #: Unable to read FPGA file
    NO_FPGA = 44,  #: FPGA not loaded
    BAD_ARG = 45,  #: Invalid argument
    MIN_SLOPE_VAL_REACHED = 46,  #: Minimum slope value reached
    MAX_SLOPE_VAL_REACHED = 47,  #: Maximum slope value reached
    MIN_OFFSET_VAL_REACHED = 48,  #: Minimum offset value reached
    MAX_OFFSET_VAL_REACHED = 49,  #: Maximum offset value reached
    BAD_PORT_TYPE = 50,  #: Invalid port type specified
    WRONG_DIG_CONFIG = 51,  #: Digital I/O is configured incorrectly
    BAD_BIT_NUM = 52,  #: Invalid bit number
    BAD_PORT_VAL = 53,  #: Invalid port value specified
    BAD_RETRIG_COUNT = 54,  #: Invalid re-trigger count
    BAD_AO_CHAN = 55,  #: Invalid analog output channel specified
    BAD_DA_VAL = 56,  #: Invalid D/A output value specified
    BAD_TMR = 57,  #: Invalid timer specified
    BAD_FREQUENCY = 58,  #: Invalid frequency specified
    BAD_DUTY_CYCLE = 59,  #: Invalid duty cycle specified
    BAD_INITIAL_DELAY = 60,  #: Invalid initial delay specified
    BAD_CTR = 61,  #: Invalid counter specified
    BAD_CTR_VAL = 62,  #: Invalid counter value specified
    BAD_DAQI_CHAN_TYPE = 63,  #: Invalid DAQ input channel type specified
    BAD_NUM_CHANS = 64,  #: Invalid number of channels specified
    BAD_CTR_REG = 65,  #: Invalid counter register specified
    BAD_CTR_MEASURE_TYPE = 66,  #: Invalid counter measurement type specified
    BAD_CTR_MEASURE_MODE = 67,  #: Invalid counter measurement mode specified
    BAD_DEBOUNCE_TIME = 68,  #: Invalid debounce time specified
    BAD_DEBOUNCE_MODE = 69,  #: Invalid debounce mode specified
    BAD_EDGE_DETECTION = 70,  #: Invalid edge detection mode specified
    BAD_TICK_SIZE = 71,  #: Invalid tick size specified
    BAD_DAQO_CHAN_TYPE = 72,  #: Invalid DAQ output channel type specified
    NO_CONNECTION_ESTABLISHED = 73,  #: No connection established
    BAD_EVENT_TYPE = 74,  #: Invalid event type specified
    EVENT_ALREADY_ENABLED = 75,  #: An event handler has already been enabled for this event type
    BAD_EVENT_SIZE = 76,  #: Invalid event count specified
    BAD_CALLBACK_FUCNTION = 77,  #: Invalid callback function specified
    BAD_MEM_ADDRESS = 78,  #: Invalid memory address
    MEM_ACCESS_DENIED = 79,  #: Memory access denied
    DEV_UNAVAILABLE = 80,  #: Device is not available at time of request
    BAD_RETRIG_TRIG_TYPE = 81,  #: Re-trigger option is not supported for the specified trigger type
    BAD_DESCRIPTOR = 100001,  #: Invalid descriptor


class InterfaceType(IntEnum):
    """The connection interface used to communicate with a DAQ device."""
    USB = 1 << 0  #: USB interface
    BLUETOOTH = 1 << 1  #: Bluetooth interface
    ETHERNET = 1 << 2  #: Ethernet interface
    ANY = USB | BLUETOOTH | ETHERNET  #: Any interface


class DaqEventType(IntEnum):
    """Conditions that trigger an event."""
    NONE = 0,  #: No trigger
    #: Generates an event when the number of samples acquired during an input scan increases by eventParameter samples
    #: or more.
    ON_DATA_AVAILABLE = 1 << 0,
    #: Generates an event when an input scan error occurs.
    ON_INPUT_SCAN_ERROR = 1 << 1,
    #: Generates an event upon completion or error of an input scan operation such as ulAInScan().
    ON_END_OF_INPUT_SCAN = 1 << 2,
    #: Generates an event when an output scan error occurs.
    ON_OUTPUT_SCAN_ERROR = 1 << 3,
    #: Generates an event upon completion or error of an output scan operation such as ulAOutScan().
    ON_END_OF_OUTPUT_SCAN = 1 << 4,


class WaitType(IntEnum):
    """Data transfer options."""
    #: Data is transferred when the operation completes
    WAIT_UNTIL_DONE = 1 << 0,


class DevVersionType(IntEnum):
    """Firmware version types."""
    FW_MAIN = 0,  #: Firmware version installed on the current device.
    FPGA = 1,  #: FPGA version installed on the current device.
    RADIO = 2,  #: Radio firmware version installed on the current device.


class MemAccessType(IntEnum):
    """Types of memory access."""
    #: Read and write memory
    READ = 1 << 0,
    #: Write memory
    WRITE = 1 << 1,


class MemRegion(IntEnum):
    """Reserved areas of memory."""
    #: Calibration region
    CAL = 1 << 0,
    #: User region
    USER = 1 << 1,
    #: Settings region
    SETTINGS = 1 << 2,


class AiInputMode(IntEnum):
    """Defines the possible modes for an analog input channel."""
    DIFFERENTIAL = 1,  #: Differential
    SINGLE_ENDED = 2,  #: Single-ended
    PSEUDO_DIFFERENTIAL = 3,  #: Pseudo-differential


class AiChanType(IntEnum):
    """A/D channel types."""
    #: Voltage
    VOLTAGE = 1 << 0,
    #: Thermocouple
    TC = 1 << 1,
    #: Resistance Temperature Detector (RTD)
    RTD = 1 << 2,
    #: Thermistor
    THERMISTOR = 1 << 3,
    #: Semiconductor
    SEMICONDUCTOR = 1 << 4,
    #: Disabled
    DISABLED = 1 << 30,


class AInFlag(IntEnum):
    """Options for analog input functions"""
    DEFAULT = 0,  #: Transfers A/D data based on the board type and sampling speed.
    #: No scaling is applied to raw data.
    NOSCALEDATA = 1 << 0,
    #: Turns off real-time software calibration for devices that are software calibrated.
    NOCALIBRATEDATA = 1 << 1,


class AInScanFlag(IntEnum):
    """Scan options for analog input scan functions."""
    DEFAULT = 0,  #: Transfers A/D data based on the board type and sampling speed.
    #: No scaling is applied to raw data.
    NOSCALEDATA = 1 << 0,
    #: Turns off real-time software calibration for devices that are software calibrated.
    NOCALIBRATEDATA = 1 << 1,


class Range(IntEnum):
    """Analog range values."""
    BIP60VOLTS = 1,  #: -60 to +60 Volts
    BIP30VOLTS = 2,  #: -30 to +30 Volts
    BIP15VOLTS = 3,  #: -15 to +15 Volts
    BIP20VOLTS = 4,  #: -20 to +20 Volts
    BIP10VOLTS = 5,  #: -10 to +10 Volts
    BIP5VOLTS = 6,  #: -5 to +5 Volts
    BIP4VOLTS = 7,  #: -4 to +4 Volts
    BIP2PT5VOLTS = 8,  #: -2.5 to +2.5 Volts
    BIP2VOLTS = 9,  #: -2.0 to +2.0 Volts
    BIP1PT25VOLTS = 10,  #: -1.25 to +1.25 Volts
    BIP1VOLTS = 11,  #: -1 to +1 Volts
    BIPPT625VOLTS = 12,  #: -.625 to +.625 Volts
    BIPPT5VOLTS = 13,  #: -.5 to +.5 Volts
    BIPPT25VOLTS = 14,  #: -0.25 to +0.25 Volts
    BIPPT125VOLTS = 15,  #: -0.125 to +0.125 Volts
    BIPPT2VOLTS = 16,  #: -0.2 to +0.2 Volts
    BIPPT1VOLTS = 17,  #: -.1 to +.1 Volts
    BIPPT078VOLTS = 18,  #: -0.078 to +0.078 Volts
    BIPPT05VOLTS = 19,  #: -.05 to +.05 Volts
    BIPPT01VOLTS = 20,  #: -.01 to +.01 Volts
    BIPPT005VOLTS = 21,  #: -.005 to +.005 Volts
    UNI60VOLTS = 1001,  #: 0 to +60 Volts
    UNI30VOLTS = 1002,  #: 0 to +30 Volts
    UNI15VOLTS = 1003,  #: 0 to +15 Volts
    UNI20VOLTS = 1004,  #: 0 to +20 Volts
    UNI10VOLTS = 1005,  #: 0 to +10 Volts
    UNI5VOLTS = 1006,  #: 0 to +5 Volts
    UNI4VOLTS = 1007,  #: 0 to +4 Volts
    UNI2PT5VOLTS = 1008,  #: 0 to +2.5 Volts
    UNI2VOLTS = 1009,  #: 0 to +2.0 Volts
    UNI1PT25VOLTS = 1010,  #: 0 to +1.25 Volts
    UNI1VOLTS = 1011,  #: 0 to +1 Volts
    UNIPT625VOLTS = 1012,  #: 0 to +.625 Volts
    UNIPT5VOLTS = 1013,  #: 0 to +.5 Volts
    UNIPT25VOLTS = 1014,  #: 0 to +0.25 Volts
    UNIPT125VOLTS = 1015,  #: 0 to +0.125 Volts
    UNIPT2VOLTS = 1016,  #: 0 to +0.2 Volts
    UNIPT1VOLTS = 1017,  #: 0 to +.1 Volts
    UNIPT078VOLTS = 1018,  #: 0 to +0.078 Volts
    UNIPT05VOLTS = 1019,  #: 0 to +.05 Volts
    UNIPT01VOLTS = 1020,  #: 0 to +.01 Volts
    UNIPT005VOLTS = 1021,  #: 0 to +.005 Volts


class ScanOption(IntEnum):
    """Scan options."""
    DEFAULTIO = 0,  #: Transfers A/D data based on the board type and sampling speed.
    #: Transfers one packet of data at a time.
    SINGLEIO = 1 << 0,
    #: Transfers A/D data in blocks.
    BLOCKIO = 1 << 1,
    #: Transfers A/D data from the FIFO after the scan completes. Allows maximum rates for finite scans up to the full
    #: capacity of the FIFO. Not recommended for slow acquisition rates.
    BURSTIO = 1 << 2,
    #: Scans data in an endless loop. The only way to stop the operation is with ulAInScanStop().
    CONTINUOUS = 1 << 3,
    #: Data conversions are controlled by an external clock signal.
    EXTCLOCK = 1 << 4,
    #: Sampling begins when a trigger condition is met.
    EXTTRIGGER = 1 << 5,
    #: Re-arms the trigger after a trigger event is performed.
    RETRIGGER = 1 << 6,
    #: Enables burst mode sampling, minimizing the channel skew.
    BURSTMODE = 1 << 7,
    #: Enables or disables the internal pacer output on a DAQ device.
    PACEROUT = 1 << 8,


class ScanStatus(IntEnum):
    """Scan status."""
    IDLE = 0,  #: scan is idle
    RUNNING = 1,  #: scan is running


class TriggerType(IntEnum):
    """Trigger types based on the trigger source."""
    NONE = 0,  #: No trigger
    #: Scanning begins when the external digital trigger transitions from 0V to 5V (logic LOW to HIGH)
    POS_EDGE = 1 << 0,
    #: Scanning begins when the external digital trigger transitions from 5V to 0V (logic HIGH to LOW)
    NEG_EDGE = 1 << 1,
    #: Scanning begins when the external digital trigger is 5V (logic HIGH or '1')
    HIGH = 1 << 2,
    #: Scanning begins when the external digital trigger is 0V (logic LOW or '0')
    LOW = 1 << 3,
    #: Scanning is enabled as long as the external digital trigger input is 5V (logic HIGH or '1').
    GATE_HIGH = 1 << 4,
    #: Scanning is enabled as long as the external digital trigger input is 0V (logic LOW or '0').
    GATE_LOW = 1 << 5,
    #: Scanning begins when the external analog trigger input transitions from below lowThreshold to above
    #: highThreshold.
    RISING = 1 << 6,
    #: Scanning begins when the external analog trigger input transitions from above highThreshold to below
    #: lowThreshold.
    FALLING = 1 << 7,
    #: Scanning begins when the external analog trigger input transitions from below highThreshold to above.
    ABOVE = 1 << 8,
    #: Scanning begins when the external analog trigger input transitions from above lowThreshold to below.
    BELOW = 1 << 9,
    #: Scanning is enabled as long as the external analog trigger input is more positive than highThreshold.
    GATE_ABOVE = 1 << 10,
    #: Scanning is enabled as long as the external analog trigger input is more negative than lowThreshold.
    GATE_BELOW = 1 << 11,
    #: Scanning is enabled as long as the external analog trigger is inside the region defined by lowThreshold and
    #: highThreshold.
    GATE_IN_WINDOW = 1 << 12,
    #: Scanning is enabled as long as the external analog trigger is outside the region defined by lowThreshold and
    #: highThreshold.
    GATE_OUT_WINDOW = 1 << 13,
    #: Scanning begins when the digital port value AND bitwise mask are equal to the pattern value AND bitwise mask.
    PATTERN_EQ = 1 << 14,
    #: Scanning begins when the digital port value AND bitwise mask are not equal to the pattern value AND bitwise mask.
    PATTERN_NE = 1 << 15,
    #: Scanning begins when the digital port value AND bitwise mask are greater than the pattern value AND bitwise mask.
    PATTERN_ABOVE = 1 << 16,
    #: Scanning begins when the digital port value AND bitwise mask are less than the pattern value AND bitwise mask.
    PATTERN_BELOW = 1 << 17,


class AdcTimingMode(IntEnum):
    """ADC timing modes."""
    AUTO = 1,  #: The timing mode is set automatically based on TBD
    HIGH_RES = 2,  #: High resolution timing mode
    HIGH_SPEED = 3,  #: High speed timing mode


class AiQueueType(IntEnum):
    """Queue types supported by the AI subsystem."""
    #: The AI subsystem supports a channel queue.
    CHAN = 1 << 0,
    #: The AI subsystem supports a gain queue.
    GAIN = 1 << 1,
    #: The AI subsystem supports a mode queue.
    MODE = 1 << 2,


class AiChanQueueLimitation(IntEnum):
    """Channel queue limitations."""
    #: A particular channel number cannot appear more than once in the queue.
    UNIQUE_CHAN = 1 << 0,
    #: Channel numbers must be listed in ascending order within the queue.
    ASCENDING_CHAN = 1 << 1,
    #: Channel numbers must be listed in consecutive order within the queue.
    CONSECUTIVE_CHAN = 1 << 2,


class AutoZeroMode(IntEnum):
    """Auto zero modes."""
    NONE = 1,  #: Disabled
    EVERY_SAMPLE = 2,  #: Perform auto zero on every thermocouple reading
    ONCE = 3,  #: Perform auto zero before every scan


class CouplingMode(IntEnum):
    """Coupling modes."""
    DC = 1,  #: DC coupling
    AC = 2,  #: AC coupling


class IepeMode(IntEnum):
    """IEPE modes."""
    DISABLED = 1,  #: IEPE excitation current is disabled
    ENABLED = 2,  #: IEPE excitation current is enabled


class TcType(IntEnum):
    """Thermocouple types."""
    J = 1,  #: Type J
    K = 2,  #: Type K
    T = 3,  #: Type T
    E = 4,  #: Type E
    R = 5,  #: Type R
    S = 6,  #: Type S
    B = 7,  #: Type B
    N = 8,  #: Type N


class TempUnit(IntEnum):
    """Temperature units."""
    CELSIUS = 1,  #: Celcius
    FAHRENHEIT = 2,  #: Fahrenheit
    KELVIN = 3,  #: Kelvin


class DigitalDirection(IntEnum):
    """Digital port direction."""
    INPUT = 1,  #: Input
    OUTPUT = 2,  #: Output


class DigitalPortIoType(IntEnum):
    """Digital port I/O capabilities."""
    IN = 1,  #: Fixed input port
    OUT = 2,  #: Fixed output port
    IO = 3,  #: Bidirectional (input or output) port
    BITIO = 4,  #: Bitwise configurable
    NONCONFIG = 5,  #: Bidirectional (input or output) port; configuration is not required.


class DigitalPortType(IntEnum):
    """Digital port type."""
    AUXPORT = 1,  #: AuxPort
    AUXPORT0 = 1,  #: AuxPort0
    AUXPORT1 = 2,  #: AuxPort1
    AUXPORT2 = 3,  #: AuxPort2
    FIRSTPORTA = 10,  #: FirstPortA
    FIRSTPORTB = 11,  #: FirstPortB
    FIRSTPORTC = 12,  #: FirstPortC
    FIRSTPORTCL = 12,  #: FirstPortC Low
    FIRSTPORTCH = 13,  #: FirstPortC High
    SECONDPORTA = 14,  #: SecondPortA
    SECONDPORTB = 15,  #: SecondPortB
    SECONDPORTCL = 16,  #: SecondPortC Low
    SECONDPORTCH = 17,  #: SecondPortC High
    THIRDPORTA = 18,  #: ThirdPortA
    THIRDPORTB = 19,  #: ThirdPortB
    THIRDPORTCL = 20,  #: ThirdPortC Low
    THIRDPORTCH = 21,  #: ThirdPortC High
    FOURTHPORTA = 22,  #: FourthPortA
    FOURTHPORTB = 23,  #: FourthPortB
    FOURTHPORTCL = 24,  #: FourthPortC Low
    FOURTHPORTCH = 25,  #: FourthPortC High
    FIFTHPORTA = 26,  #: FifthPortA
    FIFTHPORTB = 27,  #: FifthPortB
    FIFTHPORTCL = 28,  #: FifthPortC Low
    FIFTHPORTCH = 29,  #: FifthPortC High
    SIXTHPORTA = 30,  #: SixthPortA
    SIXTHPORTB = 31,  #: SixthPortB
    SIXTHPORTCL = 32,  #: SixthPortC Low
    SIXTHPORTCH = 33,  #: SixthPortC High
    SEVENTHPORTA = 34,  #: SeventhPortA
    SEVENTHPORTB = 35,  #: SeventhPortB
    SEVENTHPORTCL = 36,  #: SeventhPortC Low
    SEVENTHPORTCH = 37,  #: SeventhPortC High
    EIGHTHPORTA = 38,  #: EighthPortA
    EIGHTHPORTB = 39,  #: EighthPortB
    EIGHTHPORTCL = 40,  #: EighthPortC Low
    EIGHTHPORTCH = 41,  #: EighthPortC High


class DInScanFlag(IntEnum):
    """ Scan options for digital input functions."""
    DEFAULT = 0,  # Transfers digital data based on the board type and sampling speed.


class DOutScanFlag(IntEnum):
    """ Scan options for digital output functions."""
    DEFAULT = 0,  # Transfers counter data based on the board type and sampling speed.


class DaqInScanFlag(IntEnum):
    """Scan options for synchronous input functions."""
    DEFAULT = 0,  #: Transfers synchronous A/D data based on the board type and sampling speed.
    #: No scaling is applied to raw data.
    NOSCALEDATA = 1 << 0,
    #: Turns off real-time software calibration for devices that are software calibrated.
    NOCALIBRATEDATA = 1 << 1,
    #: Counters are not cleared (set to 0) when a scan starts
    NOCLEAR = 1 << 3,


class DaqInChanType(IntEnum):
    """Channel types for synchronous operations."""
    #: Analog input channel, differential mode
    ANALOG_DIFF = 1 << 0,
    #: Analog input channel, single-ended mode
    ANALOG_SE = 1 << 1,
    #: Digital channel
    DIGITAL = 1 << 2,
    #: 16-bit counter channel
    CTR16 = 1 << 3,
    #: 32-bit counter channel
    CTR32 = 1 << 4,
    #: 48-bit counter channel
    CTR48 = 1 << 5,


class AOutFlag(IntEnum):
    """Options for scaling and calibrating D/A data."""
    #: Transfers D/A data based on the board type and sampling speed.
    DEFAULT = 0,
    #: No scaling is applied to raw data.
    NOSCALEDATA = 1 << 0,
    #: Turns off real-time software calibration for devices that are software calibrated.
    NOCALIBRATEDATA = 1 << 1,


class AOutScanFlag(IntEnum):
    """Options for scaling and calibrating D/A data."""
    #: Transfers D/A data based on the board type and sampling speed.
    DEFAULT = 0,
    #: No scaling is applied to raw data.
    NOSCALEDATA = 1 << 0,
    #: Turns off real-time software calibration for devices that are software calibrated.
    NOCALIBRATEDATA = 1 << 1,


class DaqOutChanType(IntEnum):
    """Channel types for synchronous output operations."""
    #: Analog output channel.
    ANALOG = 1 << 0,
    #: Digital output channl.
    DIGITAL = 1 << 1,


class DaqOutScanFlag(IntEnum):
    """Options for scaling and calibrating DAQ output data."""
    #: Transfers data based on the board type and sampling speed.
    DEFAULT = 0,
    #: No scaling is applied to raw data.
    NOSCALEDATA = 1 << 0,
    #: Turns off real-time software calibration for devices that are software calibrated.
    NOCALIBRATEDATA = 1 << 1,


class CConfigScanFlag(IntEnum):
    """Counter scan options."""
    DEFAULT = 0,  #: No scan option applied


class CInScanFlag(IntEnum):
    """Scan options for counter input functions."""
    #: Transfers counter data based on the board type and sampling speed.
    DEFAULT = 0,
    #: 16-bit counter channel
    CTR16_BIT = 1 << 0,
    #: 32-bit counter channel
    CTR32_BIT = 1 << 1,
    #: 64-bit counter channel
    CTR64_BIT = 1 << 2,
    #: Disables the clearing of counters when the scan starts.
    NOCLEAR = 1 << 3,


class CounterDebounceMode(IntEnum):
    """Counter debounce modes."""
    #: Disables the debounce feature.
    NONE = 0,
    #: Rejects glitches and only passes state transitions after a specified period of stability (the debounce time).
    TRIGGER_AFTER_STABLE = 1,
    #: Use when the input signal has groups of glitches and each group is to be counted as one
    TRIGGER_BEFORE_STABLE = 2,


class CounterDebounceTime(IntEnum):
    """Counter debounce times."""
    DEBOUNCE_0ns = 0,  #: Sets the counter channel's comparator output to 0 ns.
    DEBOUNCE_500ns = 1,  #: Sets the counter channel's comparator output to 500 ns.
    DEBOUNCE_1500ns = 2,  #: Sets the counter channel's comparator output to 1500 ns.
    DEBOUNCE_3500ns = 3,  #: Sets the counter channel's comparator output to 3500 ns.
    DEBOUNCE_7500ns = 4,  #: Sets the counter channel'ss comparator output to 7500 ns.
    DEBOUNCE_15500ns = 5,  #: Sets the counter channel's comparator output to 15500 ns.
    DEBOUNCE_31500ns = 6,  #: Sets the counter channel's comparator output to 31500 ns.
    DEBOUNCE_63500ns = 7,  #: Sets the counter channel's comparator output to 63500 ns.
    DEBOUNCE_127500ns = 8,  #: Sets the counter channel's comparator output to 127500 ns.
    DEBOUNCE_100us = 9,  #: Sets the counter channel's comparator output to 100 us.
    DEBOUNCE_300us = 10,  #: Sets the counter channel's comparator output to 300 us.
    DEBOUNCE_700us = 11,  #: Sets the counter channel's comparator output to 700 us.
    DEBOUNCE_1500us = 12,  #: Sets the counter channel's comparator output to 1500 us.
    DEBOUNCE_3100us = 13,  #: Sets the counter channel'ss comparator output to 3100 us.
    DEBOUNCE_6300us = 14,  #: Sets the counter channel's comparator output to 6300 us.
    DEBOUNCE_12700us = 15,  #: Sets the counter channel'ss comparator output to 12700 us.
    DEBOUNCE_25500us = 16,  #: Sets the counter channel's comparator output to 25500 us.


class CounterEdgeDetection(IntEnum):
    """Counter edge detection."""
    RISING_EDGE = 1,  #: Rising edge
    FALLING_EDGE = 2,  #: Falling edge


class CounterMeasurementMode(IntEnum):
    """Counter modes."""
    #: Counter mode
    DEFAULT = 0,
    #: The counter is cleared after every read.
    CLEAR_ON_READ = 1 << 0,
    #: The counter counts down.
    COUNT_DOWN = 1 << 1,
    #: The gate input controls the direction of the counter. By default, the counter increments when
    #: the gate pin is high, and decrements when the gate pin is low.
    GATE_CONTROLS_DIR = 1 << 2,
    #: The gate input clears the counter. By default, the counter is cleared when the gate input is high.
    GATE_CLEARS_CTR = 1 << 3,
    #: The counter starts counting when the gate input goes active. By default, active is on the rising edge.
    #: The gate is re-armed when the counter is loaded and when ulCConfigScan() is called.
    GATE_TRIG_SRC = 1 << 4,
    #: Enables the counter output. By default, the counter output goes high when the counter reaches the
    #: value of output register 0, and low when the counter reaches the value of output register 1.
    #: Use ulCLoad() to set or read the value of the output registers.
    OUTPUT_ON = 1 << 5,
    #: Sets the initial state of the counter output pin high.
    OUTPUT_INITIAL_STATE_HIGH = 1 << 6,
    #: Enables Non-recycle counting mode, in which the counter stops counting whenever a count overflow or underflow
    #: takes place.  Counting restarts when a clear or a load operation is performed on the counter, or the count
    #: direction changes.
    NO_RECYCLE = 1 << 7,
    #: Enables Range Limit counting mode, in which an upper and lower limit is set.
    #: Use ulCLoad() to set the upper and lower limits. Set the upper limit by loading the max limit register, and the
    #: lower limit by loading the min limit register. Note that on some devices the lower limit is programmable, but on
    #: other devices the lower limit is always 0. When counting up, the counter rolls over to min limit when the max
    #: limit is reached. When counting down, the counter rolls over to max limit when the min limit is reached. When
    #: counting up with NO_RECYCLE enabled, the counter freezes whenever the count reaches the value that was loaded
    #: into the max limit register. When counting down with NO_RECYCLE enabled, the counter freezes whenever the count
    #: reaches the value that was loaded into the min limit register. Counting resumes if the counter is reset or the
    #: direction changes.
    RANGE_LIMIT_ON = 1 << 8,
    #: The counter is enabled when the mapped channel or the gate pin that is used to gate the counter is high.
    #: When the mapped channel/gate pin is low, the counter is disabled but holds the count value. By default,
    #: the counter gating option is set to "off."
    GATING_ON = 1 << 9,
    #: Inverts the polarity of the gate input.
    INVERT_GATE = 1 << 10,
    #: The measurement is latched each time 1 complete period is observed.
    PERIOD_X1 = 0,
    #: The measurement is latched each time 10 complete periods are observed.
    PERIOD_X10 = 1 << 11,
    #: The measurement is latched each time 100 complete periods are observed.
    PERIOD_X100 = 1 << 12,
    #: The measurement is latched each time 1000 complete periods are observed.
    PERIOD_X1000 = 1 << 13,
    #: The counter is enabled when the mapped channel or the gate pin that is used to gate the counter is high.
    #: When the mapped channel/gate pin is low, the counter is disabled but holds the count value. By default,
    #: the counter gating option is set to "off."
    PERIOD_GATING_ON = 1 << 14,
    #: Inverts the polarity of the gate input.
    PERIOD_INVERT_GATE = 1 << 15,
    #: Pulse width mode
    PULSE_WIDTH_DEFAULT = 0,
    #: The counter is enabled when the mapped channel or the gate pin that is used to gate the counter is high.
    #: When the mapped channel/gate pin is low, the counter is disabled but holds the count value. By default,
    #: the counter gating option is set to "off."
    PULSE_WIDTH_GATING_ON = 1 << 16,
    #: Inverts the polarity of the gate input.
    PULSE_WIDTH_INVERT_GATE = 1 << 17,
    #: Timing mode
    TIMING_DEFAULT = 0,
    #: Inverts the polarity of the gate input.
    TIMING_MODE_INVERT_GATE = 1 << 18,
    #: Sets the encoder measurement mode to X1.
    ENCODER_X1 = 0,
    #: Sets the encoder measurement mode to X2.
    ENCODER_X2 = 1 << 19,
    #: Sets the encoder measurement mode to X4.
    ENCODER_X4 = 1 << 20,
    #: Selects the encoder Z mapped signal to latch the counter outputs; this allows the user to know the exact
    #: counter value when an edge is present on another counter.
    ENCODER_LATCH_ON_Z = 1 << 21,
    #: The counter is cleared when the index (Z input) goes active. By default, the "clear on Z" option is off, and
    #: the counter is not cleared.
    ENCODER_CLEAR_ON_Z = 1 << 22,
    #: The counter is disabled whenever a count overflow or underflow takes place, and re-enabled when a clear or
    #: load operation is performed on the counter.
    ENCODER_NO_RECYCLE = 1 << 23,
    #: Enables Range Limit counting mode, in which an upper and lower limit is set.
    #: Use ulCLoad() to set the upper and lower limits. Set the upper limit by loading the max limit register, and the
    #: lower limit by loading the min limit register. Note that on some devices the lower limit is programmable, but on
    #: other devices the lower limit is always 0.  When counting up, the counter rolls over to min limit when the max
    #: limit is reached. When counting down, the counter rolls over to max limit when the min limit is reached. When
    #: counting up with NO_RECYCLE enabled, the counter freezes whenever the count reaches the value that was loaded
    #: into the max limit register. When counting down with NO_RECYCLE enabled, the counter freezes whenever the count
    #: reaches the value that was loaded into the min limit register. Counting resumes if the counter is reset or the
    #: direction changes.
    ENCODER_RANGE_LIMIT_ON = 1 << 24,
    #: Sets the encoder Z signal as the active edge.
    ENCODER_Z_ACTIVE_EDGE = 1 << 25,


class CounterMeasurementType(IntEnum):
    """Counter measurement types."""
    #: Counter measurement
    COUNT = 1 << 0,
    #: Period measurement
    PERIOD = 1 << 1,
    #: Pulse width measurement
    PULSE_WIDTH = 1 << 2,
    #: Timing measurement
    TIMING = 1 << 3,
    #: Encoder measurement
    ENCODER = 1 << 4,


class CounterRegisterType(IntEnum):
    """Counter register types."""
    #: Counter register
    COUNT = 1 << 0,
    #: Load register
    LOAD = 1 << 1,
    #: Max Limit register
    MIN_LIMIT = 1 << 2,
    #: Min Limit register
    MAX_LIMIT = 1 << 3,
    OUTPUT_VAL0 = 1 << 4,
    OUTPUT_VAL1 = 1 << 5,


class CounterTickSize(IntEnum):
    """Counter tick sizes."""
    TICK_20PT83ns = 1,  #: 20.83 ns
    TICK_208PT3ns = 2,  #: 208.3 ns
    TICK_2083PT3ns = 3,  #: 2083.3 ns
    TICK_20833PT3ns = 4,  #: 20833.3 ns
    TICK_20ns = 11,  #: 20 ns
    TICK_200ns = 12,  #: 200 ns
    TICK_2000ns = 13,  #: 2000 ns
    TICK_20000ns = 14,  #: 20000 ns


class TimerType(IntEnum):
    """Types of timer channels."""
    STANDARD = 1,  #: Programmable frequency timer
    ADVANCED = 2,  #: Programmable frequency timer, plus other attributes such as pulse width


class TmrIdleState(IntEnum):
    """Timer idle state."""
    LOW = 1,  #: Idle low
    HIGH = 2,  #: Idle high


class TmrStatus(IntEnum):
    """Status for the timer subsystem."""
    IDLE = 0,  #: Timer is idle
    RUNNING = 1,  #: Timer is running


class PulseOutOption(IntEnum):
    """Pulse out options."""
    #: No PulseOut options are applied.
    PO_DEFAULT = 0,
    #: Output pulses are generated when a trigger condition is met.
    PO_EXTTRIGGER = 1 << 5,
    #: Output pulses are automatically retriggered.
    PO_RETRIGGER = 1 << 6,
