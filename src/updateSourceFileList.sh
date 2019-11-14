#!/bin/bash
rm -f ./Makefile.am

exec > ./Makefile.am
exec 2>&1
echo "AUTOMAKE_OPTIONS = subdir-objects

lib_LTLIBRARIES = libuldaq.la"
echo -n "libuldaq_la_SOURCES = "
fileList=$(find . -type f \( -name "*.cpp" -o -name "*.c" -o -name "*.h" \) -printf "%p \n" 2>&1 | grep -v "warning" | grep -v "ul.h" | sed 's|./||')
echo $fileList
echo "
libuldaq_la_LDFLAGS = \$(LTLDFLAGS)

include_HEADERS = uldaq.h
"

