from datetime import datetime
from urllib.request import urlretrieve
import os, shutil, zipfile

temp_dir = '/__temp/'
Build_temp				= "Build_temp/"

ReHLDS_binary_path		= "bin/"
ReHLDS_engine_linux32	= "linux32/engine_i486.so"
ReHLDS_engine_win32		= "win32/swds.dll"

win32 = 0
linux32 = 1
both = 3

Build = (os.curdir + "/Build/")
if os.path.exists(Build):
	shutil.rmtree(Build)

def GetTime():
	return ('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ']')

class Component():
	"""This class will controlle our subject"""
	def __init__(self, url, name):
		self.url = url
		self.name = name

	def Get_info(self):
		description = (self.name + " URL=" + self.url).title()
		print(description)

	def GetDest(self):
		destinition = (os.curdir + temp_dir)

		if not os.path.exists(destinition):
			os.makedirs(destinition)

		return (destinition + self.name + ".zip")
	
	def Download(self):
		print(GetTime() + ' >> LOG: Starting donwload: "' + self.url + '"' )

		destinition = self.GetDest()
		urlretrieve(self.url, destinition)

		print(GetTime() + ' >> LOG: Download Finished to file "' + destinition + '"')
		ReHLDS.ArchivePath = destinition
		return destinition

class Archive():
	def __init__(self, path):
		self.path = path

	def Unpack_ReHLDS(self, system):
		print(GetTime() + ' >> LOG: Archive path: "' + self.path + '"')
		tempPath = self.path
# LEVEL_1 in ReHLDS.zip
		pZip = zipfile.ZipFile(tempPath, 'r')
		pList = pZip.namelist()
		for item in pList:
			if all([IsArchive(item), IsReHLDS(item)]):
				print(GetTime() + ' >> LOG: File finded: ' + item)
				tempPath = os.curdir + temp_dir + Build_temp
				pZip.extract(item, tempPath)
				tempPath += item
		pZip.close()

# LEVEL_2 in rehlds*.zip
		pZip = zipfile.ZipFile(tempPath, 'r')
		path = (os.curdir + temp_dir + Build_temp)

	# Extract `swds.dll` or `engine_i486.so`
		#print(pZip.namelist())

		need_file = ReHLDS_binary_path
		if system == win32:
			need_file += ReHLDS_engine_win32
			print(GetTime() + ' >> LOG: Choose "' + ReHLDS_engine_win32 + '" version')
		elif system == linux32:
			need_file += ReHLDS_engine_linux32
			print(GetTime() + ' >> LOG: Choose "' + ReHLDS_engine_linux32 + '" version')
		"""
		elif system == both:
			pZip.extract(ReHLDS_binary_path + ReHLDS_engine_win32, path)
			pZip.extract(ReHLDS_binary_path + ReHLDS_engine_linux32, path)
		"""

		pZip.extract(need_file, path)
		if not os.path.exists(Build):
			os.makedirs(Build)

		newname = (Build + 'swds.dll')
		os.rename(path + need_file, newname)
		print(GetTime() + ' >> LOG: ReHLDS installed! File="' + newname + '"')
		pZip.close()

		shutil.rmtree(os.curdir + temp_dir)

def IsReHLDS(name):
	return {("rehlds" in name)}

def IsArchive(name):
	return {(".zip" in name)}


# TRY TO USE
ReHLDS = Component("https://goo.gl/wjjkVZ", "ReHLDS")
ReHLDS.Download()

pZip = Archive(ReHLDS.ArchivePath)
pZip.Unpack_ReHLDS(win32)