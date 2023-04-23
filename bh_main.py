# import important stuff

import os
import shutil
import zipfile

# oo that looks nice (applies color to cmd)

os.system('color 02')

# get appdata, make a list of presets, and get betterbar main and presets folder

appdata = os.getenv('LOCALAPPDATA')
main_pth = os.path.dirname(__file__)
mpreset_pth = main_pth + "\presets"
list_of_p = []

# roblox versions folder

rversions_folder = f"{appdata}\Roblox\Versions\\"

# if roblox versions folder exists,
# search in the two folders to see which one has the 
# roblox GAME client, and then get the assets folder from there.

if os.path.exists(rversions_folder):
    for root, dirs, files in os.walk(rversions_folder):
        if "RobloxPlayerBeta.exe" in files:
            folder_dir = os.path.abspath(root)
            topbar_dir = fr"{folder_dir}\content\textures\ui\TopBar\\"

            print(f"[ROBLOX] Current installation folder: {folder_dir}")
            print(f"[ROBLOX] Current TopBar assets folder: {topbar_dir}")
            break
else:
    print("[ERROR] Roblox 'Versions' folder does not exist.")
    print("[ERROR] This could be because of Roblox not being installed.")
    input("[EXIT] Press enter to exit.\n")
    exit()

# for each file in presets, if ends with zip
# append to list of presets. if not zip, pass.

for file_name in os.listdir(mpreset_pth):
    if file_name.endswith(".zip"):
        try:
            list_of_p.append(file_name)
        except:
            pass

# visually better for choosing,
# also gives you the knowledge of what you're 
# actually picking.

options_numbered = '\n'.join(f"{i+1}. {option}" for i, option in enumerate(list_of_p))
zip_files = input(f"\n[PRESETS] Choose an preset:\n{options_numbered}\n\n")

# if answer is not a digit or zero, or longer than the list
# throw an invalid error.
# if answer is valid, create an folder to temporarily
# store the images, copy to roblox assets and delete the folder.

if not zip_files.isdigit() or int(zip_files) < 1 or int(zip_files) > len(list_of_p):
    print("[PRESETS] Invalid preset option.")
else:
    try:
        selected_preset = list_of_p[int(zip_files) - 1]
        print(f"[PRESETS] Preset selected: {selected_preset}.")
    
        cache_pth = os.path.join(main_pth, "extractCache\\")
        os.mkdir(cache_pth)

        with zipfile.ZipFile(f'{mpreset_pth}\\{selected_preset}', 'r') as zip:
            zip.extractall(f'{cache_pth}')

        for file_name in os.listdir(cache_pth):
            source = cache_pth + file_name
            destination = topbar_dir + file_name

            try:
                os.remove(destination)
                print('[STATUS] Removed original file:', file_name)
            except:
                pass

            if os.path.isfile(source):
                shutil.copy(source, destination)
                print('[STATUS] Copied file:', file_name)

        shutil.rmtree(cache_pth)
        os.system("color")
        os.system("cls")

        input("[STATUS] All done! Press enter to exit.\n")
        os.system("cls")
    except Exception as error:
        print(f"[ERROR]: {error}")
