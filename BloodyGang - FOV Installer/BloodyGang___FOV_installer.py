#Imports
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as mbox
import sys
import webbrowser as wb
import requests
import os
import zipfile
import shutil


#Define Paths
ini = os.path.join(os.getenv("LOCALAPPDATA"), "DeadByDaylight\Saved\Config\WindowsNoEditor\Engine.ini")
root = Tk()
root.withdraw()
discord = "https://discord.gg/xk9kJnVxTh"
fovlinkLoad = requests.get('https://bloodygang.serveblog.net/index.php/s/N4jQosCBL5SPWfi/download')
dbd_folder = ("C:\Program Files (x86)\Steam\steamapps\common\Dead by Daylight")
dbd_exe = ("C:\Program Files (x86)\Steam\steamapps\common\Dead by Daylight\DeadByDaylight.exe")

#Determines the location where DeadByDaylight is curently installed. (Working)
def selectGame():
    if not os.path.exists(dbd_exe):
        root.iconbitmap("C:/Users/wissm/OneDrive/Bilder/ICO/BG.ico")
        root.filename = filedialog.askopenfilename(initialdir="C:\\", title="Select 'DeadByDaylight.exe' from your Gamefolder.", filetypes=[("DeadByDaylight .exe")])
        if "DeadByDaylight.exe" in root.filename:
            os.makedirs('BG')
            fovMain()
        else:
            MsgBox = mbox.askquestion ('BG Installer','You need to select "DeadByDaylight.exe" to use this Installer. Retry?',icon = 'warning')
            if MsgBox == 'yes':
                selectGame()
            else:
                cleanup()
    else:
        fovMain()


#FOV - Main (Working)
def fovMain():
    #Download and unpack the archive. (Working)
    with open('FOV.zip', 'wb') as f:
        f.write(fovlinkLoad.content)
    with zipfile.ZipFile("FOV.zip", 'r') as zip_ref:
        zip_ref.extractall('BG')
    #Asks the user to install FOV or only SSL Bypass. (Working)
    MsgBox = mbox.askquestion ('BG Installer','Do you want to install FOV, or just SSL Bypass?\nClick "Yes" for both. Click "No" for SSL only.',icon = 'question')
    if MsgBox == 'yes':
        pak()
        fovini()
        cleanup()
    if MsgBox == 'no':
        pak()
        cleanup()


#SSL (Working)
def pak():
    if os.path.exists(dbd_exe):
        shutil.copy2('BG\pakchunk1-WindowsNoEditor.pak', os.path.join(dbd_folder, "DeadByDaylight\Content\Paks"))
    else:
        shutil.copy2('BG\pakchunk1-WindowsNoEditor.pak', os.path.join((os.path.dirname(root.filename)), "DeadByDaylight\Content\Paks"))
    

#Install the FOV Mod. (Working)
def fovini():
    data = data2 = ""
    with open(ini) as fp:
        data = fp.read()
    with open('BG\Engine.ini') as fp:
        data2 = fp.read()
    data += "\n"
    data += data2
    with open (ini, 'w') as fp:
        fp.write(data)


#Cleanup (Working)
def cleanup():
    if os.path.exists('BG'):
        shutil.rmtree('BG')
    if os.path.exists('FOV.zip'):
        os.remove('FOV.zip')
    else:
        pass


selectGame()


#Asks to visit our Discord.
MsgBox = mbox.askquestion ('Thanks for using the "BG Installer"','Do you want to visit our DiscordServer,\nto get more awesome Hacks?',icon = 'question')
if MsgBox == 'yes':
    wb.open(discord)
    sys.exit()
else:
    sys.exit()

