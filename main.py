import os
import json
from datetime import datetime
import urllib.request

from unpacker import ArchiveExtract

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


from threading import Thread

class DownloadThread(Thread):
    """
    Пример скачивание файла используя многопоточность
    """
   
    def __init__(self, url, dir, destinition):
        """Инициализация потока"""
        Thread.__init__(self)
        self.destinition = destinition
        self.url = url
        self.dir = dir
   
    def run(self):
        """Запуск потока"""
        Log(' >> Starting donwload: "' + self.url + '"' )

        try:
            req = urllib.request.Request(self.url)
            req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64)")
            handle = urllib.request.urlopen(req)

        except urllib.request.HTTPError as err:
            print(" >> Download aborted! ERROR: " + err.msg)
            return
   
        with open(self.destinition, "wb") as f_handler:
            while True:
                chunk = handle.read(1024)
                if not chunk:
                    break
                f_handler.write(chunk)

        DownloadEnd(self.url, self.destinition)
       

def DownloadEnd(url, file):
    Log(" > '%s' закончил загрузку!" %(file))
    if url.find('www.amxmodx.org') != -1:
        ArchiveExtract(os.path.dirname(file) ,file)
        print(">>>>> " + os.path.dirname(file))
        # os.remove(file)


def DownloadOnThread(url, dir, destinition):
    """    Запускаем программу """
    thread = DownloadThread(url, dir, destinition)
    thread.start()

def ToDownload(url, dir, destinition):
# Подготовка папки 
    CheckFolders(dir)

# Thearded download ->
    # DownloadOnThread(url, dir, destinition)

# Non-Thearded -> (deprecated)
    GetFile(url, dir, destinition)


system = 'both'
# system = 'linux'
# system = 'win32'

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
            ToDownload(url, dir, destinition)
            # 
            DownloadEnd(url, destinition)

    # configs & additionals download
        try: # Cause some keys are unavailable
            config_path = ReplaceAliases(str(component['config']['path']))
            config_url = ReplaceAliases(str(component['config']['url']))

            config_name = os.path.basename(config_url)
            destinition = (config_path + config_name)

            ToDownload(config_url, config_path, destinition)
            # DownloadOnThread(config_url, config_path, destinition)

        except KeyError as e:
            # print(' -> [WARN]: Missing Key: "' + e.args[0] + '". Will be Skipped.')
            pass
        #else:
        #    print(' > config_path = ' + config_path)
        #    print('  > config_url = ' + config_url)

if __name__ == "__main__":
    DownloadPackage()