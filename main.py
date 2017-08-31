#pip install win10toast
from win32gui import GetWindowText, GetForegroundWindow
from win10toast import ToastNotifier
import time
import win32com.client
import pystray
from PIL import Image, ImageDraw
from ConfigParser import SafeConfigParser
import tempfile
import os
import sys
import threading
from Tkinter import *

# Create that toast!
toaster = ToastNotifier()

# Import settings, if none available, make them
parser = SafeConfigParser()
configfile = tempfile.gettempdir() + "\\autosave_prog.ini"
if not os.path.isfile(configfile):
    with open(configfile, 'w+') as f:
        f.write("[config]\n")
        f.write("interval = 300\n") # Time between saves in seconds
        f.write("deftitle = CLIP STUDIO PAINT\n") # default title
        f.write("trayicon = asdf.png\n") # default icon
        f.write("toasticon = asdf.ico\n") # default toast icon
        f.write("duration = 10") # how long the toast stays up for
parser.read(configfile)
# Globals are bad, mmkay
global INTERVAL, TRAYICON, TOASTICON, PROGRAM, DURATION, shell, icon, cont
INTERVAL = float(parser.get('config','interval'))
TRAYICON = parser.get('config','trayicon')
TOASTICON = parser.get('config','toasticon')
PROGRAM = parser.get('config', 'deftitle')
DURATION = float(parser.get('config','duration'))
cont = True
print "Debug: %s %s %s %s %s" % (INTERVAL,TRAYICON,TOASTICON,PROGRAM,DURATION)

shell = win32com.client.Dispatch("WScript.Shell")

def actual_prog():      
    while cont:
        time.sleep(INTERVAL)
        current_window = GetWindowText(GetForegroundWindow())
        print current_window
        if PROGRAM in current_window:
            toaster.show_toast(
                "Autosaving in 10s",
                "%s" % current_window, icon_path=TOASTICON, duration=DURATION)
            shell.AppActivate(current_window)
            shell.SendKeys("^s")
# def show_settings():
    # return true

    #, command=callback)
    Button(main,text="Save Configuration").grid(column=0,row=b)

    main.mainloop()

class prog_thread (threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
    def run(self):
        print "Starting thread %s" % self.threadID
        actual_prog()

class settings_thread (threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
    def run(self):
        print "Starting thread %s" % self.threadID 
        show_settings()

print "Starting thread"
thread1 = prog_thread(1)
thread1.start()
print "Thread started"

# System tray
state = True
def on_clicked(icon, item):
    global state 
    state = not item.checked
def open_settings():
    threadSettings = prog_thread(2)
    threadSettings.start()
    
def exit_prog():
    icon.stop()
    cont = False

icon = pystray.Icon("AutoSave", Image.open(TRAYICON), "AutoSave", menu=pystray.Menu(
    pystray.MenuItem("Enable", on_clicked,checked=lambda item: state),
    pystray.MenuItem("Settings", open_settings),
    pystray.MenuItem("Exit", exit_prog)
))
icon.run()

sys.exit(0)