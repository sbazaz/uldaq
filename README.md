## Universal Library for Linux
A library which allows applications to interface with Measurement Computing DAQ devices on Linux and Mac OS X
 
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
  - Red Hat-based Linux distributions as Fedora, CentOS
  
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
  $ wget https://github.com/sbazaz/uldaq/releases/download/vx.x.x/libuldaq-x.x.x.tar.bz2  
  
  $ tar -xvjf libuldaq-x.x.x.tar.bz2
  
  $ cd libuldaq-x.x.x
```
  
- Run the following commands to build and install the library

```
 $ ./configure & make
  
 $ sudo make install
```
  
- The C examples are located in the examples folder and ready to run.
  
  
