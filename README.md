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
     $ wget https://github.com/sbazaz/uldaq/releases/download/v0.0.1-beta.13/libuldaq-0.0.1-b13.tar.bz2
  
  MacOS
     $ curl -L -O https://github.com/sbazaz/uldaq/releases/download/v0.0.1-beta.13/libuldaq-0.0.1-b13.tar.bz2
``` 
2. Extract the tar file:
 
```
  $ tar -xvjf libuldaq-0.0.1-b13.tar.bz2
```
  
3. Run the following commands to build and install the library:

```
  $ cd libuldaq-0.0.1-b13
  $ ./configure && make
  $ sudo make install
```
  
4. Run the C examples, which are located in the examples folder:

```
  $ cd examples
  $ ./AIn
```

### Python interface for UL for Linux
---------------------
- Follow the build [instructions](#build-instructions) above, then go to https://pypi.org/project/uldaq/ to install the Python interface and examples.
 
