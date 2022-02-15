# SteriConnect

## Raspberry Pi Image Download
1. Get [this version of RaspiOS](https://downloads.raspberrypi.org/raspios_armhf/images/raspios_armhf-2021-05-28/2021-05-07-raspios-buster-armhf.zip)
2. Extract `.zip` file

## Flashing Raspberry Pi's SD Card
1. Download and Install [Raspberry Pi Imager](https://www.raspberrypi.org/software/)
2. Follow [this 40 second video tutorial on how to flash OS on SD Card](https://www.youtube.com/watch?v=J024soVgEeM)
3. Instead of choosing default OS select the image file downloaded in previous step.

## Setup
1. Remove and reinstert the SD Card
2. Copy files from ```pre-setup-files``` to Raspberry Pi's SD Card shown as ```boot```
3. edit ```wpa_supplicant.conf```
```
country=<Set Your Country Code. CA = Canada, US = USA, IN = India>
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
    ssid="<WIFI SSID>"
    psk="<WIFI PASSOWORD>"
}
```
4. Save the ```wpa_supplicant.conf```
5. Eject SD Card and insert back to Raspberry Pi

## Login to SSH
Find IP address of your pi using your router settings page and in terminal enter the following commands
```
ssh pi@<ip-address>
password: raspberry
```

## Configure Raspberry Pi
```
sudo raspi-config
```
* Select ```System Options```
* Select ```Network at Boot```
* Select ```Yes```
* Select ```Localization Options```
* Select ```Change Timezone```
* Select your Timezone
* Exit ```raspi-config```

## Install Firmware
```
git clone https://github.com/akshaybaweja/stericonnectSDIO
```

Connect TP-Link WiFi Module and run the following command

```
sudo bash stericonnectSDIO/init.sh
```

Once the boot is completed the IP address for raspberry pi might have changed. Get the new IP anddress and ssh into it. Once you've sshed to raspberry pi run

The system should be successfully configured at this point in time.

### To change server - login to Raspberry Pi via SSH
```
sudo nano stericonnectSDIO/config.ini
```
Under section ```Storage```, replace ```URL``` with server address you wish to add.

Reboot and the system should bee ready to use.

## Access Log Files
Goto ```<ip-address>:8000``` to access logs for the stericonnect

## Debug
### Find Process ID
```
ps aux | grep stericonnect 
```
### View System Logs
```
sudo journalctl -u stericonnect
```
```
sudo journalctl -u stericonnectlogs
```
