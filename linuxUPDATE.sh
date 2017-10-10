#!/bin/sh
echo "Welcome to YotsugiBot installer!"
echo "	Please choose what you'd like to do below!"
echo ""
echo ""


choice=1
		echo "1. Download Yotsugi"
	
while [ $choice -eq 1 ]; do
read choice
if [ $choice -eq 1 ] ; then

		echo ""
		echo "Downloading Yotsugi....."
		curl -L https://raw.githubusercontent.com/Kyousei/YotsugiBotLinuxTest/master/testfile.sh | sh
		echo ""
		echo "Downloaded!"
		
	fi
done
exit 0