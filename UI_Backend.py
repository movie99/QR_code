"""
this code is the back end of the UI when buttons,checkbox ect are clicked or changed
"""
#from UI import show_frame_page
#import the UI to import the current_default settings acting like a global var
import UI
import tkinter as tk
import os
import sys


from QR_generation import color_qr
from QR_detection import write_data


def generate_folder_name():
    folder_name = "all_snapshots"
    os.makedirs(folder_name, exist_ok=True)
    return folder_name


def Entry_Changed(event,key_name,entry):
    #global current_default
    new_text = entry.get()
    UI.current_default[key_name] = entry.get()
    print("current_default changed:",UI.current_default)

def Spinbox_changed(value,key_name):
    #global current_default
    #size_reduce cant be dviced by zero cause of scren 
    UI.current_default[key_name]= value
    print("current_default changed:",UI.current_default)

def CheckButton_changed(event ,value):
    #global current_default
    UI.current_default[value]= event
    #print(type(event))
    if event == True:
        #print("True")
        generate_folder_name()
    #print(event , value)

# Define a function to create a list of values for the Spinbox widget
def create_spinbox_values(value):
    start, stop, step, current = value
    return [round(i * step + start, 1) for i in range(int((stop - start) / step) + 1)]

def spinbox_changed(value):
   #print("Spinbox Value Changed:", value)
    UI.current_default["skip_sec"] = float(value)

# Define a function to create a list of values for the Spinbox widget


def combobox_changed(event):
    #global current_default
    #print("Selection changed to index:", event.widget.current())
    UI.current_default['qr_family']['Option_Num'] = event.widget.current()

def creat_tags():
    #global NTAGS
   # global current_default
    qr_family_Option_NUM = UI.current_default["qr_family"]['Option_Num']
    filename  = UI.current_default["set_file_name"]+ str(".svg")  # Default filename (.svg, .png, .jpeg or .pgm)
    family    =  UI.current_default['qr_family']['Option'][qr_family_Option_NUM]
    color_qr(filename , family , UI.current_default["qr_color"], UI.current_default["qr_size"])


# this is the button function
def Button_pressed(button, frame = None):
    #global current_default
    #print("button",button)
    File_Default_name = "Settings.json"
    # button = ttk.Button(frame, text="Button", command=lambda: show_frame_page(frame2 if frame == frame1 else frame1))
    if button in ["Next Page","Previous page"]:
        print("next pages activated")
        frame.tkraise()
    if button == "Save All Default":
        write_data(File_Default_name, UI.current_default)
    if button == "Video Selected":
        file_paths = tk.filedialog.askopenfilenames(filetypes=[("All Files", "*.*")])
        file_paths = list(file_paths)
        start_video_feed(file_paths)
    if button == "Camera Selected":
        pass
    if button == "Generate":
        creat_tags()
    if isinstance(button, int):
        print("Variable is an integer")
