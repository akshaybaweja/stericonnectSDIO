python3 /home/pi/stericonnect/setup.py

sudo chmod a+x /home/pi/stericonnect/getMountPoint.sh
sudo chmod a+x /home/pi/stericonnect/manMount.sh
sudo chmod a+x /home/pi/stericonnect/usbPowerOFF.sh
sudo chmod a+x /home/pi/stericonnect/usbPowerON.sh

sudo cp stericonnect/stericonnect.service /lib/systemd/system/stericonnect.service
sudo chmod 644 /lib/systemd/system/stericonnect.service
sudo systemctl daemon-reload

sudo cp stericonnect/stericonnectlogs.service /lib/systemd/system/stericonnectlogs.service
sudo chmod 644 /lib/systemd/system/stericonnectlogs.service

sudo systemctl daemon-reload
sudo systemctl enable stericonnectlogs.service
sudo systemctl enable stericonnect.service

sudo reboot