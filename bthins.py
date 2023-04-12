# import important stuff
import os
import shutil

# appdata, subfolders function, and betterhud assets folder
appdata = os.getenv('LOCALAPPDATA')
subfolders = [f.path for f in os.scandir() if f.is_dir()]
masset_pth = os.path.dirname(__file__) + r"\assets\\"

# versions folder
rassets_parent_folder = f"{appdata}\Roblox\Versions\\"

# search for every folder in roblox folder to find the exe,
# thats the version of roblox, and then get the assets folder

for root, dirs, files in os.walk(rassets_parent_folder):
    if "RobloxPlayerBeta.exe" in files:
        folder_dir = os.path.abspath(root)
        topbar_dir = fr"{folder_dir}\content\textures\ui\TopBar\\"

        print("[ROBLOX] Current installation folder: ", folder_dir)
        print("[ROBLOX] Current assets folder: ", topbar_dir)
        break

# for file in folder, remove original and copy mod 
# to roblox assets folder

for file_name in os.listdir(masset_pth):
    source = masset_pth + file_name
    destination = topbar_dir + file_name

    try:
        os.remove(destination)
        print('[STATUS] Removed OG:', file_name)
    except:
        pass

    if os.path.isfile(source):
        shutil.copy(source, destination)
        print('[STATUS] Copied file:', file_name)