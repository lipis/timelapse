#! /bin/bash

rm -rf build dist
pyinstaller pss-capture.py --onefile --hidden-import=numpy --hidden-import=cv2
pyinstaller pss-upload.py --onefile
rm -rf build
rm pss-capture.spec pss-upload.spec
