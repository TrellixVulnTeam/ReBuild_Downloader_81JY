import os
import json
from datetime import datetime
import urllib.request

MOD_NAME = "cstrike"
ROOT_DIR = (os.curdir + "/__BUILD/")
AMXX_DIR_NAME = "amxmodx" 
#print("Current dir: " + ROOT_DIR)
COMPONENTS = "components.json"

def CheckFolders(dir):
	if not os.path.exists(dir):
		os.makedirs(dir)

with open(COMPONENTS, mode = 'r') as components_file:
	json_data = json.load(components_file)

def ReplaceAliases(str):
	str = str.replace("%root%", ROOT_DIR)
	str = str.replace("/%mod%", MOD_NAME)
	str = str.replace("%amxmodx%", AMXX_DIR_NAME)
	return str

Log = lambda str: print('[' + datetime.now().strftime('%H:%M:%S') + ']' + str)
toFixed = lambda numObj, digits: f"{numObj:.{digits}f}"


def GetFile(url, directory, destinition):
	CheckFolders(directory)

	Log(' >> Starting donwload: "' + url + '"' )
	try:
		header = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64)' }
		req = urllib.request.Request(url, headers=header)
		response = urllib.request.urlopen(req)

		# urllib.request.urlretrieve(url, destinition)

		with open(destinition,'wb') as output:
  			output.write(response.read())

	except urllib.request.HTTPError as err:
		print(" >> Download aborted! ERROR: " + err.msg)
		return

	Log(' >> Download Finished to file "' + destinition + '"')


# system = 'both'
# system = 'linux'
system = 'win32'

def DownloadPackage():

	print("  >Used system == " + system)

	system_list = []
	if(system == 'win32'):
		system_list.append('win32')
	elif(system == 'linux'):
		system_list.append('linux')
	else:
		system_list.append('win32')
		system_list.append('linux')

	counter = 0
	for component in json_data:
		counter += 1
		print(str(counter) + '. ' + component['name'])
		dir = ReplaceAliases(str(component['binary_path']))

	# if component['name'] != "AmxModX-dev-1.8.3":
		# continue


	# binary download
		for item in system_list:
			url = component[item]['url']
			bin_name = component[item]['bin_name']
			destinition = (dir + bin_name)
			GetFile(url, dir, destinition)

	# configs & additionals download
		try:
			config_path = ReplaceAliases(str(component['config']['path']))
			config_url = ReplaceAliases(str(component['config']['url']))

			config_name = os.path.basename(config_url)
			destinition = (config_path + config_name)
			GetFile(config_url, config_path, destinition)

		except KeyError as e:
			# print(' -> [WARN]: Missing Key: "' + e.args[0] + '". Will be Skipped.')
			pass
		else:
			print(' > config_path = ' + config_path)
			print('  > config_url = ' + config_url)

if __name__ == "__main__":
	DownloadPackage()