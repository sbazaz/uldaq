## Universal Library for Linux
UL for Linux is a library used to access and control supported Measurement Computing DAQ devices over the Linux platform. The UL for Linux binary name is libuldaq.
 
### Prerequisites:
---------------

  - C, C++ compilers and Make tool
  - Development package for libusb
  
  The following describes how the prerequisites above can be installed on different Linux distributions
  
  - Debian-based Linux distributions such as Ubuntu, Raspbian
  
  ```
     $ sudo apt-get install gcc g++ make
     $ sudo apt-get install libusb-1.0-0-dev
  ```
  - Red Hat-based Linux distributions such as Fedora, CentOS
  
  ```
     $ sudo yum install gcc gcc-c++ make
     $ sudo yum install libusbx-devel
  ```
     
  - OpenSUSE 
  
  ```
     $ sudo zypper install gcc gcc-c++ make
     $ sudo zypper install libusb-devel
  ```
  
  - MacOS (Version 10.11 or later recommended)
  
  ```
     $ xcode-select --install
     $ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
     $ brew install libusb
  ```

### Build Instructions
---------------------

1. Download the latest version of the UL for Linux package:

```
  Linux
     $ wget https://github.com/sbazaz/uldaq/releases/download/v0.0.1-beta.16/libuldaq-0.0.1-b16.tar.bz2
  
  MacOS
     $ curl -L -O https://github.com/sbazaz/uldaq/releases/download/v0.0.1-beta.16/libuldaq-0.0.1-b16.tar.bz2
``` 
2. Extract the tar file:
 
```
  $ tar -xvjf libuldaq-0.0.1-b16.tar.bz2
```
  
3. Run the following commands to build and install the library:

```
  $ cd libuldaq-0.0.1-b16
  $ ./configure && make
  $ sudo make install
```

Note: To install the Python interface, follow the above build [instructions](#build-instructions) then go to https://pypi.org/project/uldaq/ for further installation.
  
### Examples
Run the C examples, located in the examples folder, by entering the following commands 

```
  $ cd examples
  $ ./AIn
```
Refer to the uldaq [PyPI](https://pypi.org/project/uldaq/) page for instructions on installing Python examples.

### Usage
The following is a basic example of using the Universal Library for Linux to perform analog input. Further examples are available in the Examples folder.
```
#include <stdio.h>
#include "uldaq.h"

#define MAX_DEV_COUNT  100
#define MAX_STR_LENGTH 64

int main(void)
{
	unsigned int numDevs = MAX_DEV_COUNT;
	DaqDeviceDescriptor devDescriptors[MAX_DEV_COUNT];
	DaqDeviceHandle handle = 0;

	int chan = 0;
	double data = 0;
	UlError err = ERR_NO_ERROR;

	// Get descriptors for all of the available DAQ devices
	ulGetDaqDeviceInventory(ANY_IFC, devDescriptors, &numDevs);
	
	// verify at least one DAQ device is detected
	if (numDevs)
	{
		// get a handle to the DAQ device associated with the first descriptor
		handle = ulCreateDaqDevice(devDescriptors[0]);

		// check if the DAQ device handle is valid
		if (handle)
		{
			// establish a connection to the DAQ device
			err = ulConnectDaqDevice(handle);

			// read data for the first 4 analog input channels
			for (chan = 0; chan <= 3; chan++)
			{
				err = ulAIn(handle, chan, AI_SINGLE_ENDED, BIP5VOLTS, AIN_FF_DEFAULT, &data);

				printf("Channel(%d) Data: %10.6f\n", chan, data);
			}

			ulDisconnectDaqDevice(handle);
			ulReleaseDaqDevice(handle);
		}
	}

	return 0;
}
```
### Support/Feedback
The uldaq package is supported by MCC. For support for uldaq, contact technical support through ************. Please include detailed steps on how to reproduce the problem in your request.
