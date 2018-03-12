import os, json
from datetime import datetime
import urllib.request as urlLib

MOD_NAME = "cstrike"
ROOT_DIR = (os.curdir + "/__BUILD/")
AMXX_DIR_NAME = "amxmodx" 
#print("Current dir: " + ROOT_DIR)
COMPONENTS = "components.json"

def CheckFolders(dir):
	if not os.path.exists(dir):
		os.makedirs(dir)


components_file = open(COMPONENTS, mode = 'r')
json_data = json.load(components_file)
components_file.close()

def ReplaceAliases(str):
	str = str.replace("%root%", ROOT_DIR)
	str = str.replace("/%mod%", MOD_NAME)
	str = str.replace("%amxmodx%", AMXX_DIR_NAME)
	return str

def Log(str):
	print('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ']' + str)


def GetFile(url, directory, destinition):
	CheckFolders(directory)

	Log(' >> Starting donwload: "' + url + '"' )
	try:
		urlLib.urlretrieve(url, destinition)
	except urlLib.HTTPError as err:
		#print("URL: " + err.value + " error 404!")
		#print(" >> Download aborted! ERROR: " + err.msg)
		return
	
	
	Log(' >> Download Finished to file "' + destinition + '"')

#system = 'both'
system = 'linux' 
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
	config_path = "None"
	config_url = "None"

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
		#print(' -> [WARN]: Missing Key: "' + e.args[0] + '". Will be Skipped.')
		pass
	else:
		print(' > config_path = ' + config_path)
		print('  > config_url = ' + config_url)		