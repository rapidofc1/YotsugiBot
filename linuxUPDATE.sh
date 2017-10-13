#!/bin/sh
echo "Welcome to YotsugiBot installer!"
echo "	Please choose what you'd like to do below!"
echo ""
echo ""


choice=2
		echo "1. Download/Update Yotsugi"
		echo "2. Run Yotsugi"
	
while [ $choice -eq 2 ]; do
read choice
if [ $choice -eq 1 ] ; then

		echo ""
		echo "Downloading Yotsugi....."
		curl -L https://raw.githubusercontent.com/Kyousei/YotsugiBotLinuxTest/master/testfile.sh | sh
		echo ""
		echo "Downloaded!"
		
else

		if [ $choice -eq 2 ] ; then
		
			echo ""
			echo "Starting the bot..."
			echo ""
			bash linuxRUN.sh
		fi
	fi
done
exit 0
