from gpiozero import LED, LEDBoard, Button
from time import sleep, time
from signal import pause
import os
import logging
import datetime
import configparser
import requests
import re
import subprocess
import sys
import csv

led = LED(20)
btn = Button(21)
pwr = LED(6)
sd_enable = LED(12)
sd_control = LEDBoard(13,16,19)

timestamp = datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')

script_basedir = '/home/pi/stericonnectSDIO/'

log_file_path = 'logs/'
log_file_name = 'stericonnect_'+timestamp+'.log'
log_file = script_basedir + log_file_path + log_file_name

logging.basicConfig(filename=log_file, filemode='w', format='%(asctime)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S', level=logging.DEBUG)

configfile_name = 'config.ini'
config = configparser.ConfigParser()
config.read(script_basedir + configfile_name)

sd_path = ''
fileKeeper = script_basedir + 'syncedFiles.csv'

hardware_id = config.get('SYSTEM', 'HardwareID')
config_url = config.get('STORAGE', 'URL')

def run(cmd):
    proc = subprocess.Popen(cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
    )
    stdout, stderr = proc.communicate()
 
    return proc.returncode, stdout, stderr

def runCommand(cmd, shouldLog = True):
	if shouldLog:
		logging.info('>COMMAND :: %s', cmd)
	
	cmd = cmd.split(' ')
	code, out, err = run(cmd)
	
	if shouldLog:
		logging.info('-->EXIT CODE :: %s', code)

		if code == 0:
			logging.info('-->OUTPUT :: %s', out.decode('UTF-8'))
		else:
			logging.info('-->ERROR :: %s', err.decode('UTF-8'))
	
	return code, out

def turn_on():
	sd_enable.off()
	sleep(1)
	pwr.off()
	sleep(1)
	sd_control.on()
	sleep(1)
	pwr.on()
	sleep(1)
	sd_enable.on()
	sleep(1)
	logging.info('STERICONNECT :: Disconnected from Data Logger')
	logging.info('STERICONNECT :: Connected to RPi')

def turn_off():
	sd_enable.off()
	sleep(1)
	pwr.off()
	sleep(1)
	sd_control.off()
	sleep(1)
	sd_enable.on()
	sleep(1)
	pwr.on()
	sleep(1)
	logging.info('STERICONNECT -- Disconnected from RPi')
	logging.info('STERICONNECT -- Connected to Data Logger')

def mountSD():
	logging.info('Mounting SD Card')
	global sd_path
	
	mountTimeout = 5
	startTime = time()
	while True:
		code, path = runCommand(script_basedir + 'getMountPoint.sh', False)
		if code != 0:
			status = False
		else:
			status = True
			sd_path = path.decode('UTF-8').replace('\n', '')
			sd_path += '/'
			logging.info('SD Mount Point -- %s', sd_path)
			break
		
		if time()-startTime > mountTimeout:
			break
	return status

def syncFiles():
	logging.info('Syncing Files')
	
	logging.info('Getting Pi Config')

	payload = {
		'macAddress' : hardware_id,
		'password': 'admin'
	}

	try:
		response = requests.request('POST', config_url, data = payload)
		jsonResponse = response.json()

		storage_url = jsonResponse['uploadUrl']
		logging.info('>CONFIG : Storage URL :: %s', storage_url)

		dataDir = jsonResponse['dir']
		logging.info('>CONFIG : Directory :: %s', dataDir)
		
		logging.info('Initiating File Upload')
			
		payload = {
			'macAddress' : hardware_id,
			'platform' : 'pi'
		}

		path_to_files  = sd_path + dataDir
		runCommand('ls -lrth ' + path_to_files)

		for (path, subdirs, filenames) in os.walk(path_to_files):
			for filename in filenames:
				filePath = os.path.join(path, filename)
				logging.info('Processing [ %s ]', filePath)
				if not isSynced(filePath):
					try:
						files = {'file':(filename, open(filePath, 'rb'), 'multipart/form-data')}
						response = requests.request('POST', storage_url, data = payload, files = files)	
						jsonResponse = response.json()
						
						if not "error" in jsonResponse:
							saveFile(filePath)
						else:
							logging.error("-- SKIPPING FILE DUE TO SERVER ERROR --")
						
						logging.info('Processing Complete. Response :: %s', jsonResponse)
					except Exception as e:				
						logging.error('Failed to upload file %s due to error: %s', filePath, str(e))
				else:
					logging.info('File already uploaded')
		
		logging.info('Uploading Files Complete')

	except Exception as e:
		logging.error('Failed to get Pi Config for HW ID %s due to error: %s', hardware_id, str(e))

	logging.info('Syncing Complete')

def saveFile(fileName):
	data = None

	with open(fileKeeper, 'r') as file:
		reader = csv.reader(file)
		data = list(reader)
	
	data.append([fileName, time()])

	with open(fileKeeper, 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerows(data)

def isSynced(fileName):
	status = False
	with open(fileKeeper, 'r') as file:
		reader = csv.reader(file)
		for row in reader:
			if row[0]==fileName:
				status=True
	return status

def unmountSD():
	logging.info('Unmounting SD Card from %s', sd_path)
	runCommand('sudo umount ' + sd_path)

def buttonRoutine():
	logging.info('********** Entering Button Subroutine')
	
	looptimes = 10
	mountSuccess = False

	led.on()
	while looptimes and not mountSuccess:
		logging.debug("====== Mount Attempt -- %s ======", looptimes)
		turn_on()
		sleep(2)
		status = mountSD()
		if status:
			mountSuccess = True
			syncFiles()
			sleep(1)
			unmountSD()
			sleep(2)
		else:
			logging.error('---- SD Card could not be mounted ----')
		turn_off()
		sleep(2)
		looptimes -= 1
	led.off()
	logging.info('Exiting Button Subroutine **********')

def init():
	global hardware_id
	
	# Keep SD Card Disabled
	sd_enable.off()
	pwr.off()

	logging.info('Initializing System')
	led.on()
	
	os.chdir(script_basedir)

	if hardware_id == 'ERROR000000000' :
		logging.error('Invalid Hardware ID')
	else:
		logging.info('HW ID '+hardware_id)
	turn_on()
	led.off()
	logging.info('Initialized System')

init()
while True:
	btn.wait_for_press()
	buttonRoutine()
