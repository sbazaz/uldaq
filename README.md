# Universal Library for Linux
A library which allows applications to interface with Masurement Computing DAQ devices on Linux and Mac OS X
 
Prerequisites:
---------------

  - C, C++ compilers and Make tool
  - Development package for libusb
  
  The following describes how above prerequisites can be installed on diffrent Linux distributions
  
  - Debian-based Linux distributions such as Ubuntu, Raspbian
  
    - $ sudo apt-get install gcc g++ make
    - $ sudo apt-get install libusb-1.0-0-dev

  - Red Hat-based Linux distributions as Fedora, CentOS
  
    - $sudo yum install gcc gcc-c++ make
    - $sudo yum install libusbx-devel
    
  - OpenSUSE 
  
    - $sudo zypper install gcc gcc-c++ make
    - $sudo zypper install libusb-devel

Build Instructions
===================

- Download the latest version of the package

  wget https://github.com/sbazaz/uldaq/releases/latest
  
- Extract the downloaded tar file
  
  tar -xvjf libuldaq-x.x.x.tar.bz2
  
- Change the folder
  
  cd libuldaq-x.x.x
  
- Run the following commands to build and install the library

   ./configure & make
  
   sudo make install
  
- The examples are located in the examples folder and ready to run.
  
  
