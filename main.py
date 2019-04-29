import os
import json
from datetime import datetime

# From pip
from tqdm import tqdm
import requests

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
    chunk_size = 1024
    r = requests.get(url, stream = True)
    total_size = int(r.headers['content-length'])
    with open(destinition, 'wb') as f:
        for data in tqdm(iterable = r.iter_content(chunk_size = chunk_size), total = total_size/chunk_size, unit = 'KB'):
            f.write(data)


def ToDownload(url, dir, destinition):
# Подготовка папки 
    CheckFolders(dir)
    GetFile(url, dir, destinition)

    # Unpack
    ToUnpack(destinition)

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