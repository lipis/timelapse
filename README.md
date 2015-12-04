Timelapse (PSS Camera)
======================

Working on OS X, Windows, Linux, Raspberry Pi and possibly on anything that has
a camera and can run Python.

Download and Run
----------------

Visit the [download](https://pss-camera.appspot.com/download/) page and get the
binaries for OS X or Windows.

Installation
------------

```bash
$ pip install -r requirements.txt
```

Capture
-------

```bash
$ ./pss-capture.py --interval 30 --name foo
```

The above command will start saving images every 30 seconds in the directory
`feed/foo`. For more information just use `--help`.


Upload
------

```bash
$ ./pss-upload.py --username username --password password
```

The above command will start uploading the images that are located in `feed`
directory to [PSS Camera](https://pss-camera.appspot.com). For more information
just use `--help`.

Set your password from the [profile settigs](https://pss-camera.appspot.com/profile/).

Requirements
------------

- [OpenCV](http://opencv.org/) — if you want to play with the source and you
  don't have a Raspberry Pi.
- [Camera Pi Module](https://www.raspberrypi.org/products/camera-module/) —
  which is using the [Picamera](https://github.com/waveform80/picamera) if you
  are on Raspberry Pi.
- [fswebcam](https://github.com/fsphil/fswebcam) — if you don't want to install
  OpenCV on your Raspberry Pi and you have a USB camera attached to it.

Examples
--------

- [Clouds](https://pss-camera.appspot.com/lipis/clouds/)
- [Green Plant](https://pss-camera.appspot.com/lipis/green-plant/)
