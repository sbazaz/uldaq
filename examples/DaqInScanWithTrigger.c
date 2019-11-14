/*
    UL call demonstrated:        	  ulDaqInSetTrigger()

    Purpose:                          ulDaqInSetTrigger

    Demonstration:                    Uses the first available trigger type to
                                      set up an external trigger that is used
                                      to start a scan of the available analog,
                                      digital, and/or counter subsystems

    Steps:
    1. Call ulGetDaqDeviceInventory() to get the list of available DAQ devices
    2. Call ulCreateDaqDevice() to to get a handle for the first DAQ device
    3. Verify the DAQ device has an DAQ input subsystem
    4. Get the channel types supported by the DAQ input subsystem
    5. Call ulConnectDaqDevice() to establish a UL connection to the DAQ device
    6. Configure the available analog, digital, and counter channels
    7. Call ulDaqInSetTrigger to set the external trigger
    8. Call ulDaqInScan() to start the scan
    9. Call ulDaqInScanStatus to check the status of the background operation
    10. Display the data for each channel
    11. Call ulDaqInScanStop() to stop the background operation
    12. Call ulDisconnectDaqDevice and ulReleaseDaqDevice() before exiting the process
*/

#include <stdio.h>
#include <stdlib.h>
#include "uldaq.h"
#include "utility.h"


// prototypes
UlError ConfigureAnalogInputChannels(int numberOfChannels, Range range, DaqInChanDescriptor* descriptors, int* scanDesriptorIndex);
UlError ConfigureDigitalInputChannel(DaqDeviceHandle daqDeviceHandle, DaqInChanDescriptor* descriptors, int* scanDesriptorIndex);
UlError ConfigureCounterInputChannels(int numberOfChannels, DaqInChanDescriptor* descriptors, int* scanDesriptorIndex);

#define MAX_DEV_COUNT  100
#define MAX_STR_LENGTH 64
#define MAX_SCAN_OPTIONS_LENGTH 256
#define MAX_SCAN_CHAN_COUNT 64

int main(void)
{
	int descriptorIndex = 0;
	AiInputMode inputMode = AI_SINGLE_ENDED;
	DaqDeviceDescriptor devDescriptors[MAX_DEV_COUNT];
	DaqDeviceInterface interfaceType = ANY_IFC;
	DaqDeviceHandle daqDeviceHandle = 0;
	unsigned int numDevs = MAX_DEV_COUNT;

	int samplesPerChannel = 10000;
	double rate = 1000;
	Range range = BIP10VOLTS;
	ScanOption scanOptions = (ScanOption) (SO_DEFAULTIO | SO_CONTINUOUS | SO_EXTTRIGGER);
	DaqInScanFlag flags = DAQINSCAN_FF_DEFAULT;

	int numberOfAiChannels = 0;
	int numberOfScanChannels = 0;
	int hasDAQI = 0;
	int index = 0;
	int chanTypesMask = 0;
	TriggerType triggerType;

	char inputModeStr[MAX_STR_LENGTH];
	char scanOptionsStr[MAX_SCAN_OPTIONS_LENGTH];
	char daqiChannelTypeStr[MAX_SCAN_OPTIONS_LENGTH];
	char rangeStr[MAX_SCAN_OPTIONS_LENGTH];
	char triggerTypeStr[MAX_SCAN_OPTIONS_LENGTH];

	DaqInChanDescriptor scanDescriptors[MAX_SCAN_CHAN_COUNT];

	// uncomment this line if you want to change the trigger channel from an
	// external trigger to an analog channel
	//DaqInChanDescriptor dummyDesc;

	int scanDescriptorIndex = 0;

	double* buffer = NULL;
	UlError err = ERR_NO_ERROR;

	int i = 0;
	int __attribute__((unused)) ret;
	char c;

	// Get descriptors for all of the available DAQ devices
	err = ulGetDaqDeviceInventory(interfaceType, devDescriptors, &numDevs);

	if (err != ERR_NO_ERROR)
		goto end;

	// verify at least one DAQ device is detected
	if (numDevs == 0)
	{
		printf("No DAQ device is detected\n");
		goto end;
	}

	printf("Found %d DAQ device(s)\n", numDevs);
	for (i = 0; i < (int) numDevs; i++)
		printf("  %s: (%s)\n", devDescriptors[i].productName, devDescriptors[i].uniqueId);

	// get a handle to the DAQ device associated with the first descriptor
	daqDeviceHandle = ulCreateDaqDevice(devDescriptors[descriptorIndex]);

	if (daqDeviceHandle == 0)
	{
		printf ("\nUnable to create a handle to the specified DAQ device\n");
		goto end;
	}

	// verify the specified device supports analog input
	err = getDevInfoHasDaqi(daqDeviceHandle, &hasDAQI);
	if (!hasDAQI)
	{
		printf("\nThe specified DAQ device does not support DAQ input\n");
		goto end;
	}

	// get the first supported trigger type
	err = getDaqiInfoFirstTriggerType(daqDeviceHandle, &triggerType, triggerTypeStr);
	if (err != ERR_NO_ERROR)
	{
		printf("\nThe specified DAQ device does not support an external trigger\n");
		goto end;
	}

	printf("\nConnecting to device %s - please wait ...\n", devDescriptors[descriptorIndex].devString);

	// establish a connection to the DAQ device
	err = ulConnectDaqDevice(daqDeviceHandle);

	if (err != ERR_NO_ERROR)
		goto end;


	// get the channel types supported by the DAQ input subsystem
	err = getDaqiChannelTypes(daqDeviceHandle, &chanTypesMask);

	if (chanTypesMask == 0)
	{
		printf("\nDaqInScan is not supported by the specified DAQ device\n");
		goto end;
	}

	// configure the analog channels
	if (chanTypesMask & DAQI_ANALOG_SE)
	{
		// get the first supported analog input mode
		err = getAiInfoFirstSupportedInputMode(daqDeviceHandle, &numberOfAiChannels, &inputMode, inputModeStr);

		// get the first supported input range
		getAiInfoFirstSupportedRange(daqDeviceHandle, inputMode, &range, rangeStr);

		err = ConfigureAnalogInputChannels(2, range, scanDescriptors, &scanDescriptorIndex);
	}

	// configure the digital channels
	if ((chanTypesMask & DAQI_DIGITAL) && err == ERR_NO_ERROR)
	{
		err = ConfigureDigitalInputChannel(daqDeviceHandle, scanDescriptors, &scanDescriptorIndex);
	}
	else

	// configure the counter channels
	if ((chanTypesMask & DAQI_CTR32) && err == ERR_NO_ERROR)
	{
		err = ConfigureCounterInputChannels(1, scanDescriptors, &scanDescriptorIndex);
	}

	numberOfScanChannels = scanDescriptorIndex;
	
	// since this example uses the external trigger, a descriptor for the trigger channel
	// is not required ... this parameter is only used for an analog trigger channel
	//
	// if you want to change the trigger type (or any other trigger parameter), uncomment this
	// function call and change the trigger type (or any other parameter)
	//err = ulDaqInSetTrigger( daqDeviceHandle, triggerType, dummyDesc, 0.0, 0.0, 0);

	// allocate a buffer to receive the data
	buffer = (double*) malloc(numberOfScanChannels * samplesPerChannel * sizeof(double));

	if(buffer == 0)
	{
		printf("\nOut of memory, unable to create scan buffer\n");
		goto end;
	}

	ConvertScanOptionsToString(scanOptions, scanOptionsStr);

	printf("\n%s ready\n", devDescriptors[descriptorIndex].devString);
	printf("    Function demonstrated: ulDaqInSetTrigger()\n");
	printf("    Number of scan channels: %d\n", numberOfScanChannels);
	for (i=0; i<numberOfScanChannels; i++)
	{
		ConvertDaqIChanTypeToString(scanDescriptors[i].type, daqiChannelTypeStr);
		if (scanDescriptors[i].type == DAQI_ANALOG_SE || scanDescriptors[i].type == DAQI_ANALOG_DIFF)
		{
			ConvertRangeToString(scanDescriptors[i].range, rangeStr);
			printf("        ScanChannel %d: type = %s, channel = %d, range = %s\n", i, daqiChannelTypeStr, scanDescriptors[i].channel, rangeStr);
		}
		else
		{
			printf("        ScanChannel %d: type = %s, channel = %d\n", i, daqiChannelTypeStr, scanDescriptors[i].channel);
		}
	}
	printf("    Samples per channel: %d\n", samplesPerChannel);
	printf("    Rate: %f\n", rate);
	printf("    Scan options: %s\n", scanOptionsStr);
	printf("    Trigger type: %s\n", triggerTypeStr);
	printf("\nHit ENTER to continue\n");

	ret = scanf("%c", &c);

	// clear the display
	ret = system("clear");

	err = ulDaqInScan(daqDeviceHandle, scanDescriptors, numberOfScanChannels, samplesPerChannel, &rate, scanOptions, flags, buffer);

	if(err == ERR_NO_ERROR)
	{
		ScanStatus status;
		TransferStatus transferStatus;
		int i = 0;

		// get the initial status of the acquisition
		ulDaqInScanStatus(daqDeviceHandle, &status, &transferStatus);

		printf ("Hit 'Enter' to quit waiting for trigger\n\n");
		printf("Active DAQ device: %s (%s)\n\n", devDescriptors[descriptorIndex].productName, devDescriptors[descriptorIndex].uniqueId);
		printf ("Waiting for trigger ...\n");

		while(status == SS_RUNNING && err == ERR_NO_ERROR && !enter_press())
		{
			// get the current status of the acquisition
			err = ulDaqInScanStatus(daqDeviceHandle, &status, &transferStatus);

			index = transferStatus.currentIndex;
			if(err == ERR_NO_ERROR && index >= 0)
			{
				// reset the cursor to the top of the display and
				// show the termination message
				resetCursor();
				printf("%-40s\n\n","Hit 'Enter' to terminate the process");
				printf("Active DAQ device: %s (%s)\n\n", devDescriptors[descriptorIndex].productName, devDescriptors[descriptorIndex].uniqueId);
				printf("actual scan rate = %f\n\n", rate);

				printf("currentScanCount =  %-10llu \n", transferStatus.currentScanCount);
				printf("currentTotalCount = %-10llu \n", transferStatus.currentTotalCount);
				printf("currentIndex =      %-10d \n\n", index);

				// display the data
				for (i = 0; i < numberOfScanChannels; i++)
				{
					if (scanDescriptors[i].type == DAQI_ANALOG_SE ||scanDescriptors[i].type == DAQI_ANALOG_DIFF)
					{
						printf("chan (%s%d) = %+-10.6f\n",
								"Ai", scanDescriptors[i].channel,
								buffer[index + i]);
					}
					else
					{
						printf("chan (%s%d) = %-10lld\n",
								(scanDescriptors[i].type == DAQI_DIGITAL) ? "Di" : "Ci", scanDescriptors[i].channel,
								(long long)buffer[index + i]);
					}
				}

				usleep(100000);
			}
		}

		if (index < 0)
			printf("Trigger cancelled by user\n");

		// stop the acquisition if it is still running
		if (status == SS_RUNNING && err == ERR_NO_ERROR)
		{
			err = ulDaqInScanStop(daqDeviceHandle);
		}
	}

	// disconnect from the device
	ulDisconnectDaqDevice(daqDeviceHandle);

end:

	// release the handle to the device
	ulReleaseDaqDevice(daqDeviceHandle);

	// release the scan buffer
	if(buffer)
		free(buffer);

	if(err != ERR_NO_ERROR)
	{
		char errMsg[ERR_MSG_LEN];
		ulGetErrMsg(err, errMsg);
		printf("Error Code: %d \n", err);
		printf("Error Message: %s \n", errMsg);
	}

	return 0;
}

UlError ConfigureAnalogInputChannels(int numberOfChannels, Range range, DaqInChanDescriptor* descriptors, int* scanDesriptorIndex)
{
	UlError err = ERR_NO_ERROR;
	int i;
	int index = *scanDesriptorIndex;

	// fill a descriptor for each channel
	for ( i = 0; i < numberOfChannels; i++)
	{
		descriptors[index].channel = i;
		descriptors[index].type = DAQI_ANALOG_SE;
		descriptors[index].range = range;
		index++;
	}

	*scanDesriptorIndex = index;

	return err;
}

UlError ConfigureDigitalInputChannel(DaqDeviceHandle daqDeviceHandle, DaqInChanDescriptor* descriptors, int* scanDesriptorIndex)
{
	UlError err = ERR_NO_ERROR;
	DigitalPortType portType;
	char portTypeStr[MAX_STR_LENGTH];
	int index = *scanDesriptorIndex;

	err = getDioInfoFirstSupportedPortType(daqDeviceHandle, &portType, portTypeStr);

	// configure the port for input
	err = ulDConfigPort(daqDeviceHandle, portType, DD_INPUT);

	descriptors[index].channel = portType;
	descriptors[index].type = DAQI_DIGITAL;
	index++;

	*scanDesriptorIndex = index;

	return err;
}

UlError ConfigureCounterInputChannels(int numberOfChannels, DaqInChanDescriptor* descriptors, int* scanDesriptorIndex)
{
	UlError err = ERR_NO_ERROR;
	int i;
	int index = *scanDesriptorIndex;

	// fill a descriptor for each channel
	for (i = 0; i < numberOfChannels; i++)
	{
		descriptors[index].channel = i;
		descriptors[index].type = DAQI_CTR32;
		index++;
	}

	*scanDesriptorIndex = index;

	return err;
}
