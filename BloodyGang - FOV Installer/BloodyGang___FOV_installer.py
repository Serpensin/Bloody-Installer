#Imports
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as mbox
import sys
import requests
import os
import zipfile
import shutil
import subprocess
import pickle


#Define Paths
ini = os.path.join(os.getenv("LOCALAPPDATA"), "DeadByDaylight\Saved\Config\WindowsNoEditor\Engine.ini")
config = os.path.join(os.getenv("LOCALAPPDATA"), "Serpent Modding\BG Installer\Path")
fovlinkLoad = requests.get('https://www.dropbox.com/s/c9f70odtisxyz6m/FOV.zip?dl=1')
root = Tk()
root.withdraw()
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
root.attributes('-topmost', True)


#Check for saved path. (Working)
def selectGame():
    global dbd_exe
    if os.path.exists(config):
        with open(config, "rb") as f:
            dbd_exe = pickle.load(f)
        if not os.path.exists(os.path.join(dbd_exe, 'DeadByDaylight.exe')):
            subprocess.run('cmd /c rmdir "%localappdata%\Serpent Modding" /S /Q')
            selectGame()
        else:
            pass
    else:
        subprocess.run('cmd /c rmdir "%localappdata%\Serpent Modding" /S /Q')
        os.makedirs(os.path.join(os.getenv("LOCALAPPDATA"), "Serpent Modding\BG Installer"))
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
    with open('FOV.zip', 'wb') as f:
        f.write(fovlinkLoad.content)
    with zipfile.ZipFile("FOV.zip", 'r') as zip_ref:
        zip_ref.extractall('BG')


#SSL (Working)
def pak():
    shutil.copy2('BG\pakchunk1-WindowsNoEditor.pak', os.path.join(dbd_exe, "DeadByDaylight\Content\Paks"))
    mbox.showinfo('BG Installer','Success!')
    

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
    pak()


#FOV Uninstall (Working)
def fovUninstall():
    subprocess.run('cmd /c del "%localappdata%\DeadByDaylight\Saved\Config\WindowsNoEditor\Engine.ini"')
    if not os.path.exists(ini):
        mbox.showinfo('BG Installer','FOV was successfully removed.')
    if os.path.exists(ini):
        mbox.showerror('BG Installer','FOV could not be removed.')


#Cleanup (Working)
def cleanup():
    if os.path.exists('BG'):
        shutil.rmtree('BG')
    if os.path.exists('FOV.zip'):
        os.remove('FOV.zip')
    else:
        dc()
    dc()


#Asks to visit our Discord. (Working)
def dc():
    MsgBox = mbox.askquestion ('Thanks for using the "BG Installer"','Do you want to visit our DiscordServer,\nto get more awesome Hacks?',icon = 'question')
    if MsgBox == 'yes':
        subprocess.run('cmd /c explorer "https://discord.gg/gmVkK9p9hA"')
        sys.exit()
    else:
        sys.exit()


selectGame()
download()


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


