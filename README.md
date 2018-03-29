## Universal Library for Linux
UL for Linux is a library used to access and control supported Measurement Computing DAQ devices over the Linux platform. The UL for Linux binary name is libuldaq.
 
### Prerequisites:
---------------

  1. C, C++ compilers and Make tool
  2. Development package for libusb
  
  The following describes how the prerequisites above can be installed on diffrent Linux distributions
  
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

### Build Instructions
---------------------

- Download and extract the latest version of the UL for Linux package

```
  $ wget https://github.com/sbazaz/uldaq/releases/download/v0.0.1-beta.9/libuldaq-0.0.1-b9.tar.bz2  
  
  $ tar -xvjf libuldaq-0.0.1-b9.tar.bz2
  
  $ cd libuldaq-0.0.1-b9
```
  
- Run the following commands to build and install the library

```
 $ ./configure & make
  
 $ sudo make install
```
  
- The C examples are located in the examples folder and ready to run.
  
  
