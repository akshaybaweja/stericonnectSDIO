import os
import configparser
import csv

print("Entering SETUP Mode")

script_basedir = '/home/pi/stericonnect/'
media_path = 'media/'
sd_path = media_path + 'usb/'
log_folder = 'logs/'

configfile_name = "config.ini"
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

# if(not os.path.isdir(sd_path)):
# 	print(">SYSTEM: Creating Mount Point")
# 	os.mkdir(media_path)
# 	os.mkdir(sd_path)
# 	os.system("sudo chown -R pi:pi " + sd_path)
# 	print(">SYSTEM: Created Mount Point")
    
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