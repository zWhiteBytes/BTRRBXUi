import os
import sys
import shutil
import zipfile

# Clear the console screen based on the platform
def clr():
    if sys.platform.startswith('win32'):
        os.system('cls')
    elif sys.platform.startswith('linux'):
        os.system('clear')

# Get program files, get the preset directory and make an empty preset list,
# and get BTRRBXBar main and presets folder.
# Also verify OS.

if sys.platform.startswith("win32"):
    program_files = os.getenv("ProgramFiles(x86)")
elif sys.platform.startswith("linux"):
    print("\033[93mThis was tested on Linux Mint.")
    print("\033[93mYou also need to use Grapejuice.")
    print("\033[93mMay work or may not work.")
    yrn_input = input("\033[92mContinue? (Y/N): ")

    if yrn_input == 'Y':
        print("Continuing...")
    elif yrn_input == 'N':
        print("Exiting...")
        sys.exit()

    program_files = os.path.join(os.getenv("HOME"), ".local", "share", "grapejuice", "prefixes", "player", "drive_c", "Program Files (x86)")
elif sys.platform.startswith("darwin"):
    print('\033[93mUntested and not supported on MacOS.')
else:
    print('\033[93mUntested and most likely not supported on your OS.')

main_path = os.path.dirname(__file__)
preset_path = os.path.join(main_path, "presets")
preset_list = []
ui_dir = ""

# Roblox versions folder.

versions_folder = os.path.join(program_files, "Roblox", "Versions")

# If Roblox versions folder exists,
# find the Roblox player .exe.
# Thus we'll know the folder it is in.

if os.path.exists(versions_folder):
    for root, dirs, files in os.walk(versions_folder):
        if "RobloxPlayerBeta.exe" in files:
            folder_dir = os.path.abspath(root)
            ui_dir = os.path.join(folder_dir, "content", "textures", "ui")

            print(f"\033[92m[ROBLOX] Current installation folder: {folder_dir}")
            print(f"\033[92m[ROBLOX] Current TopBar assets folder: {ui_dir}")
            break
else:
    print("\033[93m[ERROR] ROBLOX 'Versions' folder does not exist.")
    print("\033[93m[ERROR] ROBLOX may not be installed.")
    input("\033[93m[EXIT] Press enter to exit.\n")
    exit()

# For each file in presets folder, if it ends with ".zip",
# append it to the list of presets.

for file_name in os.listdir(preset_path):
    if file_name.endswith(".zip"):
        preset_list.append(file_name)

# Show the options.

options = '\n'.join(f"{i+1}. {option}" for i, option in enumerate(preset_list))
preset_files = input(f"\n\033[92m[PRESETS] Choose a preset:\n{options}\n\n")

# Check if the option selected was valid,
# if not say invalid
# if yes then continue the process.

if not preset_files.isdigit() or int(preset_files) < 1 or int(preset_files) > len(preset_list):
    print("\033[93m[PRESETS] Invalid preset option.")
else:
    try:
        # Get the selected preset zip file, create a temporary folder,
        # extract the zip in there, copy everything in the folder to the
        # UI folder and then delete the temporary folder.

        clr()
        selected_preset = preset_list[int(preset_files) - 1]
        print(f"\033[92m[PRESETS] Preset selected: {selected_preset}.")

        temp_path = os.path.join(main_path, "extractTemp")
        try:
            if os.path.exists(temp_path):
                shutil.rmtree(temp_path)
                print(f"\033[92m[STATUS] Removed existing folder: {temp_path}")
        except:
            pass

        os.mkdir(temp_path)

        with zipfile.ZipFile(os.path.join(preset_path, selected_preset), 'r') as zip_file:
            zip_file.extractall(temp_path)

        for item in os.listdir(temp_path):
            source = os.path.join(temp_path, item)
            destination = os.path.join(ui_dir, item)

            try:
                if os.path.isdir(destination):
                    shutil.rmtree(destination)
                    print('\033[92m[STATUS] Removed existing folder:', item)
                elif os.path.isfile(destination):
                    os.remove(destination)
                    print('\033[92m[STATUS] Removed existing file:', item)
            except Exception as error:
                print(f"\033[93m[ERROR]: {error}")

            if os.path.isdir(source):
                shutil.copytree(source, destination)
                print('\033[92m[STATUS] Copied folder:', item)
            else:
                shutil.copy2(source, destination)
                print('\033[92m[STATUS] Copied file:', item)

        shutil.rmtree(temp_path)

        clr()
        input("\033[92m[STATUS] All done! Press enter to exit.\n")
        clr()
    except Exception as error:
        print(f"\033[93m[ERROR]: {error}")
