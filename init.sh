echo "Initializing STERICONNECT v3.2..."
python3 /home/pi/stericonnectSDIO/setup.py

echo "Installing WiFi Driver for USB WIFI Module..."
sudo bash /home/pi/stericonnectSDIO/install_wifi_driver.sh
echo "USB WiFi Driver Install Complete"

echo "Setting up Services and Routines..."
sudo chmod a+x /home/pi/stericonnectSDIO/getMountPoint.sh

sudo cp stericonnectSDIO/stericonnect.service /lib/systemd/system/stericonnect.service
sudo chmod 644 /lib/systemd/system/stericonnect.service
sudo systemctl daemon-reload

sudo cp stericonnectSDIO/stericonnectlogs.service /lib/systemd/system/stericonnectlogs.service
sudo chmod 644 /lib/systemd/system/stericonnectlogs.service

sudo systemctl daemon-reload
sudo systemctl enable stericonnectlogs.service
sudo systemctl enable stericonnect.service
echo "Service and Routine Setup Complete"

sudo echo -en "\n\ndtoverlay=sdio,poll_once=off" >> /boot/config.txt

echo "Rebooting Raspberry Pi..."
sleep 1 && sudo reboot