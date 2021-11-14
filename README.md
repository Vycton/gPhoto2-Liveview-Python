# gPhoto2-Liveview-Python
Demo of gPhoto2 live view in python.
Adapted from [aqiank/gphoto2-liveview-example](https://github.com/aqiank/gphoto2-liveview-example)

Requirements
------------
1. [gPhoto2](http://www.gphoto.org/proj/gphoto2)
1. [Python 3](https://www.python.org/downloads/)
1. [tkinter](https://docs.python.org/3/library/tkinter.html)
1. [pillow](https://pillow.readthedocs.io/en/stable/)
1. DSLR Camera

Use
-----
1. Download liveview.py and navigate to its directory
1. Plug in a USB connector from your camera to your computer
1. run `gphoto2 --capture-movie --stdout | python liveview.py`

Explanation
------
`gphoto2 --capture-movie --stdout` will spit out a byte stream of jpegs, where each jpeg is delimited by a start code `\xff\xd8` and a stop code `\xff\xd9`. 
All there is to creating a frame of the liveview is reading what's in between those codes and displaying it as a jpeg to the screen. Do that repeatedly and you have a liveview. `liveview.py` does the reading and displaying in two separate threads to increase speed, but this might be unnecessary depending on your camera and computer.
