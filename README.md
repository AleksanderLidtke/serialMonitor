Overview
=========

This is a graphical interface program that allows the user to communicate with a
microcontroller or other piece of hardware via a serial port. It provides:

- a simple output window that contains all of the information being routed through the serial port,
- a text box that allows the user to type in an arbitrary command and send it through serial by pressing return,
- a drop-down menu used to select the serial port,
- a button used to update the list of available ports (e.g. after resetting the physical connection),
- text boxes used to update the refresh rate of the GUI and the connection Baud rate,
- ability to display hex codes of the received bytes instead of their Unicode representations,
- logging facilities that can record the data received over serial port into a file,
- menu to edit advanced serial port properties (parity bits, byte lengths etc.).

Usage
======

Installation
-------------

There are the two options to use the SerialMonitor:

- install using pip and run from Python or an entry-point script,
- run directly from source by importing the SerialMonitor module and calling main()

Pip is, by far, the easiest option that should also install all the dependencies
for you. In order to install with pip, just download the newest ``tar.gz``
distribution, and run:
```pip3 install SerialMonitor--X.Y.Z.tar.gz```
On Linux, you might need to prepend ```sudo -H``` to the pip call in order allow
pip to install in write-protected directories. On Windows, you need to prepend
```python -m``` and possibly start the command line as an administrator.

Prerequisites
--------------

SerialMonitor requires wxWidgets 4.0.1 or newer. Installing with pip should
install the newest version of wxWidgets. However, pip might struggle to install
all the wxWidgets dependencies (see `this post
<https://github.com/wxWidgets/Phoenix/issues/465>`_),
so these have to be installed by hand. A complete list of dependencies can be
found `here
<https://github.com/wxWidgets/Phoenix/issues/465>`_. Installing the
following dependencies worked on Ubuntu 16 (pip successfully installed the
SerialMonitor and the newest wxWidgets afterwards):

```	apt-get install libgtk-3-dev libgstreamer-plugins-base0.10-dev libwebkit-dev libwebkitgtk-3.0-dev```

If all else fails, install the above mentioned dependencies manually. Then,
wxWidgets and other Python dependencies can be installed with pip individually
as well:

```sudo pip3 install pySerial```

```sudo pip3 install wxPython```

Running
--------

If you install with pip on Ubuntu, an entry-point script will be automatically
installed in ``/usr/local/bin/serialMonitor`` and added to the ``PATH``.
So simply typing ``serialMonitor`` in the command line will launch it. If the
script doesn't work (I don't know where it'll be located on Windows or OSX...),
you can run the monitor from Python terminal (or put the call in a script yourself):

>>> import SerialMonitor
>>> SerialMonitor.main()

There is a script ```runSerialMonitor``` provided which does exactly the above.

Tested on Ubuntu Ubuntu 16.04 with Python 3.5.2.

GUI maintenance
================
The GUI was originally built with `wxFormbuilder 3.5.1
<https://github.com/wxFormBuilder/wxFormBuilder>`_.
It did not support the newest wxWidgets (wx4), so exporting the code from the
form builder 3.5.1 or older would break the GUI.

wxFormBuilder 3.8.1 does allow exporting the project to Python code, and this is
what has been used to generate the GUI for the current release. Unfortunately,
this form builder had to be built from source. Here are some helpful hints
on building the most recent wxFormBuilder 3.8.1 (good luck):

- Added '''#define __GXX_ABI_VERSION 1002''' in src/maingui.h to avoid conflicts between
    wxWidgets versions (<https://github.com/eranif/codelite/issues/825>).
- Changed '''wxFALLTHROUGH''' to '''[[fallthrough]]''' in src/utils/typeconv.cpp
    to fix more wxWidgets compatibility issues.
- Updated GNU C++ compiler to ensure C++14 compatibility (gcc 6.4.0).
- Had to use '''git submodule update --init''' to fix ticpp.h file being missing.

Example
========

![Alt text](screenshot.png?raw=true "Main window of the program")
