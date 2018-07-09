#python script to automate the dump process
import os
import time
import telnetlib
import socket
import sys
import subprocess
import signal 
import serial

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


HOST = "localhost"
PORT = "4444"

file = open("octo_log.txt", "r+")
command = "dump_arm 0x0136AB40 10000\n" #hardcode here the first command to send to openocd
print bcolors.HEADER + bcolors.BOLD + "Starting dump : " + command + bcolors.ENDC + bcolors.ENDC
pro = subprocess.Popen("openocd -f jtagkey2.cfg -f sta8090fgbd.cfg", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid) #open a shell and launch openocd 
ser = serial.Serial('/dev/ttyUSB0', 9600) #open serial connection to Arduino
time.sleep(2) #wait for openocd initial setup
tn = telnetlib.Telnet(HOST,PORT) #open Telnet connection

tn.read_until("\n",1)
tn.read_until("\n",1) #remove the first two lines printed by openocd
tn.write(command) #send command
time.sleep(2)

count = 0 

while(True):
	line1 = file.readline() #read status line from the log file
	line2 = file.readline() #read command line from the log file
	if("dump_arm" in line2) :
		comment = line1
		command = line2
	
	if ("DEAD" in line1 or "Everything" in line1) :
		count = 0
		print bcolors.OKBLUE + command + bcolors.ENDC
		ser.write('g') #tell Arduino a hard reset is needed
		print bcolors.WARNING + "PYTHON > Switching off power supply" + bcolors.ENDC
		tn.close() #close telnet connection
		os.killpg(os.getpgid(pro.pid), signal.SIGTERM) #kill openocd shell
		while(ser.read()!='k'): #wait for Arduino ack
			print bcolors.WARNING + "PYTHON > Waiting for Arduino ACK" + bcolors.ENDC
			time.sleep(1)
		time.sleep(2) #wait for the board powerup
		pro = subprocess.Popen("openocd -f jtagkey2.cfg -f sta8090fgbd.cfg", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid) 
		time.sleep(2)
		tn = telnetlib.Telnet(HOST, PORT) #open again telnet connection
		tn.read_until("\n",1)
		tn.read_until("\n",1)
		tn.write(command)
		time.sleep(2)
		file.seek(0) 

	else: #monitors the log file
		count = count + 1
		if(count == 1000) :
			count = 0
			print bcolors.OKBLUE + command + bcolors.ENDC
			ser.write('g') #tell Arduino a hard reset is needed
			print bcolors.WARNING + "PYTHON > Switching off power supply" + bcolors.ENDC
			tn.close() #close telnet connection
			os.killpg(os.getpgid(pro.pid), signal.SIGTERM) #kill openocd shell
			while(ser.read()!='k'): #wait for Arduino ack
				print bcolors.WARNING + "PYTHON > Waiting for Arduino ACK" + bcolors.ENDC
				time.sleep(1)
			time.sleep(2) #wait for the board powerup
			pro = subprocess.Popen("openocd -f jtagkey2.cfg -f sta8090fgbd.cfg", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid) 
			time.sleep(2)
			tn = telnetlib.Telnet(HOST, PORT) #open again telnet connection
			tn.read_until("\n",1)
			tn.read_until("\n",1)
			tn.write(command)
			time.sleep(2)
			file.seek(0) 

		else :
			print bcolors.OKGREEN + "PYTHON > Seems good." + bcolors.ENDC
			time.sleep(2)

file.close()
