from uuid import uuid4
import platform
import re


def GeneratorDeviceIdWeb():
	return uuid4().hex

def ExractPID(response):
    pid = re.search(r'PID=([a-f0-9\-]+)', response)
    return pid.group(1)


def GeneratorDeviceIdApp():
	return str(uuid4())

def GetApiKey():
	return "1ccbc4c913bc4ce785a0a2de444aa0d6"

def VersionPlatform():
	return platform.release()

def UserAgent():
	return "okhttp/5.0.0-alpha.2"


