#pip install win10toast
from win32gui import GetWindowText, GetForegroundWindow
from win10toast import ToastNotifier
import time
import win32com.client
import pystray
import PIL.Image
from ConfigParser import SafeConfigParser
import tempfile
import os
import sys
import threading
from Tkinter import *
from tkFileDialog import askopenfilename

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
global INTERVAL, TRAYICON, TOASTICON, PROGRAM, DURATION, shell, icon, cont, configfile, state
INTERVAL = float(parser.get('config','interval'))
TRAYICON = parser.get('config','trayicon')
TOASTICON = parser.get('config','toasticon')
PROGRAM = parser.get('config', 'deftitle')
DURATION = float(parser.get('config','duration'))
cont = True
state = False
print "Debug: %s %s %s %s %s" % (INTERVAL,TRAYICON,TOASTICON,PROGRAM,DURATION)

shell = win32com.client.Dispatch("WScript.Shell")

def askopenfileico(ti):
    file = askopenfilename(filetypes=(("ICO files","*.ico"),("All files","*.*")))
    print file
    ti.set(file)
    return file
def askopenfileimg(ti):
    file = askopenfilename(filetypes=(("PNG files","*.png"),("JPEG files","*.jpg"),("ICO files","*.ico")))
    ti.set(file)
    return file

def callback(_interval,_toasticon,_toastlength,_trayicon,_progtitle, main):
    print "We have a winner!"
    INTERVAL = _interval
    TOASTICON = _toasticon
    DURATION = _toastlength
    TRAYICON = _trayicon
    PROGRAM = _progtitle
    os.remove(configfile)   # Honestly I can probably do better than this
    with open(configfile, 'w+') as f:
        f.write("[config]\n")
        f.write("interval = %s\n" % INTERVAL) # Time between saves in seconds
        f.write("deftitle = %s\n" % PROGRAM) # default title
        f.write("trayicon = %s\n" % TRAYICON) # default icon
        f.write("toasticon = %s\n" % TOASTICON) # default toast icon
        f.write("duration = %s" % DURATION) # how long the toast stays up for
    main.destroy()

# Settings window
def settingswindow():
    main = Tk()
    main.title("Settings")
    label = []
    entry = []
    label.append(Label(main,text="Interval (seconds)"))
    label.append(Label(main,text="Toast Icon"))
    label.append(Label(main,text="Toast Length"))
    label.append(Label(main,text="Tray Icon"))
    label.append(Label(main,text="Program Title"))
    _intrvl = StringVar()
    _toasticon = StringVar()
    _toastlen = StringVar()
    _trayicon = StringVar()
    _progtitle = StringVar()
    _intrvl.set(INTERVAL)
    _toasticon.set(TOASTICON)
    _toastlen.set(DURATION)
    _trayicon.set(TRAYICON)
    _progtitle.set(PROGRAM)
    entry.append(Entry(main, textvariable=_intrvl))
    entry.append(Entry(main, textvariable=_toasticon))
    entry.append(Entry(main, textvariable=_toastlen))
    entry.append(Entry(main, textvariable=_trayicon))
    entry.append(Entry(main, textvariable=_progtitle))
    b = 2
    for a in label:
        a.grid(column=0,row=b)
        b = b+1
    b = 2
    for a in entry:
        a.grid(column=1,row=b)
        b = b+1
    Button(main,text="Browse",command=lambda: askopenfileico(_toasticon)).grid(column=3,row=3)
    Button(main,text="Browse",command=lambda: askopenfileimg(_trayicon)).grid(column=3,row=5)
    Button(main,text="Save Configuration", command=lambda: callback(_intrvl.get(),_toasticon.get(),_toastlen.get(),_trayicon.get(),_progtitle.get(), main)).grid(column=0,row=b)
    main.mainloop()

settingswindow()

def actual_prog(self):    
    while self.running:
        while state:
            time.sleep(INTERVAL)
            current_window = GetWindowText(GetForegroundWindow())
            print current_window
            if PROGRAM in current_window:
                toaster.show_toast(
                    "Autosaving in 10s",
                    "%s" % current_window, icon_path=TOASTICON, duration=DURATION)
                keystrokes(current_window)

        time.sleep(5) # There's gonna be a five second delay after saving config settings and it actually taking effect but whatever

def show_settings():
    return True
    
class prog_thread (threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.running = True
    def run(self):
        print "Starting thread %s" % self.threadID
        actual_prog(self)
    def stop():
        self.running = False

class settings_thread (threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        print "Starting thread %s" % self.threadID 
        show_settings()

print "Starting thread"
thread1 = prog_thread(1)
threadSettings = prog_thread(2)
thread1.setDaemon(True)
thread1.start()
print "Thread started"
# System tray
state = True
def keystrokes(current_window):
    shell.AppActivate(current_window)
    shell.SendKeys("^s")
def on_clicked(icon, item):
    global state 
    state = not item.checked
def open_settings():
    print "testing!"
    main.deiconify()
def exit_prog():
    icon.stop()
    state = False
    thread1.stop()
    thread1.join()
    sys.exit(0)

icon = pystray.Icon("AutoSave", PIL.Image.open(TRAYICON), "AutoSave", menu=pystray.Menu(
    pystray.MenuItem("Enable", on_clicked,checked=lambda item: state),
    #pystray.MenuItem("Settings", open_settings),
    pystray.MenuItem("Exit", exit_prog)
))

icon.run()

sys.exit(0)
