#region Setup

import os
import subprocess
import platform
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import tkinter.ttk
import customtkinter

#Window setup
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.minsize(width=800, height=250)
root.title("Robocopy Builder")

headerFrame = customtkinter.CTkFrame(master=root)
headerFrame.grid(row = 0, column = 0)

builderFrame = customtkinter.CTkFrame(master=root)
builderFrame.grid(row = 1, column = 0)

execFrame = customtkinter.CTkFrame(master=root)
execFrame.grid(row = 2, column = 0)

outputFrame = customtkinter.CTkFrame(master=root)
outputFrame.grid(row = 3, column = 0)

functionFrame = customtkinter.CTkFrame(master=builderFrame)
functionFrame.grid(row = 0, column = 0)

fileFrame = customtkinter.CTkFrame(master=functionFrame)
fileFrame.grid(row = 0, column = 0)

optionsFrame = customtkinter.CTkFrame(master=functionFrame)
optionsFrame.grid(row = 1, column = 0, pady = 10)

#endregion
#region functions and setup

#Establish variables
sourceDirectory = tkinter.StringVar()
destinationDirectory = tkinter.StringVar()
optSubDirStr = tkinter.StringVar()
optPurgeStr = tkinter.StringVar()
optNewerStr = tkinter.StringVar()
excludeStr = tkinter.StringVar()
resultStr = tkinter.StringVar()

#Folder Dialog Functions
def sourceBrowseButton():
    folderName = tkinter.filedialog.askdirectory()
    sourceDirectory.set(folderName)
    return folderName

def destinationBrowseButton():
    folderName = tkinter.filedialog.askdirectory()
    destinationDirectory.set(folderName)
    return folderName

#Functions
def createRoboString():
    srcDir = os.path.abspath(sourceDirectory.get())
    destDir = os.path.abspath(destinationDirectory.get())
    exclStr = excludeStr.get()
    if not exclStr:
        roboCmd = f'Robocopy "{srcDir}" "{destDir}" {optSubDirStr.get()} /R:2 /W:1 /V /ETA /TEE {optPurgeStr.get()} {optNewerStr.get()} /XA:SHTC'
    else:
        roboCmd = f'Robocopy "{srcDir}" "{destDir}" /XF {exclStr} {optSubDirStr.get()} /R:2 /W:1 /V /ETA /TEE {optPurgeStr.get()} {optNewerStr.get()} /XA:SHTC'
    return roboCmd

def showRoboScript():
    resultStr.set(createRoboString())
    resultTextbox.configure(state = "normal")
    resultTextbox.delete("0.0", "end")
    resultTextbox.insert("1.0", ":start" + '\n' + '\n')
    resultTextbox.insert("4.0", "Title Robocopy Script" + '\n')
    resultTextbox.insert("5.0", resultStr.get() + '\n' + '\n')
    resultTextbox.insert("7.0", "pause")
    resultTextbox.configure(state = "disabled")

def copyResultStr():
    copyStr = resultTextbox.get("0.0", "end")
    root.clipboard_clear()
    root.clipboard_append(copyStr)
    root.update()

def excludeHelp():
    excludeHelpMsg = "Use spaces to separate files; " + '\n' + "Use * as wildcard, ex: *.txt excludes all txt files; " + '\n' + "Use ? as individual letter wildcard"
    tkinter.messagebox.showinfo(title="Exclusion Formatting", message= excludeHelpMsg)

#endregion
#region Window Elements
headerLabel = customtkinter.CTkLabel(master=headerFrame, text="Robocopy Script Builder")
headerLabel.pack(anchor = "center")

execButton = customtkinter.CTkButton(master=execFrame, text="Generate Robocopy Script", command=showRoboScript)
execButton.pack(anchor="center")

resultLabel = customtkinter.CTkLabel(master=outputFrame, text="")
resultLabel.pack(anchor = "w")

#Source and Directory Buttons
sourceLabel = customtkinter.CTkLabel(master=fileFrame, text="Source:")
sourceLabel.grid(row = 0, column = 0)

sourceField = customtkinter.CTkEntry(master=fileFrame, width=300, textvariable=sourceDirectory)
sourceField.grid(row=0, column=1)

sourceButton = customtkinter.CTkButton(master=fileFrame, text="Browse", command=sourceBrowseButton)
sourceButton.grid(row = 0, column = 2)

destinationLabel = customtkinter.CTkLabel(master=fileFrame, text="Destination:")
destinationLabel.grid(row = 1, column = 0)

destinationField = customtkinter.CTkEntry(master=fileFrame, width=300, textvariable=destinationDirectory)
destinationField.grid(row = 1, column = 1)

destinationButton = customtkinter.CTkButton(master=fileFrame, text="Browse", command=destinationBrowseButton)
destinationButton.grid(row = 1, column = 2)

#Option Buttons
optSubDir = customtkinter.CTkCheckBox(master=optionsFrame, text="Include Subdirectories", variable=optSubDirStr, onvalue="/E ", offvalue="")
optSubDir.grid(row = 0, column = 0, padx = 10)

optPurge = customtkinter.CTkCheckBox(master=optionsFrame, text="Remove Other Files", variable=optPurgeStr, onvalue="/PURGE ", offvalue="")
optPurge.grid(row = 0, column = 1, padx = 10)

optExcludeNewer = customtkinter.CTkCheckBox(master=optionsFrame, text="Exclude Newer Files in Dest", variable=optNewerStr, onvalue="/XN", offvalue="")
optExcludeNewer.grid(row = 0, column = 2, padx = 10)

excludeLabel = customtkinter.CTkLabel(master=optionsFrame, text="Exclude:", anchor="e", justify ="right")
excludeLabel.grid(row = 2, column = 0, sticky = "e")

excludeField = customtkinter.CTkEntry(master=optionsFrame, width=300, textvariable=excludeStr)
excludeField.grid(row = 2, column = 1, columnspan = 2)

excludeHelpButton = customtkinter.CTkButton(master=optionsFrame, text="ExcludeHelp", command=excludeHelp)
excludeHelpButton.grid(row = 2, column = 3, sticky = "w")

#Results Setup
resultTextbox = customtkinter.CTkTextbox(master=outputFrame, width=700)
resultTextbox.pack(anchor = "w")

copyButton = customtkinter.CTkButton(master=outputFrame, text="Copy Result", command=copyResultStr)
copyButton.pack(anchor = "center")

#endregion
root.mainloop()