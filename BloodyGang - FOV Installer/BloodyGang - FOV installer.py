#Imports
from tkinter import messagebox as mbox
from tkinter import filedialog
from tkinter import *
import tkinter as tk
import tkinter.font as tkFont
from subprocess import Popen
from stat import FILE_ATTRIBUTE_READONLY
from stat import FILE_ATTRIBUTE_NORMAL
import requests as r
import zipfile as zf
import pickle
import urllib
import json
import sys
import os
import webbrowser as wb
import shutil
from threading import _start_new_thread as th


#Define Paths and attributes. (Working)
root = Tk()
root.withdraw()
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
root.attributes('-topmost', True)
local = os.path.join(os.getenv("LOCALAPPDATA"), "SerpentModding\\DBD")
temp = os.path.join(local, "temp")
fovarchive = os.path.join(local, "temp\\FOV.zip")
inibak = os.path.join(local, "Engine.bak")
ini = os.path.join(os.getenv("LOCALAPPDATA"), "DeadByDaylight\\Saved\\Config\\WindowsNoEditor\\Engine.ini")


#Cleanup
def cleanup():
    root.destroy()
    if os.path.exists(temp):
        shutil.rmtree(temp)
    if not 'crash' in globals():
        dc()
    else:
        mbox.showerror(title='BG Installer', message='You need a working internet connection to use this program.\nExiting...')
        sys.exit()


#Test for existing internet connection. (Working)
os.environ['NO_PROXY'] = '.*.'
def connect():
    try:
        urllib.request.urlopen('https://www.dropbox.com/')
        return True
    except:
        return False
def internettest():
    global crash
    if 'ready' in globals():
        while connect():
            pass
        else:
            print('CRASH')
            crash = 1
            cleanup()
    else:
        if connect():
            pass
        else:
            print('START')
            crash = 1
            cleanup()
internettest()


#Checks for messages from the dev. (Working)
def announcement():
    motd = os.path.join(local, "temp\\motd.txt")
    if not os.path.exists(temp):
        os.mkdir(temp)
    with open(motd, 'wb') as f:
        f.write(motdlink.content)
    md = open(motd, 'r')
    if os.stat(motd).st_size != 0:
        mbox.showinfo('BG Installer',md.read())
    else:
        print('Empty')
    md.close()


#Check for saved path. (Working)
def selectGame():
    global dbd_exe
    config = os.path.join(local, "Path")
    if os.path.exists(config):
        with open(config, "rb") as f:
            dbd_exe = pickle.load(f)
        if not os.path.exists(os.path.join(dbd_exe, 'DeadByDaylight.exe')):
            os.remove(config)
            selectGame()
    else:
        if not os.path.exists(local):
            os.makedirs(local)
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


#Checks for messages from the dev.
def announcement():
    motdlink = r.get('https://www.dropbox.com/s/h8w9sd96xxd8fgn/motd.txt?dl=1')
    motd = os.path.join(local, "temp\\motd.txt")
    if not os.path.exists(temp):
        os.mkdir(temp)
    with open(motd, 'wb') as f:
        f.write(motdlink.content)
    md = open(motd, 'r')
    if os.stat(motd).st_size != 0:
        mbox.showinfo('BG Installer',md.read())
    md.close()


#Check for Update.
def updatecheck():
    updatebat = r.get('https://www.dropbox.com/s/hn95nbw9hk4xlgr/SerpentUPDATE.bat?dl=1')
    updatelink = "https://api.github.com/repos/Serpensin/BloodyGang-DBD-SSL-FOV-Installer/releases/latest"
    data = json.loads(r.get(updatelink).text)
    version = os.path.join(local, "Version")
    terz = "Update found: "+data["tag_name"]
    if os.path.exists('SerpentUPDATE.bat'):
        os.remove('SerpentUPDATE.bat')
    if os.path.exists(version):
        with open(version, "rb") as f:
            current = pickle.load(f)
    else:
        current = "v1.2.3"
        pickle.dump(current, open(version, "wb"))
    if current < data["tag_name"]:
        MsgBox = mbox.askquestion (terz,'Program will auto restart after update!\n'+data["body"],icon = 'question')
        if MsgBox == 'yes':
            with open("SerpentUPDATE.bat", 'wb') as f:
                f.write(updatebat.content)
            with open("SerpentUpdate.exe", 'wb') as f:
                f.write(r.get(data['assets'][0]["browser_download_url"]).content)
                pickle.dump(data["tag_name"], open(version, "wb"))
            Popen("SerpentUPDATE.bat")
            sys.exit()


#Download
def download():
    mbox.showinfo('BG Installer','The program will now download\nthe required archive (~100MB).\nThis can take a few seconds.\nPlease wait for another message.')
    fovlinkLoad = r.get('https://www.dropbox.com/s/c9f70odtisxyz6m/FOV.zip?dl=1')
    with open(os.path.join(local, "temp\\FOV.zip"), 'wb') as f:
        f.write(fovlinkLoad.content)
    with zf.ZipFile(fovarchive, 'r') as zip_ref:
        zip_ref.extractall(temp)


#Install the SSL Bypass.
def pak():
    pak = os.path.join(local, "temp\\pakchunk1-WindowsNoEditor.pak")
    pakbak = os.path.join(local, "pakchunk1-WindowsNoEditor.bak")
    if not os.path.exists(fovarchive):
        download()
    shutil.copy2(os.path.join(paks, "pakchunk1-WindowsNoEditor.pak"), pakbak)
    shutil.copy2(pak, paks)
    mbox.showinfo('BG Installer','The installation was successful!')
    

#Install the FOV Mod.
def fovini():
    if os.path.exists(ini):
        os.chmod(ini, FILE_ATTRIBUTE_NORMAL)
    else:
        mbox.showerror('BG Installer','Engine.ini not found!\nPlease start your game once.\nExiting...')
        sys.exit()
    if not os.path.exists(fovarchive):
            download()
    if os.path.exists(inibak):
        shutil.copy2(inibak, ini)
    shutil.copy2(ini, inibak)
    data = data2 = ""
    with open(ini) as fp:
        data = fp.read()
    with open(os.path.join(temp, 'Engine.ini')) as fp:
        data2 = fp.read()
    data += "\n"
    data += data2
    with open (ini, 'w') as fp:
        fp.write(data)
    os.chmod(ini, FILE_ATTRIBUTE_READONLY)
    pak()


#Uninstall
def uninstall():
    pakbak = os.path.join(local, "pakchunk1-WindowsNoEditor.bak")
    if os.path.exists(inibak):
        os.chmod(ini, FILE_ATTRIBUTE_NORMAL)
        shutil.copy2(inibak, ini)
        os.chmod(ini, FILE_ATTRIBUTE_READONLY)
    else:
        if os.path.exists(ini):
            os.chmod(ini, FILE_ATTRIBUTE_NORMAL)
            os.remove(ini)
    if os.path.exists(pakbak):
        shutil.copy2(pakbak, os.path.join(paks, "pakchunk1-WindowsNoEditor.pak"))
        os.remove(pakbak)
    mbox.showinfo('BG Installer','All hacks are removed!\nYou can now use our other tools.')


#Asks to visit our Discord. (Working)
def dc():
    MsgBox = mbox.askquestion ('Thanks for using the "BG Installer"','Do you want to visit our DiscordServer,\nto get more awesome Hacks?',icon = 'question')
    if MsgBox == 'yes':
        wb.open("https://discord.gg/gmVkK9p9hA", 0)
        sys.exit()
    else:
        sys.exit()


#Prompts to not use this program in PTB. (Working)
MsgBox = mbox.askquestion ('BG Installer','This software is ONLY for the Steam version!\nDo not use it if you are currently participating in the PTB!\nDo you want to continue?',icon = 'warning')
if not MsgBox == 'yes':
    cleanup()


selectGame()
announcement()
updatecheck()
paks = os.path.join(dbd_exe, "DeadByDaylight\\Content\\Paks")


#Buttons (Working)
Button(root, text='Uninstall FOV/SSL', fg='#ffffff', bg='#b8860b', font=('Microsoft Sans Serif', 12, 'normal',), command=uninstall).place(x=36, y=100)
Button(root, text='Install FOV', fg='#ffffff', bg='#b8860b', font=('Microsoft Sans Serif', 12, 'normal'), command=fovini).place(x=13, y=55)
Button(root, text='Install SSL', fg='#ffffff', bg='#b8860b', font=('Microsoft Sans Serif', 12, 'normal'), command=pak).place(x=116, y=55)
Button(root, text='X', fg='#ffffff', bg='#FE2E2E', font=('arial', 12, 'bold'), command=cleanup).place(x=181, y=8)


#This is the section of code which creates the main window. (Working)
ready = 1
th(internettest)
root.deiconify()
root.geometry("+{}+{}".format(positionRight, positionDown))
root.geometry('220x150')
root.configure(background='#23272a')
root.resizable(0,0)
root.overrideredirect(1)
root.mainloop()



