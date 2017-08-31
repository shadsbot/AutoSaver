# AutoSaver
_Compatability companion program for applications that don't support autosave_

## How to Use
Double click the app, it will create a config file in `%TEMP%\autosave_prog.ini`. Feel free to edit these settings to better fit your preferences. The program is preset for Clip Studio, but basically that field is looking to see if what you put in there is in the currently active window title. It doesn't have to be an exact match, it just has to contain it.

## What this program will do
Every X seconds, it will send the `CTRL-S` key presses if the specified program is in the foreground. If you're in a tabbed program like Paint Clip Studio or Notepad++ or Visual Studio Code or PhotoShop, it will save the __active tab at that time__.

Basically, it's a robot that reaches over your shoulder ever X seconds and hits `CTRL-S` to save whatever art or code tab you have up if the right program is up.

## What this program won't do
It won't autosave a particular artboard that you've left up in the background... yet.

## Customizing? Sure, why not
This program is licensed under the MIT license, so have fun. Also, you can specify the icons that are used in the sys tray and the toast notification. Toast notification has to be a .ico, sys tray can be png or jpg or ico (I think?).

__Technicals__

If you're going to be editing the code for this at all, you'll need `win10toast` and `pystray` for Python 2.7.

## Known bugs
If you've got the mouse held down during an autosave period, it may not save. I think this is a restriction of the `win32com.cient` lib. I'll keep looking for a fix but uh, no promises.
