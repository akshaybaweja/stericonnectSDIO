import os
import configparser
import csv

print("Entering SETUP Mode")

script_basedir = '/home/pi/stericonnectSDIO/'
media_path = 'media/'
sd_path = media_path + 'usb/'
log_folder = 'logs/'

configfile_name = script_basedir + "config.ini"
fileKeeper = script_basedir + "syncedFiles.csv"

def getSerial():
  # Extract serial from cpuinfo file
  cpuserial = "0000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[10:26]
    f.close()
  except:
    cpuserial = "ERROR000000000"

  return cpuserial

os.chdir(script_basedir)
os.system("git pull")
    
if(not os.path.isdir(log_folder)):
	print(">SYSTEM: Creating Log Folder")
	os.mkdir(log_folder)
	os.system("sudo chown -R pi:pi " + log_folder)
	print(">SYSTEM: Created Log Folder")

Config = configparser.ConfigParser()
Config["STORAGE"] = {}
Config["STORAGE"]["URL"] = 'https://us-central1-sterilwize.cloudfunctions.net/getPiConfig'
Config["SYSTEM"] = {}
Config["SYSTEM"]["HardwareID"] = getSerial()

if(not os.path.isfile(configfile_name)):
  with open(configfile_name, 'w') as configfile:
	  Config.write(configfile)

if(not os.path.isfile(fileKeeper)):
  with open(fileKeeper, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(["fileName", "timeStamp"])

print("Exiting SETUP Mode")
