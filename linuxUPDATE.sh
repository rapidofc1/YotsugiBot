#!/bin/sh
echo ""
echo ""
echo ""
echo "Downloading Yotsugi....."
curl -L https://raw.githubusercontent.com/Kyousei/YotsugiBotLinuxTest/master/testfile.sh | sh
echo ""
echo "Downloaded!"
python3 YotsugiMain.py
