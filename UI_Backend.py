"""
this code is the back end of the UI when buttons,checkbox ect are clicked or changed
"""
#from UI import show_frame_page
#import the UI to import the current_default settings acting like a global var
import UI
import tkinter as tk
import os
import sys
import threading
from tkinter import colorchooser
from tkinter import messagebox, ttk

from QR_generation import color_qr
from QR_detection import write_data
from QR_detection import start_video_feed
from QR_detection import number_picker
from QR_detection import count
from QR_detection import create_csv
from QR_detection import decrease_value
#from QR_detection import clicked_Undo_button
import QR_detection
 

def generate_folder_name():
    folder_name = "all_snapshots"
    os.makedirs(folder_name, exist_ok=True)
    return folder_name

def Entry_Changed(event,key_name,entry):
    #global current_default
    new_text = entry.get()
    UI.current_default[key_name] = entry.get()
    #print("current_default changed:",UI.current_default)

def Spinbox_changed(value,key_name):
    #global current_default
    #size_reduce cant be dviced by zero cause of scren 
    UI.current_default[key_name]= value
    #print("current_default changed:",UI.current_default)


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

# this is a custom color when click on color button it will change color 
#this creates a list of the button of color picker
def custom_button_UI(button, number):
    global current_default
    color_code = colorchooser.askcolor(title="Choose color")
    if str(color_code) == "(None, None)":
        return
    #print("rgb"+str(color_code[0]))    
    button_style = ttk.Style()
    button_style.configure(f"{button}.TButton", background= str(color_code[1])  )  # Change background color of the button
    button.configure(style=f"{button}.TButton")  # Change the style of the button to 'CustomButtonRed'
    UI.current_default["qr_color"][number] = color_code[0]

#the number 2 is the seaction of the manual selection of positions
def custom_button_UI_2(button, number):
    number_picker(button, number)
    #pass




# this is the button function
def Button_pressed(button,frame = None , width= None, height= None ):
    global clicked_skipped_button ,clicked_Undo_button
    #global current_default
    #print("button",button)
    File_Default_name = "Settings.json"
    # button = ttk.Button(frame, text="Button", command=lamb3da: show_frame_page(frame2 if frame == frame1 else frame1))

    if button == "Next":
        print("next button")
        QR_detection.clicked_skipped_button = True

    if button == "undo":
        if QR_detection.count <= 0:
            print("this is less this",QR_detection.count)
            return
        else:
            QR_detection.clicked_Undo_button = True

        print("undo")

    if button == "-":

       # print("minuse sign",UI.current_default['minuse'])

        decrease_value(UI.current_default['minuse'])
        #print("- sign")

    if button == "ok":
        print("ok")
        QR_detection.result = float(UI.current_default["Measurement"])

    if button == "canceled":
        print("calceled")


    #y, x
    if button == "Previous page":
        UI.show_frame_page(UI.frame1,1065,260)

    if button == "Next Page":
        UI.show_frame_page(UI.frame2, 290, 268)

    if button == "Test page":
        print("test page")
        UI.show_frame_page(UI.frame3, 600, 35)

    if button == "Save All Default":
        write_data(File_Default_name, UI.current_default)
    if button == "Video Selected":
        QR_detection.create_csv()

        file_paths = tk.filedialog.askopenfilenames(filetypes=[("All Files", "*.*")])
        file_paths = list(file_paths)
        #UI.show_frame_page(UI.frame4, 292, 70)
        video_thread = threading.Thread(target=start_video_feed, args=(file_paths,))
        video_thread.start()


        print("this code ened")
        #start_video_feed(file_paths)


    if button == "Camera Selected":
        pass
    if button == "Generate":
        creat_tags()
    if isinstance(button, int):
        print("Variable is an integer")
