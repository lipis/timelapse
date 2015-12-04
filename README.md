Timelapse (PSS Camera)
======================

Working on OS X, Windows, Linux, Raspberry Pi and possibly on anything that has a camera and can run Python.

Download and Run
----------------

Visit the [download](https://pss-camera.appspot.com/download/) page and get the binaries for OS X or Windows.


Installation
------------

```bash
$ pip install -r requirements.txt
```

Capture
-------

```bash
$ ./pss-capture.py --camera -1 --interval 4 --name foo
```

Upload
------

```bash
$ ./pss-upload.py --username username --password password
```

Set your password from the [profile settigs](https://pss-camera.appspot.com/profile/).


Examples
--------

- [Clouds](https://pss-camera.appspot.com/lipis/clouds/)
- [Green Plant](https://pss-camera.appspot.com/lipis/green-plant/)
