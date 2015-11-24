import os
import commands

def list_devices():
	status, output = commands.getstatusoutput("adb devices")
	if status != 0:
		return []
	else:
		return [l.split("\t")[0] for l in output.splitlines() if "\tdevice" in l]

def start_appium_for_device(device):
	# kill existing appium
	status, output = commands.getstatusoutput("pkill -f appium")
	os.system("appium -U {} &".format(device))
