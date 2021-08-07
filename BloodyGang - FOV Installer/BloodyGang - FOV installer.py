#Imports
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as mbox
import sys
import requests
import os
import zipfile
import subprocess
import pickle
import json
import urllib.request


#Sets the attributes for the program windows. (Working)
root = Tk()
root.withdraw()
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
root.attributes('-topmost', True)


#Test for existing internet connection. (Working)
def connect():
    try:
        urllib.request.urlopen('http://google.com')
        return True
    except:
        return False
def test():
    if connect():
        pass
    else:
        MsgBox = mbox.showerror(title='BG Installer', message='You need a working internet connection to use this program.\nExiting...')
        sys.exit()
test()


#Define Paths (Working)
ini = os.path.join(os.getenv("LOCALAPPDATA"), "DeadByDaylight\\Saved\\Config\\WindowsNoEditor\\Engine.ini")
local = os.path.join(os.getenv("LOCALAPPDATA"), "SerpentModding\\DBD")
fovarchive = os.path.join(local, "FOV.zip")
inibak = os.path.join(local, "Engine.bak")
version = os.path.join(local, "Version")
config = os.path.join(local, "Path")
temp = os.path.join(local, "temp")
fovlinkLoad = requests.get('https://www.dropbox.com/s/c9f70odtisxyz6m/FOV.zip?dl=1')
updatebat = requests.get('https://www.dropbox.com/s/hn95nbw9hk4xlgr/SerpentUPDATE.bat?dl=1')
updatelink = "https://api.github.com/repos/Serpensin/BloodyGang-DBD-SSL-FOV-Installer/releases/latest"
data = json.loads(requests.get(updatelink).text)


#Check for Update. (Working)
def updatecheck():
    terz = "Update found: "+data["tag_name"]
    subprocess.run('cmd /c del /Q "SerpentUPDATE.bat"')
    if os.path.exists(version):
        with open(version, "rb") as f:
            current = pickle.load(f)
    else:
        current = "v1.2"
        pickle.dump(current, open(version, "wb"))
    if current < data["tag_name"]:
        MsgBox = mbox.askquestion (terz,data["body"],icon = 'question')
        if MsgBox == 'yes':
            with open("SerpentUPDATE.bat", 'wb') as f:
                f.write(updatebat.content)
            with open("SerpentUpdate.exe", 'wb') as f:
                f.write(requests.get(data['assets'][0]["browser_download_url"]).content)
                pickle.dump(data["tag_name"], open(version, "wb"))
            subprocess.Popen("SerpentUPDATE.bat")
            sys.exit()
        else:
            pass
    else:
        pass


#Check for saved path. (Working)
def selectGame():
    global dbd_exe
    if os.path.exists(config):
        with open(config, "rb") as f:
            dbd_exe = pickle.load(f)
        if not os.path.exists(os.path.join(dbd_exe, 'DeadByDaylight.exe')):
            subprocess.run('cmd /c rmdir "%localappdata%\\SerpentModding" /S /Q')
            selectGame()
        else:
            pass
    else:
        subprocess.run('cmd /c rmdir "%localappdata%\SerpentModding" /S /Q')
        os.makedirs(os.path.join(os.getenv("LOCALAPPDATA"), "SerpentModding\\DBD"))
        root.filename = filedialog.askopenfilename(initialdir="C:\\", title="Select 'DeadByDaylight.exe' from your Gamefolder.", filetypes=[("DeadByDaylight .exe")])
        if "DeadByDaylight.exe" in root.filename:
            dbd_exe = os.path.dirname(root.filename)
            pickle.dump(dbd_exe, open(config, "wb"))
        else:
            MsgBox = mbox.askquestion ('BG Installer','You need to select "DeadByDaylight.exe" to use this Installer. Retry?',icon = 'warning')
            if MsgBox == 'yes':
                selectGame()
            else:
                cleanup()


#Download (Working)
def download():
    mbox.showinfo('BG Installer','The program will now download\nthe required archive (~100MB).\nThis can take a few seconds.\nPlease wait for another message.')
    if not os.path.exists(temp):
        os.mkdir(temp)
    else:
        pass
    with open(fovarchive, 'wb') as f:
        f.write(fovlinkLoad.content)
    with zipfile.ZipFile(fovarchive, 'r') as zip_ref:
        zip_ref.extractall(temp)


#Install the SSL Bypass. (Working)
def pak():
    pak = os.path.join(os.getenv("LOCALAPPDATA"), "SerpentModding\\DBD\\temp\\pakchunk1-WindowsNoEditor.pak")
    if os.path.exists(fovarchive):
        pass
    else:
        download()
    subprocess.run('cmd /c copy /Y "'+pak + '" "' +paks+'"')
    mbox.showinfo('BG Installer','The installation was successful!')
    

#Install the FOV Mod. (Working)
def fovini():
    if os.path.exists(fovarchive):
        pass
    else:
        download()
    subprocess.run('cmd /c attrib -R  "'+ini + '"')
    if os.path.exists(inibak):
        subprocess.run('cmd /c copy /Y "'+inibak + '" "' +ini+'"')
    subprocess.run('cmd /c copy /Y "'+ini + '" "' +inibak+'"')
    data = data2 = ""
    with open(ini) as fp:
        data = fp.read()
    with open(os.path.join(temp, 'Engine.ini')) as fp:
        data2 = fp.read()
    data += "\n"
    data += data2
    with open (ini, 'w') as fp:
        fp.write(data)
    subprocess.run('cmd /c attrib +R  "'+ini + '"')
    pak()


#FOV Uninstall (Working)
def fovUninstall():
    subprocess.run('cmd /c attrib -R  "'+ini + '"')
    subprocess.run('cmd /c copy /Y "'+inibak + '" "' +ini+'"')
    subprocess.run('cmd /c attrib +R  "'+ini + '"')
    mbox.showinfo('BG Installer','The FOV hack is now removed!')


#Cleanup (Working)
def cleanup():
    subprocess.run('cmd /c del /Q "'+fovarchive +'"')
    subprocess.run('cmd /c rmdir /S /Q "'+temp +'"')
    dc()


#Asks to visit our Discord. (Working)
def dc():
    MsgBox = mbox.askquestion ('Thanks for using the "BG Installer"','Do you want to visit our DiscordServer,\nto get more awesome Hacks?',icon = 'question')
    if MsgBox == 'yes':
        subprocess.run('cmd /c explorer "https://discord.gg/gmVkK9p9hA"')
        sys.exit()
    else:
        sys.exit()


#Prompts to not use this program in PTB. (Working)
MsgBox = mbox.askquestion ('BG Installer','This software is ONLY for the Steam version!\nDo not use it if you are currently participating in the PTB!\nDo you want to continue?',icon = 'warning')
if MsgBox == 'yes':
    pass
else:
    cleanup()


selectGame()
updatecheck()
paks = os.path.join(dbd_exe, "DeadByDaylight\\Content\\Paks")


#Buttons (Working)
Button(root, text='Uninstall FOV', bg='#90EE90', font=('arial', 12, 'normal'), command=fovUninstall).place(x=6, y=8)
Button(root, text='Install FOV', bg='#90EE90', font=('arial', 12, 'normal'), command=fovini).place(x=130, y=8)
Button(root, text='Install SSL', bg='#90EE90', font=('arial', 12, 'normal'), command=pak).place(x=233, y=8)
Button(root, text='Close', bg='#90EE90', font=('arial', 12, 'normal'), command=cleanup).place(x=147, y=55)


#This is the section of code which creates the main window. (Working)
root.deiconify()
root.geometry("+{}+{}".format(positionRight, positionDown))
root.geometry('327x100')
root.configure(background='#FFFFFF')
root.resizable(0,0)
root.overrideredirect(1)
root.mainloop()


