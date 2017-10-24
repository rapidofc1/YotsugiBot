echo "Reboot initiated.."
sleep 5
echo "Killed the bot. Welcome to the 'after-reboot' menu!"
echo "Please select what you'd like to do."


choice=2
		echo "1-  Reboot"
		echo "2-  Exit"
		
while [ $choice -eq 2 ]; do
read choice
if [ $choice -eq 1 ] ; then
		echo "Reboot selected!"
		sleep 1
		echo "Rebooting..."
		bash linuxRUN.sh
	fi
done
exit 0