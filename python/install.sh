#!/bin/bash

haveProg() {
    [ -x "$(which $1)" ]
}

# Determine the package manager to use
if haveProg apt ; then
	PKGMNGR="apt"
elif haveProg apt-get ; then
	PKGMNGR="apt-get"
elif haveProg yum ; then
	PKGMNGR="yum"
elif haveProg dnf ; then
	PKGMNGR="dnf"
elif haveProg zypper ; then
	PKGMNGR="zypper"
elif haveProg packman ; then
	PKGMNGR="packman"
else
	PKGMNGR=""
fi

# Install the Python package
if [ $(which python | wc -l) -ne 0 ]; then
    if [ $(python -m pip --version 2>/dev/null | wc -l) -ne 0 ]; then
            if [ "$PKGMNGR" = "packman" ]; then
                $PKGMNGR -S python2-pip
            else
                $PKGMNGR install python-pip
            fi
    fi
    if [ $(python -m pip --version 2>/dev/null | wc -l) -ne 0 ]; then
        echo "Installing library for Python 2"
        python -m pip install setuptools
        python -m pip install --upgrade pip setuptools
        python setup.py install --record python2_files.txt
    fi
    echo
fi

if [ $(which python3 | wc -l) -ne 0 ]; then
    if [ $(python3 -m pip --version 2>/dev/null | wc -l) -ne 0 ]; then
        if [ ! -z "$PKGMNGR" ]; then
            if [ "$PKGMNGR" = "packman" ]; then
                $PKGMNGR -S python-pip
            else
                $PKGMNGR install python3-pip
            fi
        fi
    fi
    if [ $(python3 -m pip --version 2>/dev/null | wc -l) -ne 0 ]; then
        echo "Installing library for Python 3"
        python3 -m pip install setuptools
        python3 -m pip install --upgrade pip setuptools
        python3 setup.py install --record python3_files.txt
        echo
    fi
fi

echo "uldaq Python API install complete."
