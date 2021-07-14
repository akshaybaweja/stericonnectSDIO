# SteriConnect

## Flashing Raspberry Pi's SD Card
1. Download and Install [Raspberry Pi Imager](https://www.raspberrypi.org/software/)
2. Follow [this 40 second video tutorial on how to flash OS on SD Card](https://www.youtube.com/watch?v=J024soVgEeM)

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
```
login as: pi
password: raspberry
```

## Configure Raspberry Pi
```
sudo raspi-config
```
* Select ```System Options```
* Select ```Network at Boot```
* Select ```Yes```

## Install [WiFi Driver for USB Module](./usbdriver.md)
Click above link and follow the steps. Once done continue below steps.

## Install Firmware
```
git clone https://github.com/akshaybaweja/stericonnectSDIO
```
### For Production Mode
```
bash stericonnectSDIO/init.sh
```

To change server - login to Raspberry Pi via SSH

```
sudo nano stericonnectSDIO/config.ini
```

Under section ```Storage```, replace ```URL``` with server address you wish to add.

## Access Log Files
Goto ```<ip-address>:8000``` to access logs for the stericonnect

## Debug
### Find Process ID
```
ps aux | grep /home/pi/sterionnect/ 
```
### View System Logs
```
sudo journalctl -u stericonnect
```
```
sudo journalctl -u stericonnectlogs
```