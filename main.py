import os
import json
from datetime import datetime
import urllib.request

import unpacker

MOD_NAME = "cstrike"
ROOT_DIR = (os.curdir + "/__BUILD/")
AMXX_DIR_NAME = "amxmodx"
COMPONENTS = "components.json"

systems_list = ['Error!' ,'Linux', 'Win32', 'Both']
system = 0

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
# toFixed = lambda numObj, digits: f"{numObj:.{digits}f}"

def GetFile(url, dir, destinition):
    # Log(' >> Starting donwload non-thread: "{}"'.format(url))
    try:
        header = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64)' }
        req = urllib.request.Request(url, headers=header)
        response = urllib.request.urlopen(req)

        with open(destinition,'wb') as output:
              output.write(response.read())

    except urllib.request.HTTPError as err:
        print(" >> " + os.path.basename(destinition) + " Download aborted! ERROR: " + err.msg)
        return
    Log(' >> Finished donwload non-thread: "{}"'.format(url))

    # Unpack
    ToUnpack(destinition)


from threading import Thread

class DownloadThread(Thread):   
    def __init__(self, url, dir, destinition):
        Thread.__init__(self)
        self.destinition = destinition
        self.url = url
        self.dir = dir
   
    def run(self):
        # Log('>> Starting donwload thread: "{}"'.format(self.url))
        try:
            req = urllib.request.Request(self.url)
            req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64)")
            handle = urllib.request.urlopen(req)

        except urllib.request.HTTPError as err:
            print(" >> " + os.path.basename(self.destinition) + " Download aborted! ERROR: " + err.msg)
            return
        else:
            with open(self.destinition, "wb") as f_handler:
                while True:
                    chunk = handle.read(1024)
                    if not chunk:
                        break
                    f_handler.write(chunk)
        Log('\n >> Finished donwload thread: "{}"'.format(self.url))
        
        # Unpack
        ToUnpack(self.destinition)
        
    # def _stop(self):
        #  Log(' >> _stop(): "{}"'.format(self.url))

    # def _delete(self):
        # Log(' >> _delete(): "{}"'.format(self.url))

    # def join(self):
        # Log(' >> join(): "{}"'.format(self.url))


def GetFile_ByThread(url, dir, destinition):
    thread = DownloadThread(url, dir, destinition)
    thread.start()
    # thread.join() # don't need ?! hmm..


def ToDownload(url, dir, destinition):
# Подготовка папки 
    CheckFolders(dir)

# Thearded download -> (non-used currently)
    # GetFile_ByThread(url, dir, destinition)
# OR Non-Thearded ->
    GetFile(url, dir, destinition)


def ToUnpack(destinition):
    if unpacker.IsArchive(destinition):
        unpacker.ArchiveExtract(os.path.dirname(destinition) ,destinition)
        os.remove(destinition)


def DownloadPackage():
    system_list = []
    if(systems_list[system] == 'Win32'):
        system_list.append('win32')
    elif(systems_list[system] == 'Linux'):
        system_list.append('linux')
    else:
        system_list.append('win32')
        system_list.append('linux')

    counter = 0
    for component in json_data:
        counter += 1
        print(str(counter) + '. ' + component['name'])
        dir = ReplaceAliases(str(component['binary_path']))

# Временно, для проверки распаковки AMXX в потоках
        # if component['name'].find("AmxModX") == -1:
            # continue

    # binary download
        for item in system_list:
            # print(" >>>>>>> Current item:'{}'", format(item))
            url = component[item]['url']
            bin_name = component[item]['bin_name']
            destinition = (dir + bin_name)
            ToDownload(url, dir, destinition)

    # configs & additionals download
        try: # Cause some keys are unavailable
            config_path = ReplaceAliases(str(component['config']['path']))
            config_url = ReplaceAliases(str(component['config']['url']))

            config_name = os.path.basename(config_url)
            destinition = (config_path + config_name)

            ToDownload(config_url, config_path, destinition)

        except KeyError as e:
            # print(' -> [WARN]: Missing Key: "' + e.args[0] + '". Will be Skipped.')
            pass
        # else:
        #    print(' > config_path = ' + config_path)
        #    print('  > config_url = ' + config_url)
    

def Greetings():
    print(" === ReBuild Downloader ===\n")

    GreetingsMsg = ("\
        Выберите систему для скачивания компонентов:\n\
        \t 1. Linux\n\
        \t 2. Win32\n\
        \t 3. Linux + Win32\n\n\
        \
        >>> Система? = \
    ")

    return max(0, min(int(input(GreetingsMsg)), len(systems_list)-1))

if __name__ == "__main__":
    system = Greetings()
    print("Вы выбрали систему: ", systems_list[system])

    # import time
    # start_time = time.time()
    DownloadPackage()

    # Log("Download time = {}".format(time.time() - start_time))