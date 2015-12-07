Timelapse (PSS Camera)
======================

Working on OS X, Windows, Linux, Raspberry Pi and possibly on anything that has
a camera and can run Python.

## :fire: Download and Run

Visit the [download](https://pss-camera.appspot.com/download/) page and get the
binaries for OS X or Windows.

## :pray: Installation


```bash
$ pip install -r requirements.txt
```

## :camera: Capture

```bash
$ ./pss-capture.py --interval 30 --name foo
```

The above command will start saving images every 30 seconds in the directory
`feed/foo`. For more information just use `--help`.


## :cloud: Upload


```bash
$ ./pss-upload.py --username username --password password
```

The above command will start uploading the images that are located in `feed`
directory to [PSS Camera](https://pss-camera.appspot.com). For more information
just use `--help`.

Set your password from the [profile settigs](https://pss-camera.appspot.com/profile/).

## :briefcase: Requirements

- [OpenCV](http://opencv.org/) — if you want to play with the source and you
  don't have a Raspberry Pi.
- [Camera Pi Module](https://www.raspberrypi.org/products/camera-module/) —
  which is using the [Picamera](https://github.com/waveform80/picamera) if you
  are on Raspberry Pi.
- [fswebcam](https://github.com/fsphil/fswebcam) — if you don't want to install
  OpenCV on your Raspberry Pi and you have a USB camera attached to it.

## :rose: Examples

- [Clouds](https://pss-camera.appspot.com/lipis/clouds/)
- [Green Plant](https://pss-camera.appspot.com/lipis/green-plant/)
- [Orchidaceae](https://pss-camera.appspot.com/lipis/orchidaceae/)

## :euro: Recommended Raspberry Pi Setup
- [Raspberry Pi 2 & 8GB MicroSD](http://www.modmypi.com/raspberry-pi/rpi2-model-b/raspberry-pi-2-model-b-new-and-8gb-microsd-card-bundle) — £33.99
- [Nwazet Pi Camera Box](http://www.modmypi.com/raspberry-pi/camera/nwazet-pi-camera-box-bundle-case,-lens-and-wall-mount-b-plus) — £23.99
- [Camera Board](http://www.modmypi.com/raspberry-pi/camera/raspberry-pi-camera-board-5mp-1080p-v1.3) — £12.99
- [WiFi Dongle](http://www.modmypi.com/raspberry-pi/accessories/wifi-dongles/wifi-dongle-nano-usb) — £5.99
