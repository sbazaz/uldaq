/*
 * uldaq.h
 *
 *      Author: Measurement Computing Corporation
 */

#ifndef UL_DAQ_H_
#define UL_DAQ_H_

#ifdef __cplusplus
extern "C"
{
#endif



/** \brief The connection interface used to communicate with a DAQ device. */
typedef enum
{
	/** USB interface */
	USB_IFC			= 1 << 0,

	/** Bluetooth interface */
	BLUETOOTH_IFC	= 1 << 1,

	/** Ethernet interface */
	ETHERNET_IFC	= 1 << 2,

	/** Any interface */
	ANY_IFC = USB_IFC | BLUETOOTH_IFC | ETHERNET_IFC

}DaqDeviceInterface;

/** \brief A structure representing the DAQ device.
 *
*/
struct DaqDeviceDescriptor
{
	/** The generic (unqualified) product name, except for Bluetooth devices
	 * connected through USB. For these devices, the product name with a
	 * "USB-" prefix is returned. <br>For a virtual device, an empty string is returned. */
	char productName[64];

	/**The numeric string indicating the product type.*/
	unsigned int productId;

	/**
	 * The #DaqDeviceInterface enumeration indicating the type of interface referenced by
	 * the current instance of DaqDeviceInterface.
	 */
	DaqDeviceInterface devInterface;

	/**
	 * A unique (fully-qualified) name that identifies a specific DAQ device.
	 * For a Bluetooth device, this value is the product name with a partial serial number
	 * appended. <br>For a USB device, this value is a bus location. <br>For an Ethernet device,
	 * this value represents a NetBIOS name. <br> For a virtual device, an empty string is returned.<br>
	 * This value can be used to differentiate between multiple devices of the same product type.
	 */
	char devString[64];

	/**
	 * The numeric string indicating either the serial number (for USB devices,
	 * or Bluetooth devices connected through USB), or the MAC address (for Bluetooth devices paired
	 * with the system.) <br>For a virtual device, an empty string is returned.
	 */
	char uniqueId[64];

	/** Reserved for future use */
	char reserved[512];
};

/** \brief A structure representing the DAQ device descriptor.
 *
*/
typedef struct 	DaqDeviceDescriptor DaqDeviceDescriptor;

/**
 * The DAQ device
 */
typedef long long DaqDeviceHandle;


/** \brief A structure representing the status of the data transfer.
 *
 * Status information includes the current count, total count, and current index value.
 */
struct TransferStatus
{
	/** The current scan count */
	unsigned long long currentScanCount;

	/** The total count */
	unsigned long long currentTotalCount;

	/** The current index value */
	long long currentIndex;

	/** Reserved for future use */
	char reserved[64];
};

/** \brief A structure representing the status of the data transfer.
 *
 */
typedef struct 	TransferStatus TransferStatus;


#define ERR_MSG_LEN				512

/** UL error codes */
typedef enum
{
	/** No error has occurred */
	ERR_NO_ERROR 					= 0,

	/** Unhandled internal exception */
	ERR_UNHANDLED_EXCEPTION 		= 1,

	/** Invalid device handle */
	ERR_BAD_DEV_HANDLE 				= 2,

	/** This function cannot be used with this device */
	ERR_BAD_DEV_TYPE 				= 3,

	/** Insufficient permission to access this device */
	ERR_USB_DEV_NO_PERMISSION		= 4,

	/** USB interface is already claimed */
	ERR_USB_INTERFACE_CLAIMED 		= 5,

	/** Device not found */
	ERR_DEV_NOT_FOUND 				= 6,

	/** Device not connected or connection lost */
	ERR_DEV_NOT_CONNECTED 			= 7,

	/** Device no longer responding */
	ERR_DEAD_DEV 					= 8,

	/** Buffer too small for operation */
	ERR_BAD_BUFFER_SIZE 			= 9,

	/** Invalid buffer */
	ERR_BAD_BUFFER 					= 10,

	/** Invalid memory type */
	ERR_BAD_MEM_TYPE 				= 11,

	/** Invalid memory region */
	ERR_BAD_MEM_REGION 				= 12,

	/** Invalid range */
	ERR_BAD_RANGE					= 13,

	/** Invalid analog input channel specified */
	ERR_BAD_AI_CHAN					= 14,

	/** Invalid input mode specified */
	ERR_BAD_INPUT_MODE				= 15,

	/** A background process is already in progress */
	ERR_ALREADY_ACTIVE				= 16,

	/** Invalid trigger type specified */
	ERR_BAD_TRIG_TYPE				= 17,

	/** FIFO overrun, data was not transferred from device fast enough */
	ERR_OVERRUN						= 18,

	/** FIFO underrun, data was not transferred to device fast enough */
	ERR_UNDERRUN					= 19,

	/** Operation timed out */
	ERR_TIMEDOUT					= 20,

	/** Invalid option specified */
	ERR_BAD_OPTION					= 21,

	/** Invalid sampling rate specified */
	ERR_BAD_RATE					= 22,

	/** Sample count cannot be greater than FIFO size for BURSTIO scans */
	ERR_BAD_BURSTIO_COUNT			= 23,

	/** Configuration not supported */
	ERR_CONFIG_NOT_SUPPORTED		= 24,

	/** Invalid configuration value */
	ERR_BAD_CONFIG_VAL				= 25,

	/** Invalid analog input channel type specified */
	ERR_BAD_AI_CHAN_TYPE			= 26,

	/** ADC overrun occurred */
	ERR_ADC_OVERRUN					= 27,

	/** Invalid thermocouple type specified */
	ERR_BAD_TC_TYPE					= 28,

	/** Invalid unit specified */
	ERR_BAD_UNIT					= 29,

	/** Invalid queue size */
	ERR_BAD_QUEUE_SIZE				= 30,

	/** Invalid config item specified */
	ERR_BAD_CONFIG_ITEM				= 31,

	/** Invalid info item specified */
	ERR_BAD_INFO_ITEM				= 32,

	/** Invalid flag specified */
	ERR_BAD_FLAG					= 33,

	/** Invalid sample count specified */
	ERR_BAD_SAMPLE_COUNT			= 34,

	/** Internal error */
	ERR_INTERNAL					= 35,

	/** Invalid coupling mode */
	ERR_BAD_COUPLING_MODE			= 36,

	/** Invalid sensor sensitivity */
	ERR_BAD_SENSOR_SENSITIVITY		= 37,

	/** Invalid IEPE mode */
	ERR_BAD_IEPE_MODE				= 38,

	/** Invalid channel queue specified */
	ERR_BAD_AI_CHAN_QUEUE			= 39,

	/** Invalid gain queue specified */
	ERR_BAD_AI_GAIN_QUEUE			= 40,

	/** Invalid mode queue specified */
	ERR_BAD_AI_MODE_QUEUE			= 41,

	/** FPGA file not found */
	ERR_FPGA_FILE_NOT_FOUND			= 42,

	/** Unable to read FPGA file */
	ERR_UNABLE_TO_READ_FPGA_FILE	= 43,

	/** FPGA not loaded */
	ERR_NO_FPGA						= 44,

	/** Invalid argument */
	ERR_BAD_ARG						= 45,

	/** Minimum slope value reached */
	ERR_MIN_SLOPE_VAL_REACHED		= 46,

	/** Maximum slope value reached */
	ERR_MAX_SLOPE_VAL_REACHED		= 47,

	/** Minimum offset value reached */
	ERR_MIN_OFFSET_VAL_REACHED		= 48,

	/** Maximum offset value reached */
	ERR_MAX_OFFSET_VAL_REACHED		= 49,

	/** Invalid port type specified */
	ERR_BAD_PORT_TYPE				= 50,

	/** Digital I/O is configured incorrectly */
	ERR_WRONG_DIG_CONFIG			= 51,

	/** Invalid bit number */
	ERR_BAD_BIT_NUM					= 52,

	/** Invalid port value specified */
	ERR_BAD_PORT_VAL				= 53,

	/** Invalid re-trigger count */
	ERR_BAD_RETRIG_COUNT			= 54,

	/** Invalid analog output channel specified */
	ERR_BAD_AO_CHAN					= 55,

	/** Invalid D/A output value specified */
	ERR_BAD_DA_VAL					= 56,

	/** Invalid timer specified */
	ERR_BAD_TMR						= 57,

	/** Invalid frequency specified */
	ERR_BAD_FREQUENCY				= 58,

	/** Invalid duty cycle specified */
	ERR_BAD_DUTY_CYCLE				= 59,

	/** Invalid initial delay specified */
	ERR_BAD_INITIAL_DELAY			= 60,

	/** Invalid counter specified */
	ERR_BAD_CTR						= 61,

	/** Invalid counter value specified */
	ERR_BAD_CTR_VAL					= 62,

	/** Invalid DAQ input channel type specified */
	ERR_BAD_DAQI_CHAN_TYPE			= 63,

	/** Invalid number of channels specified */
	ERR_BAD_NUM_CHANS				= 64,

	/** Invalid counter register specified */
	ERR_BAD_CTR_REG					= 65,

	/** Invalid counter measurement type specified */
	ERR_BAD_CTR_MEASURE_TYPE		= 66,

	/** Invalid counter measurement mode specified */
	ERR_BAD_CTR_MEASURE_MODE		= 67,

	/** Invalid debounce time specified */
	ERR_BAD_DEBOUNCE_TIME			= 68,

	/** Invalid debounce mode specified */
	ERR_BAD_DEBOUNCE_MODE			= 69,

	/** Invalid edge detection mode specified */
	ERR_BAD_EDGE_DETECTION			= 70,

	/** Invalid tick size specified */
	ERR_BAD_TICK_SIZE				= 71,

	/** Invalid DAQ output channel type specified */
	ERR_BAD_DAQO_CHAN_TYPE			= 72,

	/** No connection established */
	ERR_NO_CONNECTION_ESTABLISHED	= 73,

	/** Invalid event type specified */
	ERR_BAD_EVENT_TYPE				= 74,

	/** An event handler has already been enabled for this event type */
	ERR_EVENT_ALREADY_ENABLED		= 75,

	/** Invalid event parameter specified */
	ERR_BAD_EVENT_PARAMETER			= 76,

	/** Invalid callback function specified */
	ERR_BAD_CALLBACK_FUCNTION		= 77,

	/** Invalid memory address */
	ERR_BAD_MEM_ADDRESS				= 78,

	/** Memory access denied */
	ERR_MEM_ACCESS_DENIED			= 79,

	/** Device is not available at time of request */
	ERR_DEV_UNAVAILABLE				= 80,

	/** Re-trigger option is not supported for the specified trigger type */
	ERR_BAD_RETRIG_TRIG_TYPE		= 81

} UlError;

/** A/D channel input modes */
typedef enum
{
	/** Differential */
	AI_DIFFERENTIAL = 1,

	/** Single-ended */
	AI_SINGLE_ENDED = 2,

	/** Pseudo-differential */
	AI_PSEUDO_DIFFERENTIAL = 3
}AiInputMode;

/** A/D channel types */
typedef enum
{
	/** Voltage */
	AI_VOLTAGE 			= 1 << 0,

	/** Thermocouple */
	AI_TC 				= 1 << 1,

	/** Resistance Temperature Detector (RTD) */
	AI_RTD 				= 1 << 2,

	/** Thermistor */
	AI_THERMISTOR 		= 1 << 3,

	/** Semiconductor */
	AI_SEMICONDUCTOR 	= 1 << 4,

	/** Disabled */
	AI_DISABLED 		= 1 << 30
}AiChanType;

/** Thermocouple types */
typedef enum
{
	/** Type J */
	TC_J				= 1,

	/** Type K */
	TC_K				= 2,

	/** Type T */
	TC_T				= 3,

	/** Type E */
	TC_E				= 4,

	/** Type R */
	TC_R				= 5,

	/** Type S */
	TC_S				= 6,

	/** Type B */
	TC_B				= 7,

	/** Type N */
	TC_N				= 8
}TcType;

/** Range values */
typedef enum
{
	/** -60 to +60 Volts */
	BIP60VOLTS		= 1,

	/** -30 to +30 Volts */
	BIP30VOLTS		= 2,

	/** -15 to +15 Volts */
	BIP15VOLTS		= 3,

	/** -20 to +20 Volts */
	BIP20VOLTS      = 4,

	/** -10 to +10 Volts */
	BIP10VOLTS      = 5,

	/** -5 to +5 Volts */
	BIP5VOLTS       = 6,

	/** -4 to +4 Volts */
	BIP4VOLTS       = 7,

	/** -2.5 to +2.5 Volts */
	BIP2PT5VOLTS    = 8,

	/** -2.0 to +2.0 Volts */
	BIP2VOLTS       = 9,

	/** -1.25 to +1.25 Volts */
	BIP1PT25VOLTS   = 10,

	/** -1 to +1 Volts */
	BIP1VOLTS       = 11,

	/** -.625 to +.625 Volts */
	BIPPT625VOLTS   = 12,

	/** -.5 to +.5 Volts */
	BIPPT5VOLTS     = 13,

	/** -0.25 to +0.25 Volts */
	BIPPT25VOLTS    = 14,

	/** -0.125 to +0.125 Volts */
	BIPPT125VOLTS   = 15,

	/** -0.2 to +0.2 Volts */
	BIPPT2VOLTS     = 16,

	/** -.1 to +.1 Volts */
	BIPPT1VOLTS     = 17,

	/** -0.078 to +0.078 Volts */
	BIPPT078VOLTS   = 18,

	/** -.05 to +.05 Volts */
	BIPPT05VOLTS    = 19,

	/** -.01 to +.01 Volts */
	BIPPT01VOLTS    = 20,

	/** -.005 to +.005 Volts */
	BIPPT005VOLTS   = 21,

	/** 0 to +60 Volts */
	UNI60VOLTS		= 1001,

	/** 0 to +30 Volts */
	UNI30VOLTS		= 1002,

	/** 0 to +15 Volts */
	UNI15VOLTS		= 1003,

	/** 0 to +20 Volts */
	UNI20VOLTS      = 1004,

	/** 0 to +10 Volts */
	UNI10VOLTS      = 1005,

	/** 0 to +5 Volts */
	UNI5VOLTS       = 1006,

	/** 0 to +4 Volts */
	UNI4VOLTS       = 1007,

	/** 0 to +2.5 Volts */
	UNI2PT5VOLTS    = 1008,

	/** 0 to +2.0 Volts */
	UNI2VOLTS       = 1009,

	/** 0 to +1.25 Volts */
	UNI1PT25VOLTS   = 1010,

	/** 0 to +1 Volts */
	UNI1VOLTS       = 1011,

	/** 0 to +.625 Volts */
	UNIPT625VOLTS   = 1012,

	/** 0 to +.5 Volts */
	UNIPT5VOLTS     = 1013,

	/** 0 to +0.25 Volts */
	UNIPT25VOLTS    = 1014,

	/** 0 to +0.125 Volts */
	UNIPT125VOLTS   = 1015,

	/** 0 to +0.2 Volts */
	UNIPT2VOLTS     = 1016,

	/** 0 to +.1 Volts */
	UNIPT1VOLTS     = 1017,

	/** 0 to +0.078 Volts */
	UNIPT078VOLTS   = 1018,

	/** 0 to +.05 Volts */
	UNIPT05VOLTS    = 1019,

	/** 0 to +.01 Volts */
	UNIPT01VOLTS    = 1020,

	/** 0 to +.005 Volts */
	UNIPT005VOLTS   = 1021
}Range;

/** Temperature units */
typedef enum
{
	/** Celcius */
	TU_CELSIUS  	= 1,

	/** Fahrenheit */
	TU_FAHRENHEIT 	= 2,

	/** Kelvin */
	TU_KELVIN 		= 3
}TempUnit;

/** Temperature units */
typedef enum
{
	/** Celcius */
	TS_CELSIUS  	= TU_CELSIUS,

	/** Fahrenheit */
	TS_FAHRENHEIT 	= TU_FAHRENHEIT,

	/** Kelvin */
	TS_KELVIN 		= TU_KELVIN,

	/** Volts */
	TS_VOLTS 		= 4,

	/** No scale (Raw) */
	TS_NOSCALE 		= 5
}TempScale;

/** Auto zero modes */
typedef enum
{
	/** Disabled */
	AZM_NONE = 1,

	/** Perform auto zero on every thermocouple reading. */
	AZM_EVERY_SAMPLE = 2,

	/** Perform auto zero before every scan. */
	AZM_ONCE = 3
}AutoZeroMode;

/** ADC timing modes */
typedef enum
{
	/** The timing mode is set automatically. */
	ADC_TM_AUTO 		= 1,

	/** Acquires data in samples per 1000 seconds per channel. */
	ADC_TM_HIGH_RES 	= 2,

	/** High speed timing mode. */
	ADC_TM_HIGH_SPEED 	= 3
}AdcTimingMode;

/** IEPE modes */
typedef enum
{
	/** IEPE excitation current is disabled. */
	IEPE_DISABLED = 1,

	/** IEPE excitation current is enabled. */
	IEPE_ENABLED = 2
}IepeMode;

/** Coupling modes */
typedef enum
{
	/** DC coupling */
	CM_DC = 1,

	/** AC coupling */
	CM_AC = 2
}CouplingMode;

/** Queue types supported by the AI subsystem */
typedef enum
{
	/** The AI subsystem supports a channel queue. */
	CHAN_QUEUE = 1 << 0,

	/** The AI subsystem supports a gain queue. */
	GAIN_QUEUE = 1 << 1,

	/** The AI subsystem supports a mode queue. */
	MODE_QUEUE = 1 << 2
}AiQueueType;

/** Channel queue limitations */
typedef enum
{
	/** A particular channel number cannot appear more than once in the queue. */
	UNIQUE_CHAN = 1 << 0,

	/** Channel numbers must be listed in ascending order within the queue. */
	ASCENDING_CHAN = 1 << 1,

	/** Channel numbers must be listed in contiguous order within the queue. */
	CONSECUTIVE_CHAN = 1 << 2
} AiChanQueueLimitation;

/** Digital port type */
typedef enum
{
	/** AuxPort */
	AUXPORT = 1,

	/** AuxPort0 */
	AUXPORT0 = 1,

	/** AuxPort1 */
	AUXPORT1 = 2,

	/** AuxPort2 */
	AUXPORT2 = 3,

	/** FirstPortA */
	FIRSTPORTA = 10,

	/** FirstPortB */
	FIRSTPORTB = 11,

	/** FirstPortC */
	FIRSTPORTC = 12,

	/** FirstPortC Low */
	FIRSTPORTCL = 12,

	/** FirstPortC High */
	FIRSTPORTCH = 13,

	/** SecondPortA */
	SECONDPORTA = 14,

	/** SecondPortB */
	SECONDPORTB = 15,

	/** SecondPortC Low */
	SECONDPORTCL = 16,

	/** SecondPortC High */
	SECONDPORTCH = 17,

	/** ThirdPortA */
	THIRDPORTA = 18,

	/** ThirdPortB */
	THIRDPORTB = 19,

	/** ThirdPortC Low */
	THIRDPORTCL = 20,

	/** ThirdPortC High */
	THIRDPORTCH = 21,

	/** FourthPortA */
	FOURTHPORTA = 22,

	/** FourthPortB */
	FOURTHPORTB = 23,

	/** FourthPortC Low */
	FOURTHPORTCL = 24,

	/** FourthPortC High */
	FOURTHPORTCH = 25,

	/** FifthPortA */
	FIFTHPORTA = 26,

	/** FifthPortB */
	FIFTHPORTB = 27,

	/** FifthPortC Low */
	FIFTHPORTCL = 28,

	/** FifthPortC High */
	FIFTHPORTCH = 29,

	/** SixthPortA */
	SIXTHPORTA = 30,

	/** SixthPortB */
	SIXTHPORTB = 31,

	/** SixthPortC Low */
	SIXTHPORTCL = 32,

	/** SixthPortC High */
	SIXTHPORTCH = 33,

	/** SeventhPortA */
	SEVENTHPORTA = 34,

	/** SeventhPortB */
	SEVENTHPORTB = 35,

	/** SeventhPortC Low */
	SEVENTHPORTCL = 36,

	/** SeventhPortC High */
	SEVENTHPORTCH = 37,

	/** EighthPortA */
	EIGHTHPORTA = 38,

	/** EighthPortB */
	EIGHTHPORTB = 39,

	/** EighthPortC Low */
	EIGHTHPORTCL = 40,

	/** EighthPortC High */
	EIGHTHPORTCH = 41
}DigitalPortType;

/** Digital port I/O capabilities */
typedef enum
{
	/** Fixed input port */
	DPIOT_IN = 1,

	/** Fixed output port */
	DPIOT_OUT = 2,

	/** Bidirectional (input or output) port */
	DPIOT_IO = 3,

	/** Bitwise configurable */
	DPIOT_BITIO = 4,

	/** Bidirectional (input or output) port; configuration is not required. */
	DPIOT_NONCONFIG = 5
} DigitalPortIoType;

/** Digital port direction */
typedef enum
{
	/** Input */
	DD_INPUT = 1,

	/** Output */
	DD_OUTPUT = 2
}DigitalDirection;

/** Types of timer channels */
typedef enum
{
	/** Programmable frequency timer */
	TMR_STANDARD = 1,

	/** Programmable frequency timer, plus other attributes such as pulse width. */
	TMR_ADVANCED = 2
}TimerType;

/** Timer idle state */
typedef enum
{
	/** Idle low */
	TMRIS_LOW = 1,

	/** Idle high */
	TMRIS_HIGH = 2
}TmrIdleState;

/** Timer status */
typedef enum
{
	/** Timer is running */
	TMRS_IDLE = 0,

	/** Timer is idle */
	TMRS_RUNNING = 1
}TmrStatus;

/** Trigger types based on the trigger source */
typedef enum
{
	/** No trigger */
	TRIG_NONE = 0,	
	
	/** Scanning begins when the external digital trigger transitions
	 * from 0V to 5V (logic LOW to HIGH). */
	TRIG_POS_EDGE =  1 << 0,

	/** Scanning begins when the external digital trigger transitions
	 * from 5V to 0V (logic HIGH to LOW). */
	TRIG_NEG_EDGE = 1 << 1,

	/**  Scanning begins when the external digital trigger is 5V (logic HIGH or '1'). */
	TRIG_HIGH = 1 << 2,

	/**  Scanning begins when the external digital trigger is 0V (logic LOW or '0'). */
	TRIG_LOW = 1 << 3,

	/**  Scanning is enabled as long as the external digital trigger
	 * input is 5V (logic HIGH or '1'). */
	GATE_HIGH = 1 << 4,

	/**  Scanning is enabled as long as the external digital trigger
	 * input is 0V (logic LOW or '0'). */
	GATE_LOW = 1 << 5,

	/** Scanning begins when the external analog trigger input transitions
	 * from below lowThreshold to above highThreshold. */
	TRIG_RISING = 1 << 6,

	/** Scanning begins when the external analog trigger input transitions
	 * from above highThreshold to below lowThreshold. */
	TRIG_FALLING = 1 << 7,

	/**  Scanning begins when the external analog trigger input transitions
	 * from below highThreshold to above. */
	TRIG_ABOVE = 1 << 8,

	/**  Scanning begins when the external analog trigger input transitions
	 * from above lowThreshold to below. */
	TRIG_BELOW = 1 << 9,

	/** Scanning is enabled as long as the external analog trigger input is
	 * more positive than highThreshold. */
	GATE_ABOVE = 1 << 10,

	/**  Scanning is enabled as long as the external analog trigger input is
	 * more negative than lowThreshold. */
	GATE_BELOW = 1 << 11,

	/**  Scanning is enabled as long as the external analog trigger is inside
	 * the region defined by lowThreshold and highThreshold. */
	GATE_IN_WINDOW = 1 << 12,

	/**  Scanning is enabled as long as the external analog trigger is outside
	 * the region defined by lowThreshold and highThreshold. */
	GATE_OUT_WINDOW = 1 << 13,

	/** Scanning begins when the digital port value AND bitwise mask are equal
	 * to the pattern value AND bitwise mask. */
	TRIG_PATTERN_EQ = 1 << 14,

	/** Scanning begins when the digital port value AND bitwise mask are not equal
	 * to the pattern value AND bitwise mask. */
	TRIG_PATTERN_NE = 1 << 15,

	/** Scanning begins when the digital port value AND bitwise mask are greater
	 * than the pattern value AND bitwise mask. */
	TRIG_PATTERN_ABOVE = 1 << 16,

	/** Scanning begins when the digital port value AND bitwise mask are less than
	 * the pattern value AND bitwise mask. */
	TRIG_PATTERN_BELOW = 1 << 17
}TriggerType;

/** \brief A structure representing the queue element
 *
 * Information includes the number, mode, and range of the A/D channel.
 */
struct AiQueueElement
{
	/** The channel number to add to the channel-gain queue. */
	int channel;

	/** The channel input mode configured for the current instance of AiQueueElement(). */
	AiInputMode inputMode;

	/** The channel range configured for the current instance of AiQueueElement(). */
	Range range;

	/** Reserved for future use */
	char reserved[64];
};

/** \brief A structure representing the queue element
 *
 */
typedef struct 	AiQueueElement AiQueueElement;

/** Scan status */
typedef enum
{
	/** Scan is idle */
	SS_IDLE = 0,

	/** Scan is running */
	SS_RUNNING = 1
}ScanStatus;

#define NOSCALEDATA 		1 << 0
#define NOCALIBRATEDATA 	1 << 1
#define NOCLEAR				1 << 3


/** Scan options */
typedef enum
{
	/** Transfers A/D data based on the board type and sampling speed. */
	SO_DEFAULTIO	= 0,

	/** Transfers one packet of data at a time. */
	SO_SINGLEIO		= 1 << 0,

	/** Transfers A/D data in blocks. */
	SO_BLOCKIO		= 1 << 1,

	/** Transfers A/D data from the FIFO after the scan completes.
	 * Allows maximum rates for finite scans up to the full capacity of the FIFO. Not recommended for slow acquisition rates. */
	SO_BURSTIO		= 1 << 2,

	/** Scans data in an endless loop. The only way to stop the operation is with ulAInScanStop(). */
	SO_CONTINUOUS 	= 1 << 3,

	/** Data conversions are controlled by an external clock signal. */
	SO_EXTCLOCK		= 1 << 4,

	/** Sampling begins when a trigger condition is met. */
	SO_EXTTRIGGER 	= 1 << 5,

	/** Re-arms the trigger after a trigger event is performed. */
	SO_RETRIGGER 	= 1 << 6,

	/** Enables burst mode sampling, minimizing the channel skew. */
	SO_BURSTMODE 	= 1 << 7,

	/** Enables or disables the internal pacer output on a DAQ device. */
	SO_PACEROUT		= 1 << 8
}ScanOption;

/** Scan options for scaling and calibrating A/D scan data */
typedef enum
{
	/** Transfers A/D data based on the the board type and sampling speed. */
	AINSCAN_FF_DEFAULT 				= 0,

	/** No scaling is applied to raw data. */
	AINSCAN_FF_NOSCALEDATA 			= NOSCALEDATA, 		

	/** Turns off real-time software calibration for devices that are software calibrated. */
	AINSCAN_FF_NOCALIBRATEDATA 		= NOCALIBRATEDATA 	
}AInScanFlag;

/** Scan options for scaling and calibrating A/D data */
typedef enum
{
	/** Transfers A/D data based on the the board type and sampling speed. */
	AIN_FF_DEFAULT = 0,

	/** No scaling is applied to raw data. */
	AIN_FF_NOSCALEDATA 			= NOSCALEDATA, 		

	/** Turns off real-time software calibration for devices that are software calibrated. */
	AIN_FF_NOCALIBRATEDATA 		= NOCALIBRATEDATA 	
}AInFlag;

/** Scan options for scaling and calibrating D/A scan data */
typedef enum
{
	/** Transfers D/A data based on the the board type and sampling speed. */
	AOUTSCAN_FF_DEFAULT					= 0,

	/** No scaling is applied to raw data. */
	AOUTSCAN_FF_NOSCALEDATA 			= NOSCALEDATA, 		

	/** Turns off real-time software calibration for devices that are software calibrated. */
	AOUTSCAN_FF_NOCALIBRATEDATA 		= NOCALIBRATEDATA 	
}AOutScanFlag;

/** Scan options for scaling and calibrating D/A data */
typedef enum
{
	/** Transfers D/A data based on the the board type and sampling speed. */
	AOUT_FF_DEFAULT	= 0,

	/** No scaling is applied to raw data. */
	AOUT_FF_NOSCALEDATA 			= NOSCALEDATA, 		

	/** Turns off real-time software calibration for devices that are software calibrated. */
	AOUT_FF_NOCALIBRATEDATA 		= NOCALIBRATEDATA 	
}AOutFlag;

/** Scan options for counter input functions. */
typedef enum
{
	/** Transfers counter data based on the the board type and sampling speed. */
	CINSCAN_FF_DEFAULT 			= 0,

	/** 16-bit counter channel */
	CINSCAN_FF_CTR16_BIT 		= 1 << 0,

	/** 32-bit counter channel */
	CINSCAN_FF_CTR32_BIT 		= 1 << 1,

	/** 64-bit counter channel */
	CINSCAN_FF_CTR64_BIT 		= 1 << 2,

	/** Disables the clearing of counters when the scan starts. */
	CINSCAN_FF_NOCLEAR			= NOCLEAR   
}CInScanFlag;

/** Scan options for digital input functions. */
typedef enum
{
	/** Transfers digital data based on the the board type and sampling speed. */
	DINSCAN_FF_DEFAULT 			= 0,
}DInScanFlag;

/** Scan options for digital output functions */
typedef enum
{
	/** Transfers counter data based on the the board type and sampling speed. */
	DOUTSCAN_FF_DEFAULT 			= 0,
}DOutScanFlag;

/** Scan options for synchronous input functions */
typedef enum
{
	/** Transfers synchronous A/D data based on the the board type and sampling speed. */
	DAQINSCAN_FF_DEFAULT			= 0,

	/** No scaling is applied to raw data. */
	DAQINSCAN_FF_NOSCALEDATA 		= NOSCALEDATA, 		

	/** Turns off real-time software calibration for devices that are software calibrated. */
	DAQINSCAN_FF_NOCALIBRATEDATA 	= NOCALIBRATEDATA, 	

	/** Counters are not cleared (set to 0) when a scan starts **/
	DAQINSCAN_FF_NOCLEAR			= NOCLEAR			
}DaqInScanFlag;

/** Scan options for synchronous output functions */
typedef enum
{
	/** Transfers synchronous D/A data based on the the board type and sampling speed. */
	DAQOUTSCAN_FF_DEFAULT			= 0,

	/** No scaling is applied to raw data. */
	DAQOUTSCAN_FF_NOSCALEDATA 		= NOSCALEDATA, 		

	/** Turns off real-time software calibration for devices that are software calibrated. */
	DAQOUTSCAN_FF_NOCALIBRATEDATA 	= NOCALIBRATEDATA 	
}DaqOutScanFlag;

/** Counter measurement types */
typedef enum
{
	/** Counter measurement */
	CMT_COUNT =			1 << 0,

	/** Period measurement */
	CMT_PERIOD = 		1 << 1,

	/** Pulsewidth measurement */
	CMT_PULSE_WIDTH = 	1 << 2,

	/** Timing measurement */
	CMT_TIMING = 		1 << 3,

	/** Encoder measurement */
	CMT_ENCODER =		1 << 4
}CounterMeasurementType;

/** Counter modes */
typedef enum
{
	/** Counter mode */
	CMM_DEFAULT =						0,

	/** The counter is cleared after every read. */
	CMM_CLEAR_ON_READ =					1 << 0,

	/** The counter counts down. */
	CMM_COUNT_DOWN =					1 << 1,

	/** The gate input controls the direction of the counter. By default, the counter increments when
	 * the gate pin is high, and decrements when the gate pin is low. */
	CMM_GATE_CONTROLS_DIR =				1 << 2,

	/** The gate input clears the counter. By default, the counter is cleared when the gate input is high. */
	CMM_GATE_CLEARS_CTR =				1 << 3,

	/** The counter starts counting when the gate input goes active. By default, active is on the rising edge.
	 * The gate is re-armed when the counter is loaded and when ulCConfigScan() is called. */
	CMM_GATE_TRIG_SRC =					1 << 4,

	/** Enables the counter output. By default, the counter output goes high when the counter reaches the
	 * value of output register 0, and low when the counter reaches the value of output register 1.
	 * Use ulCLoad() to set or read the value of the output registers. */
	CMM_OUTPUT_ON =						1 << 5,

	/** Sets the initial state of the counter output pin high. */
	CMM_OUTPUT_INITIAL_STATE_HIGH =		1 << 6,

	/** Enables Non-recycle counting mode, in which the counter stops counting whenever a count overflow or underflow takes place.
	 * Counting restarts when a clear or a load operation is performed on the counter, or the count direction changes. */
	CMM_NO_RECYCLE = 					1 << 7,

	/** Enables Range Limit counting mode, in which an upper and lower limit is set.<br>
	 * Use ulCLoad() to set the upper and lower limits. Set the upper limit by loading the max limit register, and the lower limit
	 * by loading the min limit register. Note that on some devices the lower limit is programmable, but on other devices the lower limit is always 0.<br>
	 * When counting up, the counter rolls over to min limit when the max limit is reached. When counting down, the counter rolls
	 * over to max limit when the min limit is reached. When counting up with NO_RECYCLE enabled,
	 * the counter freezes whenever the count reaches the value that was loaded into the max limit register.<br>
	 * When counting down with NO_RECYCLE enabled, the counter freezes whenever the count reaches the value that
	 * was loaded into the min limit register. Counting resumes if the counter is reset or the direction changes. */
	CMM_RANGE_LIMIT_ON =				1 << 8,

	/** The counter is enabled when the mapped channel or the gate pin that is used to gate the counter is high.<br>
	 * When the mapped channel/gate pin is low, the counter is disabled but holds the count value. By default,
	 * the counter gating option is set to "off." */
	CMM_GATING_ON = 					1 << 9,

	/** Inverts the polarity of the gate input.*/
	CMM_INVERT_GATE =					1 << 10,

	/** The measurement is latched each time 1 complete period is observed. */
	CMM_PERIOD_X1 =						0,

	/** The measurement is latched each time 10 complete periods are observed. */
	CMM_PERIOD_X10 =					1 << 11,

	/** The measurement is latched each time 100 complete periods are observed. */
	CMM_PERIOD_X100 =					1 << 12,

	/** The measurement is latched each time 1000 complete periods are observed. */
	CMM_PERIOD_X1000 =					1 << 13,

	/** The counter is enabled when the mapped channel or the gate pin that is used to gate the counter is high.<br>
	 * When the mapped channel/gate pin is low, the counter is disabled but holds the count value. By default,
	 * the counter gating option is set to "off." */
	CMM_PERIOD_GATING_ON =				1 << 14,

	/** Inverts the polarity of the gate input.*/
	CMM_PERIOD_INVERT_GATE =			1 << 15,

	/** Pulsewidth mode */
	CMM_PULSE_WIDTH_DEFAULT =			0,

	/** The counter is enabled when the mapped channel or the gate pin that is used to gate the counter is high. <br>
	 * When the mapped channel/gate pin is low, the counter is disabled but holds the count value. By default,
	 * the counter gating option is set to "off." */
	CMM_PULSE_WIDTH_GATING_ON =			1 << 16,

	/** Inverts the polarity of the gate input.*/
	CMM_PULSE_WIDTH_INVERT_GATE =		1 << 17,

	/** Timing mode */
	CMM_TIMING_DEFAULT	=				0,

	/** Inverts the polarity of the gate input.*/
	CMM_TIMING_MODE_INVERT_GATE =		1 << 18,

	/** Sets the encoder measurement mode to X1. */
	CMM_ENCODER_X1 =					0,

	/** Sets the encoder measurement mode to X2. */
	CMM_ENCODER_X2 =					1 << 19,

	/** Sets the encoder measurement mode to X4. */
	CMM_ENCODER_X4	=					1 << 20,

	/** Selects the encoder Z mapped signal to latch the counter outputs; this allows the user to know the exact counter value
	 * when an edge is present on another counter. */
	CMM_ENCODER_LATCH_ON_Z =			1 << 21,

	/** The counter is cleared when the index (Z input) goes active. By default, the "clear on Z" option is off, and the counter is not cleared. */
	CMM_ENCODER_CLEAR_ON_Z =			1 << 22,

	/** The counter is disabled whenever a count overflow or underflow takes place, and re-enabled when a clear or
	 * load operation is performed on the counter. */
	CMM_ENCODER_NO_RECYCLE = 			1 << 23,

	/** Enables Range Limit counting mode, in which an upper and lower limit is set.<br>
	 * Use ulCLoad() to set the upper and lower limits. Set the upper limit by loading the max limit register, and the lower limit
	 * by loading the min limit register. Note that on some devices the lower limit is programmable, but on other devices the lower limit is always 0.<br>
	 * When counting up, the counter rolls over to min limit when the max limit is reached. When counting down, the counter rolls
	 * over to max limit when the min limit is reached. When counting up with NO_RECYCLE enabled,
	 * the counter freezes whenever the count reaches the value that was loaded into the max limit register.<br>
	 * When counting down with NO_RECYCLE enabled, the counter freezes whenever the count reaches the value that
	 * was loaded into the min limit register. Counting resumes if the counter is reset or the direction changes. */
	CMM_ENCODER_RANGE_LIMIT_ON	=		1 << 24,

	/** Sets the encoder Z signal as the active edge. */
	CMM_ENCODER_Z_ACTIVE_EDGE	=		1 << 25
}CounterMeasurementMode;

/** Counter debounce times */
typedef enum
{
	/** Sets the counter channel's comparator output to 0 ns. */
	CDT_DEBOUNCE_0ns =		0,

	/** Sets the counter channel's comparator output to 500 ns. */
	CDT_DEBOUNCE_500ns =	1,

	/** Sets the counter channel's comparator output to 1500 ns. */
	CDT_DEBOUNCE_1500ns =   2,

	/** Sets the counter channel's comparator output to 3500 ns. */
	CDT_DEBOUNCE_3500ns =   3,

	/** Sets the counter channel'ss comparator output to 7500 ns. */
	CDT_DEBOUNCE_7500ns =   4,

	/** Sets the counter channel's comparator output to 15500 ns. */
	CDT_DEBOUNCE_15500ns =  5,

	/** Sets the counter channel's comparator output to 31500 ns. */
	CDT_DEBOUNCE_31500ns =  6,

	/** Sets the counter channel's comparator output to 63500 ns. */
	CDT_DEBOUNCE_63500ns =  7,

	/** Sets the counter channel's comparator output to 127500 ns. */
	CDT_DEBOUNCE_127500ns = 8,

	/** Sets the counter channel's comparator output to 100 us. */
	CDT_DEBOUNCE_100us =    9,

	/** Sets the counter channel's comparator output to 300 us. */
	CDT_DEBOUNCE_300us =    10,

	/** Sets the counter channel's comparator output to 700 us. */
	CDT_DEBOUNCE_700us =    11,

	/** Sets the counter channel's comparator output to 1500 us. */
	CDT_DEBOUNCE_1500us =   12,

	/** Sets the counter channel'ss comparator output to 3100 us. */
	CDT_DEBOUNCE_3100us =   13,

	/** Sets the counter channel's comparator output to 6300 us. */
	CDT_DEBOUNCE_6300us =   14,

	/** Sets the counter channel'ss comparator output to 12700 us. */
	CDT_DEBOUNCE_12700us =  15,

	/** Sets the counter channel's comparator output to 25500 us. */
	CDT_DEBOUNCE_25500us =  16
}CounterDebounceTime;

/** Counter debounce modes */
typedef enum
{
	/** Disables the debounce feature. */
	CDM_NONE					= 0,

	/** Rejects glitches, and only passes state transitions after a specified period of stability (the debounce time). */
	CDM_TRIGGER_AFTER_STABLE 	= 1,

	/** Use when the input signal has groups of glitches, and each group is to be counted as one */
	CDM_TRIGGER_BEFORE_STABLE 	= 2
}CounterDebounceMode;

/** Counter edge detection */
typedef enum
{
	/** Rising edge */
	CED_RISING_EDGE 			= 1,

	/** Falling edge */
	CED_FALLING_EDGE 			= 2
}CounterEdgeDetection;

/** Counter tick sizes */
typedef enum
{
	/** CTS_TICK_20PT83ns */
	CTS_TICK_20PT83ns			= 1,

	/** CTS_TICK_208PT3ns */
	CTS_TICK_208PT3ns			= 2,

	/** CTS_TICK_208PT3ns */
	CTS_TICK_2083PT3ns	 		= 3,

	/** CTS_TICK_20833PT3ns */
	CTS_TICK_20833PT3ns 		= 4,

	/** CTS_TICK_20ns */
	CTS_TICK_20ns 				= 11,

	/** CTS_TICK_200ns */
	CTS_TICK_200ns 				= 12,

	/** CTS_TICK_2000ns */
	CTS_TICK_2000ns 			= 13,

	/** CTS_TICK_20000ns */
	CTS_TICK_20000ns 			= 14
}CounterTickSize;


/** Counter scan options */
typedef enum
{
	/** No scan option applied */
	CF_DEFAULT = 0
}
CConfigScanFlag;

/** Counter register types */
typedef enum
{
	/** Counter register */
	CRT_COUNT 		= 1 << 0,

	/** Load register */
	CRT_LOAD 		= 1 << 1,

	/** Max Limit register */
	CRT_MIN_LIMIT	= 1 << 2,

	/** Min Limit register */
	CRT_MAX_LIMIT	= 1 << 3,

	/** Value 0*/
	CRT_OUTPUT_VAL0	= 1 << 4,

	/** Value 1*/
	CRT_OUTPUT_VAL1	= 1 << 5
}CounterRegisterType;

/** Channel types for synchronous operations */
typedef enum
{
	/** Analog input channel, differential mode */
	DAQI_ANALOG_DIFF 	= 1 << 0,

	/** Analog input channel, single-ended mode */
	DAQI_ANALOG_SE 		= 1 << 1,

	/** Digital channel */
	DAQI_DIGITAL 		= 1 << 2,

	/** 16-bit counter channel */
	DAQI_CTR16			= 1 << 3,

	/** 32-bit counter channel */
	DAQI_CTR32			= 1 << 4,

	/** 48-bit counter channel */
	DAQI_CTR48			= 1 << 5
	/** DAQI_CTR64 */
}DaqInChanType;

/** \brief A structure representing the input channel descriptor.
 *
*/
struct DaqInChanDescriptor
{
	/** The input channel */
	int channel;

	/** The channel type configured for the current instance of DaqInChanDescriptor. */
	DaqInChanType type;

	/** The channel range configured for the current instance of DaqInChanDescriptor. */
	Range range;
	/** Reserved for future use */
	char reserved[64];
};

/** \brief A structure representing the input channel descriptor */
typedef struct 	DaqInChanDescriptor DaqInChanDescriptor;

/** The output channel type */
typedef enum
{
	/** Analog output */
	DAQO_ANALOG			= 1 << 0,

	/** Digigtal output */
	DAQO_DIGITAL 		= 1 << 1
}DaqOutChanType;


/** \brief A structure representing the output channel descriptor.
 *
*/
struct DaqOutChanDescriptor
{
	/** The output channel */
	int channel;

	/** The channel type configured for the current instance of DaqOutChanDescriptor. */
	DaqOutChanType type;

	/** The channel range configured for the current instance of DaqOutChanDescriptor. */
	Range range;

	/** Reserved for future use */
	char reserved[64];
};

/** \brief A structure representing the output channel descriptor.
 *
*/
typedef struct 	DaqOutChanDescriptor DaqOutChanDescriptor;

/** Pulse out options */
typedef enum
{
	/** No PulseOut options are applied. */
	PO_DEFAULT = 0,

	/** Output pulses are generated when a trigger condition is met.
	* Set the trigger condition with ulTmrSetTrigger(). */
	PO_EXTTRIGGER = 1 << 5,

	/** Output pulses are automatically retriggered. **/
	PO_RETRIGGER = 1 << 6
} PulseOutOption;

/** Conditions that trigger an event */
typedef enum
{
	/** No trigger */
	DE_NONE 						= 0, 

	/** Generates an event when the number of samples acquired during an input scan increases by eventParameter samples or more. */
	DE_ON_DATA_AVAILABLE =			1 << 0,

	/** Generates an event when an input scan error occurs. */
	DE_ON_INPUT_SCAN_ERROR =		1 << 1,

	/**  Generates an event upon completion or error of an input scan operation such as ulAInScan(). */
	DE_ON_END_OF_INPUT_SCAN =		1 << 2,

	/** Generates an event when an output scan error occurs. */
	DE_ON_OUTPUT_SCAN_ERROR =		1 << 3,

	/**  Generates an event upon completion or error of an output scan operation such as ulAOutScan(). */
	DE_ON_END_OF_OUTPUT_SCAN =		1 << 4

}DaqEventType;

/** Reserved areas of memory */
typedef enum
{
	/** Calibration region */
	MR_CAL =		1 << 0,

	/** User region */
	MR_USER = 		1 << 1,

	/** Settings region */
	MR_SETTINGS = 	1 << 2
}MemRegion;

/** Types of memory access */
typedef enum
{
	/** Read and write memory */
	MA_READ =		1 << 0,

	/** Write memory */
	MA_WRITE = 		1 << 1
}MemAccessType;

/** The callback function called in response to an event condition. */
typedef void (*DaqEventCallback)(DaqDeviceHandle, DaqEventType, unsigned long long, void*);

/** Wait types  */
typedef enum
{
	/** Data is transferred when the operation completes */
	WAIT_UNTIL_DONE = 1 << 0
}WaitType;


/** UL info, configuration */


typedef enum
{
	UL_INFO_VER_STR = 2000
}UlInfoItemStr;


typedef enum
{	
	UL_CFG_USB_XFER_PRIORITY = 1
}UlConfigItem;


/** Returns device subsystem support */
typedef enum
{
	/** The DAQ device has an analog input subsystem. */
	DEV_INFO_HAS_AI_DEV = 1,

	/** The DAQ device has an analog output subsystem. */
	DEV_INFO_HAS_AO_DEV = 2,

	/** The DAQ device has a Digital I/O subsystem. */
	DEV_INFO_HAS_DIO_DEV = 3,

	/** The DAQ device has a counter input subsystem. */
	DEV_INFO_HAS_CTR_DEV = 4,

	/** The DAQ device has a timer output subsystem. */
	DEV_INFO_HAS_TMR_DEV = 5,

	/** The DAQ device has a DAQ input subsystem. */
	DEV_INFO_HAS_DAQI_DEV = 6,

	/** The DAQ device has an DAQ output subsystem. */
	DEV_INFO_HAS_DAQO_DEV = 7,

	/** Event types supported by the DAQ device */
	DEV_INFO_DAQ_EVENT_TYPES = 8,

	/** Memory regions supported by the DAQ device */
	DEV_INFO_MEM_REGIONS = 9
}DevInfoItem;

/** Returns the configuration version */
typedef enum
{
	DEV_CFG_VER_STR = 2000
}DevConfigItemStr;

/** Returns the firmware version */
typedef enum
{
	/** Firmware version installed on the current device. */
	DEV_VER_FW_MAIN = 0,

	/** FPGA version installed on the current device. */
	DEV_VER_FPGA = 1,

	/** Radio firmware version installed on the current device. */
	DEV_VER_RADIO = 2
}DevVersionType;

/** Use with ulAIGetInfo() to obtain information about the analog input subsystem. */
typedef enum
{
	/** The A/D resolution in number of bits. */
	AI_INFO_RESOLUTION = 1,

	/** The number of A/D channels on the specified device. */
	AI_INFO_NUM_CHANS = 2,

	/** The number of A/D channels for the specified channel mode. */
	AI_INFO_NUM_CHANS_BY_MODE = 3,

	/** The number of A/D channels for the specified channel type. */
	AI_INFO_NUM_CHANS_BY_TYPE = 4,

	/** A bitmask of supported #AiChanType values. */
	AI_INFO_CHAN_TYPES = 5,

	/** A bitmask of supported #ScanOption values. */
	AI_INFO_SCAN_OPTIONS = 6,

	/** Paced operations are supported. */
	AI_INFO_HAS_PACER = 7,

	/** A number of supported #Range values for differential mode operations. */
	AI_INFO_NUM_DIFF_RANGES = 8,

	/** A number of supported #Range values for single-ended mode operations. */
	AI_INFO_NUM_SE_RANGES = 9,

	/** The #Range for the specified differential range index. */
	AI_INFO_DIFF_RANGE = 10,

	/** The #Range for the specified single-ended range index. */
	AI_INFO_SE_RANGE = 11,

	/** A bitmask of supported #TriggerType values. */
	AI_INFO_TRIG_TYPES = 12,

	/** The maximum length of the queue for the specified channel mode. */
	AI_INFO_MAX_QUEUE_LENGTH_BY_MODE = 13,

	/** A bitmask of supported #AiQueueType values supported for the specified device. */
	AI_INFO_QUEUE_TYPES = 14,

	/** A bitmask of supported #AiChanQueueLimitation values, if any, that applies to the queue for the specified device. */
	AI_INFO_QUEUE_LIMITS = 15,

	/** FIFO size in bytes. */
	AI_INFO_FIFO_SIZE = 16

}AiInfoItem;

/** Use with ulAIGetInfoDbl() to obtain information about the analog input subsystem. */
typedef enum
{
	/** The minimum scan rate in samples per second of the specified device. */
	AI_INFO_MIN_SCAN_RATE = 1000,

	/** The maximum scan rate in samples per second of the specified device. */
	AI_INFO_MAX_SCAN_RATE = 1001,

	/** The maximum throughput in samples per second of the specified device. */
	AI_INFO_MAX_THROUGHPUT = 1002,

	/** The maximum scan rate in samples per second when using ::SO_BURSTIO mode. */
	AI_INFO_MAX_BURST_RATE = 1003,

	/** The maximum throughput in samples per second when using ::SO_BURSTIO mode. */
	AI_INFO_MAX_BURST_THROUGHPUT = 1004
}AiInfoItemDbl;

/** Use with ulAISetConfig() and ulAIGetConfig() to configure the AI subsystem. */
typedef enum
{
	/** The channel type of the specified  channel. Set with #AiChanType. */
	AI_CFG_CHAN_TYPE = 1,

	/** The thermocouple type of the specified channel. Set with #TcType. */
	AI_CFG_CHAN_TC_TYPE = 2,

	/** The temperature unit of the specified channel. Set with #TempUnit. */
	AI_CFG_CHAN_TEMP_UNIT = 3,

	/** The temperature unit. Set with #TempUnit. */
	AI_CFG_TEMP_UNIT = 4,
	
	/** The timing mode. Set with #AdcTimingMode. */
	AI_CFG_ADC_TIMING_MODE = 5,

	/** The auto zero mode. Set with #AutoZeroMode. */
	AI_CFG_AUTO_ZERO_MODE = 6,

	/** The date when the device was calibrated last. */
	AI_CFG_CAL_DATE = 7,

	/** The IEPE current excitation mode for the specified channel. Set with #IepeMode. */
	AI_CFG_CHAN_IEPE_MODE = 8,

	/** The coupling mode for the specified device. Set with #CouplingMode. */
	AI_CFG_CHAN_COUPLING_MODE = 9
}AiConfigItem;

/** Use with ulAISetConfigDbl() and ulAIGetConfigDbl() to configure the AI subsystem. */
typedef enum
{
	/** The slope of the specified channel. */
	AI_CFG_CHAN_SLOPE = 1000,

	/** The offset of the specified channel. */
	AI_CFG_CHAN_OFFSET = 1001,

	/** The sensitivity of the sensor connected to the specified channel. */
	AI_CFG_CHAN_SENSOR_SENSIVITY = 1002
}AiConfigItemDbl;

/** Calibration information */
typedef enum
{
	/** The calibration date */
	AI_CFG_CAL_DATE_STR = 2000
}AiConfigItemStr;


/** Use with ulAOGetInfo() to obtain information about the analog output subsystem. */
typedef enum
{
	/** The D/A resolution. */
	AO_INFO_RESOLUTION = 1,

	/** The number of D/A channels on the specified device. */
	AO_INFO_NUM_CHANS = 2,

	/** A bit mask of supported #ScanOption values. */
	AO_INFO_SCAN_OPTIONS = 3,

	/** Paced operations are supported. */
	AO_INFO_HAS_PACER = 4,

	/** The number of supported #Range values for D/A operations. */
	AO_INFO_NUM_RANGES = 5,

	/** The #Range for the specified range index. */
	AO_INFO_RANGE = 6,

	/** A bitmask of supported #TriggerType values. */
	AO_INFO_TRIG_TYPES = 7,

	/** FIFO size in bytes. */
	AO_INFO_FIFO_SIZE = 8
}AoInfoItem;

/** Use with ulAOGetInfoDbl() to obtain information about the Analog output subsystem. */
typedef enum
{
	/** The minimum scan rate of the specified device. */
	AO_INFO_MIN_SCAN_RATE = 1000,

	/** The maximum scan rate of the specified device. */
	AO_INFO_MAX_SCAN_RATE = 1001,

	/** The maximum scanning throughput of the specified device. */
	AO_INFO_MAX_THROUGHPUT = 1002
}AoInfoItemDbl;

/** Use with ulDIOGetInfo() to obtain information about the DIO subsystem. */
typedef enum
{
	/** The number of ports on the specified device. */
	DIO_INFO_NUM_PORTS = 1,

	/** The port type for the specified port index. */
	DIO_INFO_PORT_TYPE = 2,

	/** The #DigitalPortIoType for the specified port index. */
	DIO_INFO_PORT_IO_TYPE = 3,

	/** The number of bits on the port specified by the port index. */
	DIO_INFO_NUM_BITS = 4,

	/** Paced operations are supported for the specified digital direction. */
	DIO_INFO_HAS_PACER = 5,

	/** A bit mask of supported #ScanOption values for the specified digital direction. */
	DIO_INFO_SCAN_OPTIONS = 6,

	/** A bitmask of supported #TriggerType values for the specified digital direction. */
	DIO_INFO_TRIG_TYPES = 7,

	/** FIFO size in bytes for the specified digital direction. */
	DIO_INFO_FIFO_SIZE = 8
}DioInfoItem;

/** Use with ulDIOGetInfoDbl() to obtain information about the DIO subsystem. */
typedef enum
{
	/** The minimum scan rate of the specified device. */
	DIO_INFO_MIN_SCAN_RATE = 1000,

	/** The maximum scan rate of the specified device. */
	DIO_INFO_MAX_SCAN_RATE = 1001,

	/** The maximum scanning throughput of the specified device. */
	DIO_INFO_MAX_THROUGHPUT = 1002
}DioInfoItemDbl;

/** Use with ulDIOGetConfig() to configure the DIO subsystem. */
typedef enum
{
	/** The port direction. Set with #DigitalDirection. */
	DIO_CFG_PORT_DIRECTION_MASK = 1,
}DioConfigItem;

/** Use with ulCtrGetInfo() to obtain information about the counter subsystem. */
typedef enum
{
	/** The number of counter channels on the specified device. */
	CTR_INFO_NUM_CTRS = 1,

	/** A bitmask of supported #CounterMeasurementType values. */
	CTR_INFO_MEASUREMENT_TYPES = 2,

	/** A bitmask of supported #CounterMeasurementType values.*/
	CTR_INFO_MEASUREMENT_MODES = 3,

	/** A bitmask of supported #CounterRegisterType values. */
	CTR_INFO_REGISTER_TYPES = 4,

	/** The resolution of the specified counter channel */
	CTR_INFO_RESOLUTION = 5,

	/** Paced operations are supported. */
	CTR_INFO_HAS_PACER = 6,

	/** A bit mask of supported #ScanOption values. */
	CTR_INFO_SCAN_OPTIONS = 7,

	/** A bitmask of supported #TriggerType values. */
	CTR_INFO_TRIG_TYPES = 8,

	/** FIFO size in bytes. */
	CTR_INFO_FIFO_SIZE = 9
}CtrInfoItem;

/** Use with ulCtrGetInfoDbl() to obtain information about the counter subsystem. */
typedef enum
{
	/** The minimum scan rate in samples per second. */
	CTR_INFO_MIN_SCAN_RATE = 1000,

	/** The maximum scan rate of the specified device. */
	CTR_INFO_MAX_SCAN_RATE = 1001,

	/** The maximum throughput of the specified device. */
	CTR_INFO_MAX_THROUGHPUT = 1002
}CtrInfoItemDbl;

/** Use with ulTmrGetInfo() to obtain timer subsystem information. */
typedef enum
{
	/** #TimerType of the specified timer index. */
	TMR_INFO_NUM_TMRS = 1,

	/** The number of bits on the port specified by the port index. */
	TMR_INFO_TYPE = 2,
}TmrInfoItem;

/** Use with ulTmrGetInfoDbl() to obtain timer subsystem information. */
typedef enum
{
	/** The minimum frequency of the specified device. */
	TMR_INFO_MIN_FREQ = 1000,

	/** The maximum frequency of the specified device. */
	TMR_INFO_MAX_FREQ = 1001,
}TmrInfoItemDbl;

/** Use with ulDaqIGetInfo() to obtain DAQ input subsystem information. */
typedef enum
{
	/** A bitmask of supported #DaqInChanType values. */
	DAQI_INFO_CHAN_TYPES = 1,

	/** A bit mask of supported #ScanOption values. */
	DAQI_INFO_SCAN_OPTIONS = 2,

	/** A bitmask of supported #TriggerType values. */
	DAQI_INFO_TRIG_TYPES = 3,

	/** FIFO size in bytes. */
	DAQI_INFO_FIFO_SIZE = 4
}DaqIInfoItem;

/** Use with ulDaqIGetInfoDbl() to obtain information about the counter subsystem. */
typedef enum
{
	/** The minimum scan rate in samples per second. */
	DAQI_INFO_MIN_SCAN_RATE = 1000,

	/** The maximum scan rate of the specified device. */
	DAQI_INFO_MAX_SCAN_RATE = 1001,

	/** The maximum throughput of the specified device. */
	DAQI_INFO_MAX_THROUGHPUT = 1002
}DaqIInfoItemDbl;

/** Use with ulDaqOGetInfo() to obtain information about the synchronous output subsystem. */
typedef enum
{
	/** A bitmask of supported #DaqOutChanType values. */
	DAQO_INFO_CHAN_TYPES = 1,

	/** A bit mask of supported #ScanOption values. */
	DAQO_INFO_SCAN_OPTIONS = 2,

	/** A bitmask of supported #TriggerType values. */
	DAQO_INFO_TRIG_TYPES = 3,

	/** FIFO size in bytes. */
	DAQO_INFO_FIFO_SIZE = 4
}DaqOInfoItem;

/** Use with ulDaqOGetInfoDbl() to obtain information about the counter subsystem. */
typedef enum
{
	/** The minimum scan rate in samples per second. */
	DAQO_INFO_MIN_SCAN_RATE = 1000,

	/** The maximum scan rate of the specified device. */
	DAQO_INFO_MAX_SCAN_RATE = 1001,

	/** The maximum throughput of the specified device. */
	DAQO_INFO_MAX_THROUGHPUT = 1002
}DaqOInfoItemDbl;

/** \brief A structure representing the memory descriptor.
 *
*/
struct MemDescriptor
{
	/** A bitmask of #MemAccessType values. */
	unsigned int address;

	/** The size of the memory in bytes. */
	unsigned int size;

	/** The type of memory access for the specified device. */
	MemAccessType accessTypes;

	/** Reserved for future use */
	char reserved[64];
};

/** A structure representing the memory descriptor. */
typedef struct 	MemDescriptor MemDescriptor;

/**
 * \defgroup DeviceDiscovery Device Discovery
 * Manage devices connected to the system.
 * @{
 */
/**
 * Get the list of connected devices.
 * @param interfaceTypes the interface types to discover
 * @param daqDevDescriptors the array to receive the DaqDeviceDescriptors
 * @param numDescriptors on input, specifies the max number of descriptors; on output, specifies the actual number of descriptors
 * @return The UL error code.
 */

UlError ulGetDaqDeviceInventory(DaqDeviceInterface interfaceTypes, DaqDeviceDescriptor daqDevDescriptors[], unsigned int* numDescriptors );

/**
 * Create a device object within the Universal Library for the DAQ device specified by the descriptor, and assign the specified board number
 * to the DAQ device.
 * @param daqDevDescriptor device descriptor
 * @return The UL error code.
 */
DaqDeviceHandle ulCreateDaqDevice(DaqDeviceDescriptor daqDevDescriptor);

/**
 * Get descriptor information for a device.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param daqDeviceDescriptor the array to receive the DaqDeviceDescriptors
 * @return The UL error code.
 */
UlError ulGetDaqDeviceDescriptor(DaqDeviceHandle daqDeviceHandle, DaqDeviceDescriptor* daqDeviceDescriptor);

/**
 * Establish a connection to a physical DAQ device.
 * @param daqDeviceHandle the handle to the DAQ device
 * @return The UL error code.
 */
UlError ulConnectDaqDevice(DaqDeviceHandle daqDeviceHandle);

/**
 * Disconnect from a device.
 * @param daqDeviceHandle the handle to the DAQ device
 * @return The UL error code.
 */
UlError ulDisconnectDaqDevice(DaqDeviceHandle daqDeviceHandle);

/**
 * Remove a device from the Universal Library, and release all resources associated with that device.
 * @param daqDeviceHandle the handle to the DAQ device
 * @return The UL error code.
 */
UlError ulReleaseDaqDevice(DaqDeviceHandle daqDeviceHandle);

/**
 * The connection status of a DAQ device.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param connected the connection status
 * @return The UL error code.
 */
UlError ulIsDaqDeviceConnected(DaqDeviceHandle daqDeviceHandle, int* connected);

/** @} */ 

/**
 * \ingroup Misc
 * Causes the LED on a DAQ device to flash.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param flashCount The number of flashes; this parameter is ignored on some devices.
 * @return The UL error code.
 */
UlError ulFlashLed(DaqDeviceHandle daqDeviceHandle, int flashCount);

/**
 * \defgroup AnalogInput Analog Input
 * Configure the analog input subsystem and acquire data.
 * @{
 */

/**
 * Returns the value read from an A/D channel.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param channel A/D channel number
 * @param inputMode A/D channel mode
 * @param range A/D range; ignored if the specified A/D device does not have a programmable range.
 * @param flags bit mask that specifies whether to scale and/or calibrate the data
 * @param data pointer to the buffer to receive the A/D data
 * @return The value of the A/D sample.
 */
UlError ulAIn(DaqDeviceHandle daqDeviceHandle, int channel, AiInputMode inputMode, Range range, AInFlag flags, double* data);

/**
 * Scans a range of A/D channels, and stores the samples in an array.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param lowChan first A/D channel in the scan
 * @param highChan last A/D channel in the scan
 * @param inputMode A/D channel mode
 * @param range A/D range; ignored if the specified A/D device does not have a programmable range.
 * @param samplesPerChan the number of A/D samples to collect from each channel in the scan
 * @param rate A/D sample rate in samples per channel
 * @param options A/D scan options
 * @param flags bit mask that specifies whether to scale and/or calibrate the data
 * @param data pointer to the buffer to receive the data array
 * @return The actual sampling rate.
 */
UlError ulAInScan(DaqDeviceHandle daqDeviceHandle, int lowChan, int highChan, AiInputMode inputMode, Range range, int samplesPerChan, double* rate, ScanOption options, AInScanFlag flags, double data[]);

/**
 * Returns the status of an A/D scan operation.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param status the status of the background operation
 * @param xferStatus count and index values
 * @return The actual sampling rate.
 */
UlError ulAInScanStatus(DaqDeviceHandle daqDeviceHandle, ScanStatus* status, TransferStatus* xferStatus);

/**
 * Stops the analog input operation currently running.
 * @param daqDeviceHandle the handle to the DAQ device
 * @return The UL error code.
 */
UlError ulAInScanStop(DaqDeviceHandle daqDeviceHandle);

/**
 * Returns when the scan operation completes or the specified timeout elapses.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param waitType the wait type
 * @param waitParam Reserved for future use
 * @param timeout the timeout value in seconds (s)
 * @return The UL error code.
 */
UlError ulAInScanWait(DaqDeviceHandle daqDeviceHandle, WaitType waitType, long long waitParam, double timeout);

/**
 * Loads the A/D queue of a specified device.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param queue the channel values
 * @param numElements the number of elements in the queue
 * @return The UL error code.
 */
UlError ulAInLoadQueue(DaqDeviceHandle daqDeviceHandle, AiQueueElement queue[], unsigned int numElements);

/**
 * Selects the A/D trigger source and configures its parameters.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param type analog trigger types
 * @param trigChan the trigger channel
 * @param level the level at or around which the trigger event should be detected
 * @param variance the degree to which the input signal can vary relative to the level parameter
 * @param retriggerSampleCount the number of samples per trigger to acquire with each trigger event
 * @return The UL error code.
 */
UlError ulAInSetTrigger(DaqDeviceHandle daqDeviceHandle, TriggerType type, int trigChan, double level, double variance, unsigned int retriggerSampleCount);

/** @}*/ 

/** 
 * \defgroup AnalogOutput Analog Output
 * Configure the analog output subsystem and acquire data
 * @{
 */
 
/**
 * Writes the value of a D/A output.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param channel D/A channel number
 * @param range D/A range; ignored if the specified D/A device does not have a programmable range.
 * @param flags bit mask that specifies whether to scale and/or calibrate the data
 * @param data the value to write to the D/A channel
 * @return The D/A data value.
 */
UlError ulAOut(DaqDeviceHandle daqDeviceHandle, int channel, Range range, AOutFlag flags, double data);

/**
 * Writes values to a range of D/A channels.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param lowChan first D/A channel in the scan
 * @param highChan last D/A channel in the scan
 * @param range the D/A range code; ignored if the D/A channel does not have a programmable range
 * @param samplesPerChan the number of D/A samples to output
 * @param rate the sample rate in scans per second
 * @param options bit mask that specifies D/A scan options
 * @param flags bit mask that specifies whether to scale and/or calibrate the data
 * @param data pointer to the buffer to receive the data
 * @return The actual sample rate.
 */
UlError ulAOutScan(DaqDeviceHandle daqDeviceHandle, int lowChan, int highChan, Range range, int samplesPerChan, double* rate, ScanOption options, AOutScanFlag flags, double data[]);

/**
 * Returns when the scan operation completes or the specified timeout elapses.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param waitType the wait type
 * @param waitParam Reserved for future use
 * @param timeout the timeout value in milliseconds (ms)
 * @return The UL error code.
 */
UlError ulAOutScanWait(DaqDeviceHandle daqDeviceHandle, WaitType waitType, long long waitParam, double timeout);

/**
 * Returns the status of a D/A scan operation.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param status the status of the background operation
 * @param xferStatus count and index values
 * @return The UL error code.
 */
UlError ulAOutScanStatus(DaqDeviceHandle daqDeviceHandle, ScanStatus* status, TransferStatus* xferStatus);

/**
 * Stops the analog output operation currently running.
 * @param daqDeviceHandle the handle to the DAQ device
 * @return The UL error code.
 */
UlError ulAOutScanStop(DaqDeviceHandle daqDeviceHandle);

/**
 * Selects the D/A trigger source and triggers its parameters.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param type the trigger type
 * @param trigChan the trigger channel
 * @param level the level at or around which the trigger event should be detected
 * @param variance the degree to which the input signal can vary relative to the level parameter
 * @param retriggerSampleCount the number of samples to acquire with each trigger event
 * @return The UL error code.
 */
UlError ulAOutSetTrigger(DaqDeviceHandle daqDeviceHandle, TriggerType type, int trigChan, double level, double variance, unsigned int retriggerSampleCount);

/** @}*/ 

/** 
 * \defgroup DigitalIO Digital I/O
 * Configure the digital I/O subsystem and acquire data
 * @{
 */

/**
 * Configures a digital port as input or output.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param portType the port type
 * @param direction the port direction (input or output)
 * @return The UL error code.
 */
UlError ulDConfigPort(DaqDeviceHandle daqDeviceHandle, DigitalPortType portType, DigitalDirection direction);

/**
 * Configures a digital bit as input or output.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param portType the digital port; the port must be configurable.
 * @param bitNum the bit number
 * @param direction the bit direction (input or output)
 * @return The UL error code.
 */
UlError ulDConfigBit(DaqDeviceHandle daqDeviceHandle, DigitalPortType portType, int bitNum, DigitalDirection direction);

/**
 * Returns the value read from a digital input port.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param portType the port type
 * @param data the data value
 * @return The digital input port value.
 */
UlError ulDIn(DaqDeviceHandle daqDeviceHandle, DigitalPortType portType, unsigned long long* data);

/**
 * Writes the value of a digital output port.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param portType the type of digital port type
 * @param data the digital byte value
 * @return The UL error code.
 */
UlError ulDOut(DaqDeviceHandle daqDeviceHandle, DigitalPortType portType, unsigned long long data);

/**
 * Returns the value of a digital bit.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param portType the type of digital port to read
 * @param bitNum the bit number
 * @param bitValue the bit value
 * @return The value of a digital bit.
 */
UlError ulDBitIn(DaqDeviceHandle daqDeviceHandle, DigitalPortType portType, int bitNum, unsigned int* bitValue);

/**
 * Writes a value to a digital bit.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param portType the digital port type
 * @param bitNum the bit number of the specified digital port
 * @param bitValue the bit value
 * @return The UL error code.
 */
UlError ulDBitOut(DaqDeviceHandle daqDeviceHandle, DigitalPortType portType, int bitNum, unsigned int bitValue);

/**
 * Reads a range of digital ports.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param lowPort the first port number to scan
 * @param highPort the last port number to scan
 * @param samplesPerPort the number of samples to read
 * @param rate the number of times per second (Hz) to read the port
 * @param options digital scan options
 * @param flags bit masks that specifies whether to scale and/or calibrate the data
 * @param data the value of the digital data
 * @return The actual transfer rate.
 */
UlError ulDInScan(DaqDeviceHandle daqDeviceHandle, DigitalPortType lowPort, DigitalPortType highPort, int samplesPerPort, double* rate, ScanOption options, DInScanFlag flags, unsigned long long data[]);

/**
 * The status of a digital scan operation.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param status the status of the background operation
 * @param xferStatus count and index values
 * @return The UL error code.
 */
UlError ulDInScanStatus(DaqDeviceHandle daqDeviceHandle, ScanStatus* status, TransferStatus* xferStatus);

/**
 * Stops the digital input operation currently running.
 * @param daqDeviceHandle the handle to the DAQ device
 * @return The UL error code.
 */
UlError ulDInScanStop(DaqDeviceHandle daqDeviceHandle);

/**
 * Returns when the scan operation completes or the specified timeout elapses.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param waitType the wait type
 * @param waitParam Reserved for future use
 * @param timeout the timeout value in milliseconds (ms)
 * @return The UL error code.
 */
UlError ulDInScanWait(DaqDeviceHandle daqDeviceHandle, WaitType waitType, long long waitParam, double timeout);

/**
 * Selects the digital trigger source and configures its parameters.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param type the trigger type
 * @param trigChan the trigger channel
 * @param level the level at or around which the trigger event should be detected
 * @param variance the degree to which the input signal can vary relative to the level parameter
 * @param retriggerSampleCount the number of samples to acquire with each trigger event
 * @return The UL error code.
 */
UlError ulDInSetTrigger(DaqDeviceHandle daqDeviceHandle, TriggerType type, int trigChan, double level, double variance, unsigned int retriggerSampleCount);

/** DO functions
 * Writes a series of bytes or words to a digital port.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param lowPort the first port number to scan
 * @param highPort the last port number to scan
 * @param samplesPerPort the number of samples per port to write
 * @param rate the number of times per second (Hz) to write to the port.
 * @param options digital scan options
 * @param flags bit mask that specifies whether to scale and/or calibrate the data
 * @param data the data value
 * @return The actual update rate.
 */
UlError ulDOutScan(DaqDeviceHandle daqDeviceHandle, DigitalPortType lowPort, DigitalPortType highPort, int samplesPerPort, double* rate, ScanOption options, DOutScanFlag flags, unsigned long long data[]);

/**
 * Returns the status of the digital output operation
 * @param daqDeviceHandle the handle to the DAQ device
 * @param status the status of the background operation
 * @param xferStatus count and index values
 * @return The UL error code.
 */
UlError ulDOutScanStatus(DaqDeviceHandle daqDeviceHandle, ScanStatus* status, TransferStatus* xferStatus);

/**
 * Stops the digital output operation currently running.
 * @param daqDeviceHandle the handle to the DAQ device
 * @return The UL error code.
 */
UlError ulDOutScanStop(DaqDeviceHandle daqDeviceHandle);

/**
 * Returns when the scan operation completes or the specified timeout elapses.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param waitType the wait type
 * @param waitParam Reserved for future use
 * @param timeout the timeout value in milliseconds (ms)
 * @return The UL error code.
 */
UlError ulDOutScanWait(DaqDeviceHandle daqDeviceHandle, WaitType waitType, long long waitParam, double timeout);

/**
 * Selects the digital trigger type and configures trigger parameters.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param type the trigger type
 * @param trigChan the trigger channel
 * @param level the level at or around which the trigger event should be detected
 * @param variance the degree to which the output signal can vary relative to the level parameter
 * @param retriggerSampleCount the number of samples to acquire with each trigger event
 * @return The UL error code.
 */
UlError ulDOutSetTrigger(DaqDeviceHandle daqDeviceHandle, TriggerType type, int trigChan, double level, double variance, unsigned int retriggerSampleCount);

/** @}*/ 

/** 
 * \defgroup CounterInput Counter Input
 * Configure the counter input subsystem and acquire data
 * @{
 */
 
/**
 * Returns the value read from a counter.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param counterNum the counter number
 * @param data the pointer to the buffer to receive the data
 * @return The UL error code.
 */
UlError ulCIn(DaqDeviceHandle daqDeviceHandle, int counterNum, unsigned long long* data);

UlError ulCRead(DaqDeviceHandle daqDeviceHandle, int counterNum, CounterRegisterType regType, unsigned long long* data);

/**
 * Loads a value into the specified counter register.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param counterNum the counter number
 * @param registerType the register type
 * @param loadValue the load value
 * @return The UL error code.
 */
UlError ulCLoad(DaqDeviceHandle daqDeviceHandle, int counterNum, CounterRegisterType registerType, unsigned long long loadValue);

/**
 * Clears a specified counter (sets it to 0).
 * @param daqDeviceHandle the handle to the DAQ device
 * @param counterNum the counter number
 * @return The UL error code.
 */
UlError ulCClear(DaqDeviceHandle daqDeviceHandle, int counterNum);

/**
 * Configures a counter channel.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param counterNum the counter number
 * @param type the type of counter measurement
 * @param mode the counter mode
 * @param edgeDetection the edge to detect
 * @param tickSize bit mask that specifies the counter tick size
 * @param debounceMode bit mask that specifies the counter debounce mode
 * @param debounceTime bit mask that specifies the counter debounce time
 * @param flags bit mask that specifies the counter scan option
 * @return The UL error code.
 */
UlError ulCConfigScan(DaqDeviceHandle daqDeviceHandle, int counterNum, CounterMeasurementType type,  CounterMeasurementMode mode,
					  CounterEdgeDetection edgeDetection, CounterTickSize tickSize,
					  CounterDebounceMode debounceMode, CounterDebounceTime debounceTime, CConfigScanFlag flags);

/**
 * Reads a range of counter channels.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param lowCounterNum the first channel of the scan. This parameter is zero-based, so the first counter number is "0".
 * @param highCounterNum the last channel of the scan. This parameter is zero-based, so the first counter number is "0".
 * @param samplesPerCounter the number of counter samples to read.
 * @param rate the rate in samples per second at which samples are taken
 * @param options scan options
 * @param flags bit mask that specifies the counter scan option
 * @param data pointer to the buffer to receive the data
 * @return The actual sample rate.
 */
UlError ulCInScan(DaqDeviceHandle daqDeviceHandle, int lowCounterNum, int highCounterNum, int samplesPerCounter, double* rate, ScanOption options, CInScanFlag flags, unsigned long long data[]);

/**
 * Selects the counter trigger source and configures its parameters.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param type the trigger type
 * @param trigChan the trigger channel
 * @param level the level at or around which the trigger event should be detected
 * @param variance the degree to which the input signal can vary relative to the level parameter
 * @param retriggerSampleCount the number of samples to acquire with each trigger event
 * @return The UL error code.
 */
UlError ulCInSetTrigger(DaqDeviceHandle daqDeviceHandle, TriggerType type, int trigChan, double level, double variance, unsigned int retriggerSampleCount);

/**
 * Returns the status of a counter input operation.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param status the status of the background operation
 * @param xferStatus count and index values
 * @return The UL error code.
 */
UlError ulCInScanStatus(DaqDeviceHandle daqDeviceHandle, ScanStatus* status, TransferStatus* xferStatus);

/**
 * Stops the counter input operation currently running.
 * @param daqDeviceHandle the handle to the DAQ device
 * @return The UL error code.
 */
UlError ulCInScanStop(DaqDeviceHandle daqDeviceHandle);

/**
 * Returns when the scan operation completes or the specified timeout elapses.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param waitType the wait type
 * @param waitParam Reserved for future use
 * @param timeout the timeout value in milliseconds (ms)
 * @return The UL error code.
 */
UlError ulCInScanWait(DaqDeviceHandle daqDeviceHandle, WaitType waitType, long long waitParam, double timeout);

/** @}*/ 

/** 
 * \defgroup TimerOutput Timer Output
 * Configure the timer output subsystem and acquire data
 * @{
 */

/**
 * Starts a timer to generate digital pulses at a specified frequency and duty cycle.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param timerNum the timer number
 * @param frequency the timer frequency
 * @param dutyCycle the duty cycle
 * @param pulseCount the number of pulses to generate
 * @param initialDelay the amount of time in seconds to wait before the timer output
 * @param idleState the idle state (high or low)
 * @param options pulse out options
 * @return The UL error code.
 */
UlError ulTmrPulseOutStart(DaqDeviceHandle daqDeviceHandle, int timerNum, double* frequency, double* dutyCycle, unsigned long long pulseCount, double* initialDelay, TmrIdleState idleState, PulseOutOption options);

/**
 * Stops a timer output.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param timerNum the timer number to stop
 * @return The UL error code.
 */
UlError ulTmrPulseOutStop(DaqDeviceHandle daqDeviceHandle, int timerNum);

/**
 * The status of the timer output operation
 * @param daqDeviceHandle the handle to the DAQ device
 * @param timerNum the timer number
 * @param status the status of the background operation
 * @return The UL error code.
 */
UlError ulTmrPulseOutStatus(DaqDeviceHandle daqDeviceHandle, int timerNum, TmrStatus* status);

/**
 * Selects the trigger source and configures its parameters.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param type the trigger type
 * @param trigChan the trigger channel
 * @param level the level at or around which the trigger event should be detected
 * @param variance the degree to which the input signal can vary relative to the level parameter
 * @param retriggerSampleCount the number of samples to acquire with each trigger event
 * @return The UL error code.
 */
UlError ulTmrSetTrigger(DaqDeviceHandle daqDeviceHandle, TriggerType type, int trigChan, double level, double variance, unsigned int retriggerSampleCount);

/** @}*/ 

/** 
 * \defgroup SyncIo Synchronous device I/O
 * Configure the DAQ I/O subsystem and acquire data
 * @{
 */

/**
 * Scans analog, digital, counter, and temperature input channels synchronously, and stores the samples in an array.<br>
 * This method works with devices that support synchronous input.
 *
 * @param daqDeviceHandle the handle to the DAQ device
 * @param chanDescriptors the #DaqInChanDescriptor enumeration indicating the input channel descriptor
 * @param numChans the number of channels in the scan
 * @param samplesPerChan the number of A/D samples to collect from each channel in the scan
 * @param rate A/D sample rate in samples per channel
 * @param options scan options
 * @param flags bit mask that specifies whether to scale and/or calibrate the data
 * @param data pointer to the buffer to receive the data
 * @return The UL error code.
 */
UlError ulDaqInScan(DaqDeviceHandle daqDeviceHandle, DaqInChanDescriptor chanDescriptors[], int numChans, int samplesPerChan, double* rate, ScanOption options, DaqInScanFlag flags, double data[]);

/**
 * Returns the status of a synchronous input operation.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param status the status of the background operation
 * @param xferStatus count and index values
 * @return The UL error code.
 */
UlError ulDaqInScanStatus(DaqDeviceHandle daqDeviceHandle, ScanStatus* status, TransferStatus* xferStatus);

/**
 * Stops the synchronous input operation currently running.
 * @param daqDeviceHandle the handle to the DAQ device
 * @return The UL error code.
 */
UlError ulDaqInScanStop(DaqDeviceHandle daqDeviceHandle);

/**
 * Returns when the scan operation completes or the specified timeout elapses.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param waitType the wait type
 * @param waitParam reserved for future use
 * @param timeout the timeout value in milliseconds (ms)
 * @return The UL error code.
 */
UlError ulDaqInScanWait(DaqDeviceHandle daqDeviceHandle, WaitType waitType, long long waitParam, double timeout);

/**
 * Selects the trigger source and configures its parameters.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param type the trigger type
 * @param trigChanDescriptor the #DaqInChanDescriptor enumeration indicating the input channel descriptor
 * @param level the level at or around which the trigger event should be detected
 * @param variance the degree to which the input signal can vary relative to the level parameter
 * @param retriggerSampleCount the number of samples to acquire with each trigger event.
 * @return The UL error code.
 */
UlError ulDaqInSetTrigger(DaqDeviceHandle daqDeviceHandle, TriggerType type, DaqInChanDescriptor trigChanDescriptor, double level, double variance, unsigned int retriggerSampleCount);

/**
 * Outputs values synchronously to analog output channels and digital output ports.<br>
 * This function only works with devices that support synchronous output.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param chanDescriptors array to receive the DaqOutChanDescriptor
 * @param numChans the number of channels in the scan
 * @param samplesPerChan the number of samples to output
 * @param rate the sample rate in scans per second
 * @param options scan options
 * @param flags bit mask that specifies whether to scale and/or calibrate data
 * @param data pointer to the buffer to store the data
 * @return The actual sample rate
 */
UlError ulDaqOutScan(DaqDeviceHandle daqDeviceHandle, DaqOutChanDescriptor chanDescriptors[], int numChans, int samplesPerChan, double* rate, ScanOption options, DaqOutScanFlag flags, double data[]);

/**
 * Returns the status of a synchronous output operation.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param status the status of the background operation
 * @param xferStatus count and index values
 * @return The UL error code.
 */
UlError ulDaqOutScanStatus(DaqDeviceHandle daqDeviceHandle, ScanStatus* status, TransferStatus* xferStatus);

/**
 * Stops the synchronous output operation currently running.
 * @param daqDeviceHandle the handle to the DAQ device
 * @return The UL error code.
 */
UlError ulDaqOutScanStop(DaqDeviceHandle daqDeviceHandle);

/**
 * Stops a synchronous output operation for a specified time.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param waitType the type of wait
 * @param waitParam reserved for future use
 * @param timeout the timeout value in milliseconds (ms)
 * @return The UL error code.
 */
UlError ulDaqOutScanWait(DaqDeviceHandle daqDeviceHandle, WaitType waitType, long long waitParam, double timeout);

/**
 * Selects the trigger source and configures its parameters.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param type the trigger type
 * @param trigChanDescriptor array to receive the DaqInChanDescriptor
 * @param level the level at or around which the trigger event should be detected
 * @param variance the degree to which the input signal can vary relative to the level parameter
 * @param retriggerSampleCount the number of samples to acquire with each trigger event.
 * @return The UL error code.
 */
UlError ulDaqOutSetTrigger(DaqDeviceHandle daqDeviceHandle, TriggerType type, DaqInChanDescriptor trigChanDescriptor, double level, double variance, unsigned int retriggerSampleCount);

/** @}*/ 

/** 
 * \defgroup Misc Miscellaneous
 * Miscellaneous functions
 * @{
 */
 
/**
 * Binds one or more event conditions to a DaqEventCallback function.
 * Upon detection of an event condition, DaqEventCallback is invoked.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param eventTypes event conditions
 * @param eventParameter additional data that specifies an event condition
 * @param eventCallbackFunction the pointer to the user-defined callback function to handle event conditions.
 * @param userData the pointer to the data that will be passed to the callback function
 * @return The UL error code.
 */
UlError ulEnableEvent(DaqDeviceHandle daqDeviceHandle, DaqEventType eventTypes, unsigned long long eventParameter, DaqEventCallback eventCallbackFunction, void* userData);

/**
 * Disables one or more event conditions, and disconnects their user-defined handlers.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param eventTypes event conditions
 * @return The UL error code.
 */
UlError ulDisableEvent(DaqDeviceHandle daqDeviceHandle, DaqEventType eventTypes);

/**
 * Reads a value read from a specified region in memory.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param memRegion memory region
 * @param address memory address
 * @param buffer buffer size
 * @param count number or data points to read
 * @return The data value read from memory.
 */
UlError ulMemRead(DaqDeviceHandle daqDeviceHandle, MemRegion memRegion, unsigned int address, unsigned char* buffer, unsigned int count);

/**
 * Writes a value to a specified region in memory.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param memRegion memory region
 * @param address memory address
 * @param buffer buffer size
 * @param count number or data points to write
 * @return The data value written to memory.
 */
UlError ulMemWrite(DaqDeviceHandle daqDeviceHandle, MemRegion memRegion, unsigned int address, unsigned char* buffer, unsigned int count);

/**
 * Returns the error message associated with an error code.
 * @param errCode the error code returned
 * @param errMsg the text of the error associated with the error code
 * @return The UL error code.
 */
UlError ulGetErrMsg(UlError errCode, char errMsg[ERR_MSG_LEN]);

/** @}*/ 

/** 
 * \defgroup DeviceInfo Device Information
 * Retrieve device information
 * @{
 */

/**
 * Use with #UlInfoItemStr to retrieve device information as a null-terminated string.
 * @param infoItem the information to read from the device
 * @param index either ignored or an index into the infoStr
 * @param infoStr pointer to the buffer where the information string is copied
 * @param maxConfigLen pointer to the value holding the maximum number of bytes to be read from the device into configStr
 * @return The UL error code.
 * */
UlError ulGetInfoStr(UlInfoItemStr infoItem, unsigned int index, char* infoStr, unsigned int* maxConfigLen);


/**
 * Use with UlConfigItem to change device configuration options at runtime.
 * @param configItem the type of information to write to the device
 * @param index either ignored or an index into the configValue
 * @param configValue the specified configuration value is returned to this variable
 * @return The UL error code.
 * */
UlError ulSetConfig(UlConfigItem configItem, unsigned int index, long long configValue);


/**
 * Returns a configuration option set for the device.<br>Use ulSetConfig() to change configuration options.
 * @param configItem the configuration item to retrieve
 * @param index the index into the configItem
 * @param configValue the specified configuration value is returned to this variable
 * @return The UL error code. 
 */
UlError ulGetConfig(UlConfigItem configItem, unsigned int index, long long* configValue);

/**
 * Use with #DevInfoItem to retrieve information about the device subsystem.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param infoItem the subsystem information to retrieve
 * @param index either ignored or an index into the infoValue
 * @param infoValue the subsystem information is returned to this variable
 * @return The UL error code.
 */
UlError ulDevGetInfo(DaqDeviceHandle daqDeviceHandle, DevInfoItem infoItem, unsigned int index, long long* infoValue);

/**
 * Use with #DevConfigItemStr to retrieve configuration information as a null-terminated string.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param configItem the configuration item to retrieve from the device
 * @param index either ignored or an index into the configStr
 * @param configStr pointer to the buffer where the configuration string is copied
 * @param maxConfigLen pointer to the value holding the maximum number of bytes to be read from the device into configStr
 * @return The UL error code.
 */
UlError ulDevGetConfigStr(DaqDeviceHandle daqDeviceHandle, DevConfigItemStr configItem, unsigned int index, char* configStr, unsigned int* maxConfigLen);

/** @}*/ /** end of DeviceInfo group */

/**
 * \ingroup AnalogInput
 * Use with #AiInfoItem to retrieve information about the AI subsystem.
 * @param daqDeviceHandle the device the handle to the DAQ device
 * @param infoItem the analog input information to retrieve
 * @param index either ignored or an index into the infoValue
 * @param infoValue the AI information is returned to this variable
 * @return The UL error code.
 */
UlError ulAIGetInfo(DaqDeviceHandle daqDeviceHandle, AiInfoItem infoItem, unsigned int index, long long* infoValue);

/**
 * \ingroup AnalogInput
 * Use with #AiInfoItemDbl to retrieve information about the AI subsystem.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param infoItem the analog input information to retrieve
 * @param index either ignored or an index into the infoValue
 * @param infoValue the AI information is returned to this variable
 * @return The UL error code.
 */
UlError ulAIGetInfoDbl(DaqDeviceHandle daqDeviceHandle, AiInfoItemDbl infoItem, unsigned int index, double* infoValue);

/**
 * \ingroup AnalogInput
 * Use with #AiConfigItem to set configuration options at runtime.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param configItem the configuration item to set
 * @param index either ignored or an index into the configValue
 * @param configValue the specified configuration value is returned to this variable
 * @return The UL error code.
 */
UlError ulAISetConfig(DaqDeviceHandle daqDeviceHandle, AiConfigItem configItem, unsigned int index, long long configValue);

/**
 * \ingroup AnalogInput
 * Use with #AiConfigItem to retrieve configuration options set for a device.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param configItem the configuration item to retrieve
 * @param index either ignored or an index into the configValue
 * @param configValue the specified configuration value is returned to this variable
 * @return The UL error code.
 */
UlError ulAIGetConfig(DaqDeviceHandle daqDeviceHandle, AiConfigItem configItem, unsigned int index, long long* configValue);

/**
 * \ingroup AnalogInput
 * Use with #AiConfigItemDbl to set configuration options at runtime.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param configItem the configuration item to set
 * @param index either ignored or an index into the configValue
 * @param configValue the specified configuration value is returned to this variable
 * @return The UL error code.
 */
UlError ulAISetConfigDbl(DaqDeviceHandle daqDeviceHandle, AiConfigItemDbl configItem, unsigned int index, double configValue);

/**
 * \ingroup AnalogInput
 * Use with #AiConfigItem to retrieve configuration options set for a device.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param configItem the configuration item to retrieve
 * @param index either ignored or an index into the configValue
 * @param configValue the specified configuration value is returned to this variable
 * @return The UL error code.
 */
UlError ulAIGetConfigDbl(DaqDeviceHandle daqDeviceHandle, AiConfigItemDbl configItem, unsigned int index, double* configValue);

/**
 * \ingroup AnalogInput
 * Use with #AiConfigItemDbl to retrieve configuration information as a null-terminated string.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param configItem the configuration item to retrieve
 * @param index either ignored or an index into the configStr
 * @param configStr pointer to the buffer where the configuration string is copied
 * @param maxConfigLen pointer to the value holding the maximum number of bytes to be read from the device into configStr
 * @return The UL error code.
 */
UlError ulAIGetConfigStr(DaqDeviceHandle daqDeviceHandle, AiConfigItemStr configItem, unsigned int index, char* configStr, unsigned int* maxConfigLen);

/** start AO info/config
 * \ingroup AnalogOutput
 * Use with #AoInfoItem to retrieve information about the AO subsystem.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param infoItem the analog output information to retrieve
 * @param index either ignored or an index into the infoValue
 * @param infoValue the AO information is returned to this variable
 * @return The UL error code.
 */
UlError ulAOGetInfo(DaqDeviceHandle daqDeviceHandle, AoInfoItem infoItem, unsigned int index, long long* infoValue);

/**
 * \ingroup AnalogOutput
 * Use with #AoInfoItemDbl to retrieve information about the AO subsystem.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param infoItem the analog output information to retrieve
 * @param index either ignored or an index into the infoValue
 * @param infoValue the AO information is returned to this variable
 * @return The UL error code.
 */
UlError ulAOGetInfoDbl(DaqDeviceHandle daqDeviceHandle, AoInfoItemDbl infoItem, unsigned int index, double* infoValue);

/** start of DIO info/config
 * \ingroup DigitalIO
 * Use with #DioInfoItem to retrieve information about the DIO subsystem.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param infoItem the digital I/O information to retrieve
 * @param index either ignored or an index into the infoValue
 * @param infoValue the DIO information is returned to this variable
 * @return The UL error code.
 */
UlError ulDIOGetInfo(DaqDeviceHandle daqDeviceHandle, DioInfoItem infoItem, unsigned int index, long long* infoValue);

/**
 * \ingroup DigitalIO
 * Use with #DioInfoItemDbl to retrieve information about the DIO subsystem.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param infoItem the digital I/O information to retrieve
 * @param index either ignored or an index into the infoValue
 * @param infoValue the DIO information is returned to this variable
 * @return The UL error code.
 */
UlError ulDIOGetInfoDbl(DaqDeviceHandle daqDeviceHandle, DioInfoItemDbl infoItem, unsigned int index, double* infoValue);

/**
 * \ingroup DigitalIO
 * Use with #DioConfigItem to retrieve information about the DIO subsystem.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param configItem the configuration item to retrieve
 * @param index either ignored or an index into the configValue
 * @param configValue the specified configuration value is returned to this variable
 * @return The UL error code.
 */
UlError ulDIOGetConfig(DaqDeviceHandle daqDeviceHandle, DioConfigItem configItem, unsigned int index, long long* configValue);

/**
 * \ingroup CounterInput
 * Use with #CtrInfoItem to retrieve information about the counter subsystem.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param infoItem the counter information to retrieve
 * @param index either ignored or an index into the infoValue
 * @param infoValue the counter information is returned to this variable
 * @return The UL error code.
 */
UlError ulCtrGetInfo(DaqDeviceHandle daqDeviceHandle, CtrInfoItem infoItem, unsigned int index, long long* infoValue);

/**
 * \ingroup CounterInput
 * Use with #CtrInfoItemDbl to retrieve information about the counter subsystem.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param infoItem the counter information to retrieve
 * @param index either ignored or an index into the infoValue
 * @param infoValue the counter information is returned to this variable
 * @return The UL error code.
 */
UlError ulCtrGetInfoDbl(DaqDeviceHandle daqDeviceHandle, CtrInfoItemDbl infoItem, unsigned int index, double* infoValue);

/**
 * \ingroup TimerOutput
 * Use with #TmrInfoItem to retrieve information about the timer subsystem.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param infoItem the timer information to retrieve
 * @param index either ignored or an index into the infoValue
 * @param infoValue the timer information is returned to this variable
 * @return The UL error code.
 */
UlError ulTmrGetInfo(DaqDeviceHandle daqDeviceHandle, TmrInfoItem infoItem, unsigned int index, long long* infoValue);

/**
 * \ingroup TimerOutput
 * Use with #TmrInfoItemDbl to retrieve information about the timer subsystem.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param infoItem the timer information to retrieve
 * @param index either ignored or an index into the infoValue
 * @param infoValue the timer information is returned to this variable
 * @return The UL error code.
 */
UlError ulTmrGetInfoDbl(DaqDeviceHandle daqDeviceHandle, TmrInfoItemDbl infoItem, unsigned int index, double* infoValue);

/**
 * \ingroup SyncIo
 * Use with #DaqIInfoItem to retrieve information about the synchronous input subsystem.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param infoItem the synchronous input information to retrieve
 * @param index either ignored or an index into the infoValue
 * @param infoValue the synchronous input information is returned to this variable
 * @return The UL error code.
 */
UlError ulDaqIGetInfo(DaqDeviceHandle daqDeviceHandle, DaqIInfoItem infoItem, unsigned int index, long long* infoValue);

/**
 * \ingroup SyncIo
 * Use with #DaqIInfoItemDbl to retrieve information about the synchronous input subsystem.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param infoItem the synchronous input information to retrieve
 * @param index either ignored or an index into the infoValue
 * @param infoValue the synchronous input information is returned to this variable
 * @return The UL error code.
 */
UlError ulDaqIGetInfoDbl(DaqDeviceHandle daqDeviceHandle, DaqIInfoItemDbl infoItem, unsigned int index, double* infoValue);

/**
 * \ingroup SyncIo
 * Use with #DaqOInfoItem to retrieve information about the synchronous output subsystem.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param infoItem the synchronous output information to retrieve
 * @param index either ignored or an index into the infoValue
 * @param infoValue the synchronous output information is returned to this variable
 * @return The UL error code.
 */
UlError ulDaqOGetInfo(DaqDeviceHandle daqDeviceHandle, DaqOInfoItem infoItem, unsigned int index, long long* infoValue);

/**
 * \ingroup SyncIo
 * Use with #DaqOInfoItemDbl to retrieve information about the synchronous output subsystem.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param infoItem the synchronous output information to retrieve
 * @param index either ignored or an index into the infoValue
 * @param infoValue the synchronous output information is returned to this variable
 * @return The UL error code.
 */
UlError ulDaqOGetInfoDbl(DaqDeviceHandle daqDeviceHandle, DaqOInfoItemDbl infoItem, unsigned int index, double* infoValue);

/**
 * \ingroup DeviceInfo
 * Use with MemDescriptor to retrieve information about the memory region on a DAQ device.
 * @param daqDeviceHandle the handle to the DAQ device
 * @param memRegion the memory region
 * @param memDescriptor the MemDescriptor memory descriptor
 * @return The UL error code.
 */

UlError ulMemGetInfo(DaqDeviceHandle daqDeviceHandle, MemRegion memRegion, MemDescriptor* memDescriptor);


/** \mainpage
 * <h1>Introduction</h1>
 * <p>UL for Linux is a software API used to access and control supported Measurement Computing DAQ devices over the Linux platform. The UL for Linux binary name is libuldaq.</p>
 * <p>Refer to the <a href="uldaq_8h.html">API File Reference</a> for the data structures and enumerations included in the API.</p>

 * <h2>Requirements</h2>
 * <ul>
 *     <li>libusb API library</li>
 * </ul>
 * <p>UL for Linux API uses the libusb C library to access MCC devices. When creating programs with the UL for Linux API, include a reference to the libusb header. Refer to <a href="http://libusb.info/">http://libusb.info/</a> for more information about libusb, including download locations.</p>

 * <h2>Getting Started</h2>
 * <p>The <a href="modules.html">Modules</a> page provides links to the different categories of libuldaq functionality, and is a good place to start reading about the API documentation.</p>

 * <h2>Error Handling</h2>
 * <p>UL for Linux functions return 0 on success or a numeric value &gt;1 on failure. The error codes relate to UlError enumerator values.</p>

 * <h2>Contact Information</h2>
 * <p>Measurement Computing Corporation
 * <br>508-946-5100
 * <br>Technical Support: <a href="https://www.mccdaq.com/support.aspx">www.mccdaq.com/support</a>
 * <br>Knowledgebase: <a href="http://kb.mccdaq.com/Default.aspx">kb.mccdaq.com</a>
 * <br><a href="https://www.mccdaq.com">www.mccdaq.com</a></p>
*/

/** \page api API file reference
 * uldaq.h
 */

/** \page hw Supported Hardware
 * Measurement Computing hardware devices that support UL for Linux
 * <table class="doxtable">
 * <tr><td>USB-1208FS-Plus</td><td>USB-1608FS-Plus</td><td>USB-201<br>USB-202<br>USB-204<br>USB-205</td></tr>
 * <tr><td>USB-1208HS<br>USB-1208HS-2AO<br>USB-1208HS-4AO</td><td>USB-1608G<br>USB-1608GX<br>USB-1608GX-2AO</td><td>USB-2623<br>USB-2627<br>USB-2633<br>USB-2637</td></tr>
 * <tr><td>USB-1408FS-Plus</td><td>USB-1808<br>USB-1808X</td><td>USB-DIO32HS</td></tr>
 * </table>
 * The list of MCC devices that support UL for Linuxis also posted on our website at 
 * <a href="https://www.mccdaq.com/PDFs/Manuals/Linux-hw.pdf">UL for Linux Supported Products</a>
 * <br>
 */

 /** \page examples Example Projects
 * UL for Linux example projects to run with MCC hardware
 * <p>The UL for Linux package includes an installer file &quot;TBD&quot; used to download,install, and run UL for Linux example projects.
 * Users can alternately import the example code into an IDE such as
Eclipse.</p>
<p>Complete the following steps to install the UL for Linux example projects:</p>
<ol>
<li>TBD</li>
<li>TBD</li>
<li>TBD</li>
<li>TBD</li>
</ol>
<!-- Example programs ==================================================================================-->
<h2>UL for Linux Example projects</h2>
<table class="doxtable" width="70%">
<tr><td width="20%"><strong>Example name</strong></td><td><strong>Description</strong></td></tr>
<tr><td>AIn</td><td>Reads an A/D input channel. Demonstrates the use of ulAIn().</td></tr>
<tr><td>AInScan</td><td>Scans a range of A/D input channels, and stores the data in an array. Demonstrates the use of ulAInScan()
and ulAInScanStop().</td></tr>

<tr><td>AInScanEvents</td><td>Performs an A/D scan using events to determine when data is available or when
the acquisition is complete. The example also demonstrates how to retrieve the data when it becomes
available. Demonstrates the use of ulAInScan(), ulAInScan(), and ulAInScanStop().</td></tr>
<tr><td>AInScanLoadQueue</td><td>Creates a channel gain queue that sets individual channel ranges for an A/D scan. Demonstrates the
use of ulALoadQueue(), ulAInScan(), and ulAInScanStop().</td></tr>
<tr><td>AInScanWithTrigger</td><td>Scans a range of A/D channels when a trigger is received, and stores the data in an array. This
 example shows how to obtain and configure trigger options. Demonstrates the use of ulAInScan() and ulAInScanStop().</td></tr>
<tr><td>AOut</td><td>Writes a specified value to a D/A output channel. Demonstrates the use of ulAOut().</td></tr>
<tr><td>AOutScan</td><td>Performs a D/A scan that outputs a sine wave to channel 0, and a ramp function to channel 1. Data can be
viewed with an oscilloscope or meter. Demonstrates the use of ulAOut() and ulAOutScanStop().</td></tr>
<tr><td>CtrIn</td><td>Sets the initial value of a counter and counts events. Demonstrates the use of ulCIn() and ulCLoad().</td></tr>
<tr><td>CtrInScan</td><td>Scans a range of counter channels. Demonstrates the use of ulCInScan(), ulCLoad() and ulCInScanStop().</td></tr>
<tr><td>CtrInScanEncoder</td><td>Scans a range of encoder data. Demonstrates the use of ulCInScan(), ulCConfigScan(), and ulCInScanStop().</td></tr>
<tr><td>DaqInScan</td><td>Simultaneously acquires analog, digital, and counter data. Demonstrates the use of ulDaqInScan() and
ulDaqInScanStop().</td></tr>
<tr><td>DaqInScanWithTrigger</td><td>Sets up a trigger function, and simultaneously acquires analog, digital, and counter data when the
trigger is received. Demonstrates the use of ulDaqInScan() and ulDaqInScanStop().</td></tr>
<tr><td>DaqOutScan</td><td>Simultaneously outputs an analog sine wave and a digital ramp signal.
Demonstrates the use of ulDaqOutScan().</td></tr>
<tr><td>DBitIn</td><td>Configures multiple digital bits for input and reads the bit values. Demonstrates the use of ulDConfigBit() and
ulDIn().</td></tr>
<tr><td>DBitOut</td><td>Writes a specified value to multiple digital output bits. Demonstrates the use of ulDConfigBit() and ulDBitOut().</td></tr>
<tr><td>DIn</td><td>Configures a port for input and reads the port value. Demonstrates the use of ulDConfigPort() and ulDIn().</td></tr>
<tr><td>DInScan</td><td>Configures a port for input and performs multiple port reads. Demonstrates the use of ulDConfigPort(), ulDIn(), and
ulDInScanStop().</td></tr>
<tr><td>DOut</td><td>Configures a port for output and writes a specified value. Demonstrates the use of ulDConfigPort() and ulDOut().</td></tr>
<tr><td>DOutScan</td><td>Configures the port direction and outputs a ramp signal. Demonstrates the use of ulDConfigPort(), ulDOutScan(), and ulDOutScanStop().</td></tr>
<tr><td>TmrPulseOut</td><td>Generates an output pulse at a specified duty cycle and frequency. Demonstrates the use of ulTmrPulseOutStart() and ulTmrPulseOutStop().</td></tr>
</table>
<br>
*/


#ifdef __cplusplus
}
#endif

#endif /* UL_DAQ_H_ */
