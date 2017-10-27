#!/bin/sh
echo "Welcome to Yotsugi Bot launcher for WINDOWS!"
echo ""
echo "  Choose what you would like to do below!"


choice=4
		echo "1-- Download (Downloads and installs prereqs)"
		echo "2-- Update"
		echo "3-- Start"
		echo "4-- Exit"
		echo -n "IMPORTANT NOTE: When updating, copy 'credentials.py' and paste them somewhere safe, then delete the 'YotsugiBot' folder!"
	
while [ $choice -eq 4 ]; do
read choice
if [ $choice -eq 1 ] ; then
    echo "Selected 1; Download Yotsugi! (Downloads and installs prereqs)"
    echo "Running..."
    curl -L https://raw.githubusercontent.com/Kyousei/YotsugiBotWindows/master/download.sh | sh
	echo "Installing Prereqs...!"
	sleep 2
	curl -L https://raw.githubusercontent.com/Kyousei/YotsugiBotWindows/master/prereqs.sh | sh
	echo ""
    echo "//////////////////////////"
    echo "Finished!"
else
    if [ $choice -eq 2 ] ; then
        echo "Selected 2; Update Yotsugi"
        echo "Running..."
        echo "Downloading updates...."
        curl -L https://raw.githubusercontent.com/Kyousei/YotsugiBotWindows/master/download.sh | sh
		echo ""
else
    if [ $choice -eq 3 ] ; then
        echo "Selected 3; Starting Yotsugi"
        echo "Running..."
        python YotsugiMain.py
        echo "//////////////////////////"
        echo "Finished!"
else
    if [ $choice -eq 4 ] ; then
        echo "Selected 4; Closing the launcher!"
        echo ""
        echo "//////////////////////////"
        fi
      fi
    fi
  fi
done
exit 0
