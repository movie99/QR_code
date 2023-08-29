#note to programmer

#bugs

#packages needed 
#sudo apt-get install python3-pil python3-pil.imagetk
#sudo apt install python3-pip
#sudo apt-get install python3-tk

#pip install opencv-python
#pip install pupil-apriltags
#pip install svgwrite
#pip install Pillow


# add a undo 
# add the ten colors in the new video feed for manual 
#add a next button on corner left 
# add color detect 
# add a new threshold for uppper and lower 
#add a convertsion rate to pexels to cm not inches matric system 
# when starting add the first 3 location of the stick and a pop up on middle of screen 
#


#adding notes change the time via start video 




# need to fix the Spinbox input cause not saving so i decided to disabled at the moment 

# need to fix the Default_settings to INT and not only float 

# need to add  window.columnconfigure towards end of forr loop instead of manulay placing them





#credit 

#https://github.com/Kazuhito00/AprilTag-Detection-Python-Sample/blob/main/sample.py

#https://gitlab.eecs.umich.edu/wearhouse-bot/wearhouse-april/-/blob/master/apriltag_gen.py

import threading

from datetime import datetime

from functools import partial

import csv

from tkinter import messagebox, ttk

import tkinter as tk

from tkinter import *

from tkinter import filedialog

from tkinter import colorchooser

from tkinter import simpledialog, messagebox

import time

import os

import threading 

import base64

import io

import math

import struct

import json

import os

import sys

#cv2 outside lib
import cv2

import time

import copy

import ast

#save data



#https://towardsdatascience.com/lightning-fast-video-reading-in-python-c1438771c4e6

#from decord import VideoReader

#from decord import cpu, gpu

#New_Custom imports pip install 

from PIL import Image as pil_image

from PIL import Image, ImageTk

import numpy as np, svgwrite


import cv2 as cv
#https://pupil-apriltags.readthedocs.io/en/stable/api.html

#puppil with opencv2
#https://github.com/Kazuhito00/AprilTag-Detection-Python-Sample/blob/main/README_EN.md
from pupil_apriltags import Detector



#import svgwrite


#one bug i needed to convert all into floats only read float input at the moment

#this is the default setting for the UI

Default_settings = {

        "qr_family":{"Option":["tag16h5","tag25h9","tag36h11"], "Option_Num":1},

        "set_file_name":"qrcode2",

        "tag_generate":10.0,

        "qr_color":{} ,

        "qr_size": 1.0,

        "color_detect": False,

        "nthreads":1.0,

        "quad_decimate":2.0,

        "quad_sigma":0.0,

        "refine_edges":1.0,

        "decode_sharpening":1.0,

        "debug":0.0,

        "size_reduced":4.0,

        "set_data_file_name":"bird_data",

        "data_header":['Treatment', 'Group', 'Video_date', 'Snapshot_', 'Neighbor_1', "Neighbor_2", "Distance_cm", "block","half"],

        "data_format":"['Young', '1', 'day,month,year', 'Snapshot_', 'Neighbor_1', 'Neighbor_2', 'Distance_cm', 'block','half']",

        "skip_sec":180.0,

        "qr_keys":"[0,1,2,3]",

        "Save_Snapshot":False,

}



# this is your current default settings stored in memory

current_default = {

    

}



#this is an image in hex string

image_base64string = """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

"""



#check if file exits if not create it and dump Default_settings

def read_file(file_path):

    # Check if the file exists

    if os.path.exists(file_path):

        # Open the file and read its contents

        with open(file_path, 'r') as file:

            content = file.read()

            return content

        file.close()  # Close the file after reading its contents

    else:

        # Create the file if it doesn't exist

        with open(file_path, 'w') as file:

            initial_content = Default_settings

            initial_content_str = json.dumps(initial_content)

            file.write(initial_content_str)

        file.close()

        return initial_content_str



def generate_folder_name():
    folder_name = "all_snapshots"
    os.makedirs(folder_name, exist_ok=True)
    return folder_name


#check if file exits and add content

def write_data( filename , data):



    # check file extension

    extension = filename.split(".")[-1]

    

    if extension == "json":

        with open(filename, "w") as f:

            json.dump(data, f)



    elif extension == "csv":

        # convert data to string if it's not already

        if not isinstance(data, str):

            data = str(data)

        

        # parse string to list using ast.literal_eval

        my_data = ast.literal_eval(data)

        

        # write data to csv file

        with open(filename, "a", encoding='UTF8', newline='') as f:

            #print("my_data",my_data)

            #writer = csv.writer(f)

            #writer.writerow(my_data)
            pass

    else:

        print("Unsupported file extension")









def check_File_Settings():

    global current_default

    File_Default_name = "Settings.json"

    current_default = json.loads(read_file(File_Default_name))

    #print("current_default",current_default)


#this is the buttion function 
def Button_pressed(button):

    global current_default


    #print("button",button)

    #print("i been pressed",button)

    File_Default_name = "Settings.json"

    if button == "Save All Default":

        write_data(File_Default_name,current_default)
    
        pass

        

    if button == "Video Selected":

        file_paths = tk.filedialog.askopenfilenames(filetypes=[("All Files", "*.*")])

    # Start the video feed for each selected file

        file_paths = list(file_paths)

        #print("file_paths",file_paths)

        start_video_feed(file_paths)

    if button == "Camera Selected":

        pass

    if button == "Generate":

        #print("generate")

        creat_tags()

    # if number button is detected then call the change color detection    
    if isinstance(button, int):
        print("Variable is an integer")


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

    current_default["qr_color"][number] = color_code[0]
    
    #print(current_default["qr_color"])



  


def Entry_Changed(event,key_name,entry):

    global current_default

    new_text = entry.get()

    current_default[key_name] = entry.get()




def Spinbox_changed(value,key_name):

    global current_default

    #size_reduce cant be dviced by zero cause of scren 

    current_default[key_name]= value



def combobox_changed(event):

    global current_default

    #print("Selection changed to index:", event.widget.current())

    current_default['qr_family']['Option_Num'] = event.widget.current()


def CheckButton_changed(event ,value):
    global current_default

    current_default[value]= event
    #print(type(event))
    if event == True:
        #print("True")
        generate_folder_name()
    #print(event , value)



# Define a function to create a list of values for the Spinbox widget

def create_spinbox_values(value):

    start, stop, step, current = value

    return [round(i * step + start, 1) for i in range(int((stop - start) / step) + 1)]


#setting for tkinter

window = tk.Tk()

color_background = "#8c0b42"

window.configure(bg=color_background)

window.title("NMSU Bird research")



style = ttk.Style()

style.theme_create("New_Custom", parent="alt", settings={

    "TLabel": {"configure": {"foreground": "#FFFFFF", "background": "#8c0b42" , "font":("Comic Sans MS", 13, "bold")}},

    "TSpinbox": {"configure": {"arrowsize":20,"selectbackground": "#858282", "fieldbackground": "white", "background": "#FFFFFF", "font":("Comic Sans MS", 13, "bold"), "width": 5}},

    "TEntry": {"configure": {"foreground": "#858282", "background": "#FFFFFF" , "font":("Comic Sans MS", 13, "bold")}},

    "TButton": {

            "configure": {

                "foreground": "white",

                "background": "black",

                "font": ("Comic Sans MS", 13, "bold"),

                "bordercolor": "red",    # set border color

                "borderwidth": 2,        # set border width

                "pressedcolor": "white",  # set pressed color

            },

            "map": {


                "background": [("active", "!disabled", "pressed", "#8c0b42"), 

                               ("active", "!disabled", "pressed", "!focus", "white"),

                               ("active", "!disabled", "!pressed", "black"),

                               ("active", "!disabled", "!pressed", "!focus", "black")],

                "foreground": [("active", "!disabled", "pressed", "white"),

                               ("active", "!disabled", "!pressed", "white")],

                "bordercolor": [("active", "!disabled", "pressed", "gray"),

                                ("active", "!disabled", "!pressed", "red")]

            }

        },

    "TCombobox": {"configure": {"arrowsize":20,"foreground": "#white","font":("Comic Sans MS", 13, "bold")}},

    "TLabel2":{"configure": {"foreground": "#FFFFFF", "background": "#8c0b42" , "font":("Comic Sans MS", 13, "bold")}}

})

style.theme_use("New_Custom")


#this function will display the ui 
def UI_Design():

    global current_default

    path_icon = PhotoImage(data = image_base64string) 

    image_bytes = base64.b64decode(image_base64string)

    img = pil_image.open(io.BytesIO(image_bytes))

    resized_image = img.resize((64, 70), pil_image.LANCZOS)  

    #print("running")

    new_image= ImageTk.PhotoImage(resized_image)

    hex_str = "44 45 56 20 61 6C 65 78 30 32 40 6E 6D 73 75 2E 65 64 75"

    string = bytes.fromhex(hex_str).decode('utf-8')

    #This is New_Custom themes for tkinter

   


    #All Labels for UI and IMAGE

    All_Labels = {

        "IMAGE":{ "image":new_image,"style":'New_Custom.TLabel', "row":0, "column":0 ,"sticky":"nsew"},



        "QR gen and Type":{ "style":'New_Custom.TLabel', "row":0, "column":1 ,"sticky":"nsew"},

        "QR Settings":{ "style":'New_Custom.TLabel', "row":0, "column":3 ,"sticky":"nsew"},

        "Save & Start":{ "style":'New_Custom.TLabel', "row":0, "column":5 ,"sticky":"nsew"},



        "QR Type Family":{ "style":'New_Custom.TLabel', "row":1, "column":0 ,"sticky":"nsew"},

        "Set File Name":{ "style":'New_Custom.TLabel', "row":2, "column":0 ,"sticky":"nsew"},

        "Tags Generate":{ "style":'New_Custom.TLabel', "row":3, "column":0 ,"sticky":"nsew"},

        "color picker":{ "style":'New_Custom.TLabel', "row":4, "column":0 ,"sticky":"nsew"},

        "color detect":{ "style":'New_Custom.TLabel', "row":5, "column":0 ,"sticky":"nsew"},

        "qr size":{ "style":'New_Custom.TLabel', "row":6, "column":0 ,"sticky":"nsew"},



        "nthreads":{ "style":'New_Custom.TLabel', "row":1, "column":2 ,"sticky":"nsew"},

        "Quad decimage":{ "style":'New_Custom.TLabel', "row":2, "column":2 ,"sticky":"nsew"},

        "Quad sigma":{ "style":'New_Custom.TLabel', "row":3, "column":2 ,"sticky":"nsew"},

        "refined edges":{ "style":'New_Custom.TLabel', "row":4, "column":2 ,"sticky":"nsew"},

        "decode sharpening":{ "style":'New_Custom.TLabel', "row":5, "column":2 ,"sticky":"nsew"},

        "debug":{ "style":'New_Custom.TLabel', "row":6, "column":2 ,"sticky":"nsew"},



        "size_reduced":{ "style":'New_Custom.TLabel', "row":1, "column":4 ,"sticky":"nsew"},

        "Save File Name":{ "style":'New_Custom.TLabel', "row":2, "column":4 ,"sticky":"nsew"},

        "Data Format":{ "style":'New_Custom.TLabel', "row":3, "column":4 ,"sticky":"nsew"},

        "skip_sec":{ "style":'New_Custom.TLabel', "row":4, "column":4 ,"sticky":"nsew"},

        "Simultaneous QR detection":{ "style":'New_Custom.TLabel', "row":5, "column":4 ,"sticky":"nsew"},

        "Save Snapshots":{ "style":'New_Custom.TLabel', "row":6, "column":4 ,"sticky":"nsew"},

        "Save Settings ":{ "style":'New_Custom.TLabel', "row":7, "column":4 ,"sticky":"nsew"},

        "Select Vid":{ "style":'New_Custom.TLabel', "row":8, "column":4 ,"sticky":"nsew"},


    } 



    #"qr_family":{0:["tag16h5","tag25h9","tag36h11"]},



    ALL_Combobox = {

        #"default":{"Option":["Option 1", "Option 2", "Option 3"],"row":1, "column":1 ,"sticky":"nsew"}



        "qr_family":{ "Option":["tag16h5","tag25h9","tag36h11"], "Option_Num":0, "row":1, "column":1 ,"sticky":"nsew" }

 

    }



    #this is All Entry the first key is the data textvariable

    All_Entry = {

        #Default_settings["qr_family"]:{ "style":'New_Custom.TEntry', "row":2, "column":1 ,"sticky":""},

        "set_file_name":{ "style":'New_Custom.TEntry', "row":2, "column":1 ,"sticky":"nsew"},

        #"size_reduced":{ "style":'New_Custom.TEntry', "row":1, "column":5 ,"sticky":"nsew"},

        "set_data_file_name":{ "style":'New_Custom.TEntry', "row":2, "column":5 ,"sticky":"nsew"},

        "data_format":{ "style":'New_Custom.TEntry', "row":3, "column":5 ,"sticky":"nsew"},  

        "qr_keys":{ "style":'New_Custom.TEntry', "row":5, "column":5 ,"sticky":"nsew"},  

    } 





    #may need to add the tuple to the default settings instead

    All_Spinbox= {

        "tag_generate":{ "start_stop_setp":(0, 11.0, 1.0,1),"style":'New_Custom.TSpinbox', "row":3, "column":1 ,"sticky":"nsew",},

        "nthreads":{  "start_stop_setp":(0, 10.0, 1.0,1),"style":'New_Custom.TSpinbox', "row":1, "column":3 ,"sticky":"nsew"},

        "quad_decimate":{  "start_stop_setp":(0, 30.0, 0.1,1.0),"style":'New_Custom.TSpinbox', "row":2, "column":3 ,"sticky":"nsew"},

        "quad_sigma":{  "start_stop_setp":(0, 30.0, 0.1,1.0),"style":'New_Custom.TSpinbox', "row":3, "column":3 ,"sticky":"nsew"},

        "refine_edges":{ "start_stop_setp":(0, 11.0, 1.0, 1), "style":'New_Custom.TSpinbox', "row":4, "column":3 ,"sticky":"nsew"},  

        "decode_sharpening":{  "start_stop_setp":(0, 30.0, 0.1,1.0),"style":'New_Custom.TSpinbox', "row":5, "column":3 ,"sticky":"nsew"}, 

        "debug":{  "start_stop_setp":(0, 30.0, 0.1,1.0),"style":'New_Custom.TSpinbox', "row":6, "column":3 ,"sticky":"nsew"}, 

        "size_reduced":{ "start_stop_setp":(1, 3000.0, 1.0,1.0), "style":'New_Custom.TSpinbox', "row":1, "column":5 ,"sticky":"nsew"},

        "skip_sec":{  "start_stop_setp":(0, 3000.0, 1.0,1.0),"style":'New_Custom.TSpinbox', "row":4, "column":5 ,"sticky":"nsew"}, 

        "qr_size":{  "start_stop_setp":(0, 30.0, 0.1,1.0),"style":'New_Custom.TSpinbox', "row":6, "column":1 ,"sticky":"nsew"}, 

    }



    All_button={

        "Save All Default":{ "style":'New_Custom.TButton',   "row":7, "column":5 ,"sticky":"nsew"},

        "Video Selected":  {  "style":'New_Custom.TButton',  "row":8, "column":5 ,"sticky":"nsew"},

       # "Camera Selected": { "style":'New_Custom.TButton',   "row":7, "column":5 ,"sticky":"nsew"},

        "Generate":        { "style":'New_Custom.TButton',   "row":7, "column":1 ,"sticky":"nsew"}

    }

    All_Check_Box = {

        "Save_Snapshot":{ "style":'New_Custom.TButton', "row":6, "column":5 ,"sticky":"nsew"},

        "color_detect":{ "style":'New_Custom.TButton', "row":5, "column":1 ,"sticky":"nsew"},
    }


    #this is a custom function i build it build a horizaonta list of buttons ingore this 
    custom_lists_buttons = {

        "color_detect":{ "style":'New_Custom.TButton', "amount_of_buttons":10, "row":4, "column":1 ,"sticky":"nsew"},

   
    }


    # create labels

    for key, value in All_Labels.items():

        if "image" in value:

            label = ttk.Label(window ,image=value["image"],style=value['style'])

            label.grid(row=value["row"], column=value["column"], sticky=value["sticky"])

            #print("this is ture")

        else:

            label = ttk.Label(window, text=key, style=value['style'])

            label.grid(row=value["row"], column=value["column"], sticky=value["sticky"])

      

    # create entries

    for key, value in All_Entry.items():

        key_name = key

        key = current_default[str(key)]

        entry = ttk.Entry(window, textvariable=key, style=value['style'])

        entry.grid(row=value["row"], column=value["column"], sticky=value["sticky"])

        entry.bind("<KeyRelease>",lambda event, m=key_name,c=entry: Entry_Changed(event, m, c))

        entry.insert(0, key)





    # create spinboxes

    for key, value in All_Spinbox.items():

        key_name = key

        key = current_default[str(key)]

        selected_value = tk.DoubleVar(value=key)

        spinbox = ttk.Spinbox(window, values=create_spinbox_values(value["start_stop_setp"]),textvariable=selected_value, style=value["style"],command=lambda c=key_name, m=selected_value: Spinbox_changed(m.get(),c),state="readonly")

        spinbox.grid(row=value["row"], column=value["column"], sticky=value["sticky"])

        window.columnconfigure(value["column"], weight=1)



    #creates buttons

    for key, value in All_button.items():

        button = ttk.Button(window, text=key, style=value["style"],command=lambda m=key: Button_pressed(m))

        button.grid(row=value["row"], column=value["column"], sticky=value["sticky"])



    # create comboboxes

    for key, value in ALL_Combobox.items():

        combobox = ttk.Combobox(window, values=value["Option"], state="readonly")

        combobox.grid(row=value["row"], column=value["column"], sticky=value["sticky"])

        combobox.bind("<<ComboboxSelected>>", combobox_changed)

        combobox.current(current_default['qr_family']['Option_Num'])


    for key, value in All_Check_Box.items():

        key_name = key

        key = current_default[str(key)]

        #selected_value = tk.DoubleVar(value=key)

        #spinbox = ttk.Spinbox(window, values=create_spinbox_values(value["start_stop_setp"]),textvariable=selected_value, style=value["style"],command=lambda c=key_name, m=selected_value: Spinbox_changed(m.get(),c),state="readonly")
        var2 = tk.BooleanVar(value=current_default['Save_Snapshot'])
        spinbox = tk.Checkbutton(window, onvalue=True, offvalue=False, variable=var2, command=lambda c=key_name, m=var2: CheckButton_changed(m.get(), c))

        spinbox.grid(row=value["row"], column=value["column"], sticky=value["sticky"])

        window.columnconfigure(value["column"], weight=1)  

    #custom colors horizontal list button 
    #total_buttons = len(buttons_list)  # Total number of buttons
    # custom colors horizontal list button

    # total_buttons = len(buttons_list)  # Total number of buttons

  
    #NW work good
    
   # button_style = ttk.Style()
    #button_style.configure(f"{button}.TButton", background= str(color_code[1])  )  # Change background color of the button


    print(current_default["qr_color"])
    for key, value in custom_lists_buttons.items():
        for i in range(0,10):
            button_style = f"Button{i}"+".TButton"
            color = current_default['qr_color'].get(str(i), [0,0,0])
            # Convert the RGB values to hexadecimal format
            hex_color = '#%02x%02x%02x' % (color[0], color[1], color[2])

            style = ttk.Style()
            style.configure(button_style, background=hex_color)

            button2 = ttk.Button(window, text=f"{i}", style=button_style)
            button2.configure(command=lambda btn=button2, idx=i: custom_button_UI(btn, idx))
            button2.grid(row=value["row"], column=value["column"], sticky="NW", ipadx=5, ipady=0, padx=i * 15, pady=0)

  


    label = ttk.Label(window, text=string, style="New_Custom.TLabel")

    label.grid(row=8, column=0, sticky="nsew")



    window.iconphoto(False, new_image)

    window.columnconfigure(0, weight=1)

    window.columnconfigure(1, weight=1)

    window.columnconfigure(2, weight=1)

    window.columnconfigure(3, weight=1)

    window.columnconfigure(4, weight=1)

    window.columnconfigure(5, weight=1)

    window.mainloop()







#this current code found in 

#https://gitlab.eecs.umich.edu/wearhouse-bot/wearhouse-april/-/blob/master/apriltag_gen.py


def color_qr(filename , family , color, size):
    #filename = 'test.svg'  # Default filename (.svg, .png, .jpeg or .pgm)
    #family = 'tag16h5'   # Default tag family (see tag_families)
    NTAGS = 10          # Number of tags to create
    TAG_PITCH = 10          # Spacing of tags
    WHITE = 0         # White color (0 is black)

    #thic piece of code will convert str(int) in acually real int on dict 
    #dict cant store real int as keys cause of hash
    color = {int(key): value for key, value in color.items()}
    # this converts all list to tuples
    for key in color:
        color[key] = tuple(color[key])

    print("this is color: ",color)

    DEFAULT_COLOR = 'rgb(0, 0, 0)'  # Default color for QR codes

    tag16h5 =  16, 5, (0x231b, 0x2ea5, 0x346a, 0x45b9, 0x79a6,
                      0x7f6b, 0xb358, 0xe745, 0xfe59, 0x156d)
    tag25h9 = 25, 9, (0x155cbf1, 0x1e4d1b6, 0x17b0b68, 0x1eac9cd, 0x12e14ce,
                      0x3548bb, 0x7757e6, 0x1065dab, 0x1baa2e7, 0xdea688)
    tag36h11 = 36, 11, (0xd5d628584, 0xd97f18b49, 0xdd280910e, 0xe479e9c98, 0xebcbca822,
                       0xf31dab3ac, 0x056a5d085, 0x10652e1d4, 0x22b1dfead, 0x265ad0472)
    tag_families = {"tag16h5": tag16h5, "tag25h9": tag25h9, "tag36h11": tag36h11}

    def set_graphics(fname, family):
        global FTYPE, IMG_WD, IMG_HT, SCALE, DWG_SIZE, VIEW_BOX
        FTYPE = fname.split('.')[-1].upper()
        FTYPE = FTYPE.replace("PGM", "PPM").replace("JPG", "JPEG")
        IMG_HT = int(math.sqrt(family[0])) + 6
        IMG_WD = (NTAGS - 1) * TAG_PITCH + IMG_HT

        if FTYPE == "SVG":
            SCALE = size
            DWG_SIZE = "%umm" % (IMG_WD * SCALE), "%umm" % (IMG_HT * SCALE)
            VIEW_BOX = "0 0 %u %s" % (IMG_WD, IMG_HT)
        else:
            SCALE = 10

    #gen tag
    def gen_tag(tag, val):
        area, minham, codes = tag
        dim = int(math.sqrt(area))
        d = np.frombuffer(np.array(codes[val], ">i8"), np.uint8)
        bits = np.unpackbits(d)[-area:].reshape((-1, dim))
        bits = np.pad(bits, 1, 'constant', constant_values=0)
        return np.pad(bits, 2, 'constant', constant_values=1)

    #save bitmpa
    def save_bitmap(fname, arrays):
        img = Image.new('L', (IMG_WD, IMG_HT), WHITE)
        for i, a in enumerate(arrays):
            t = Image.fromarray(a * WHITE)
            img.paste(t, (i * TAG_PITCH, 0))
        img = img.resize((IMG_WD * SCALE, IMG_HT * SCALE))
        img.save(fname, FTYPE)

    def save_vector(fname, arrays):
        qr_codes = {}  # Dictionary to store QR codes and colors
        dwg = svgwrite.Drawing(fname, DWG_SIZE, viewBox=VIEW_BOX, debug=False)
        for i, a in enumerate(arrays):
            fill_color = color.get(i, DEFAULT_COLOR)
            qr_codes[i] = fill_color  # Store QR code index and color
            g = dwg.g(stroke='none', fill=f"rgb{fill_color}")
            for dy, dx in np.column_stack(np.where(a == 0)):
                g.add(dwg.rect((i * TAG_PITCH + dx, dy), (1, 1)))
            dwg.add(g)
        dwg.save(pretty=True)
        return qr_codes

    opt = None
    for arg in sys.argv[1:]:
        if arg[0] == "-":
            opt = arg.lower()
        else:
            if opt == '-f':
                family = arg
            else:
                filename = arg
            opt = None
    if family not in tag_families:
        print("Unknown tag family: '%s'" % family)
        sys.exit(1)
    tagdata = tag_families[family]
    set_graphics(filename, tagdata)
    print("Creating %s, file %s" % (family, filename))
    tags = [gen_tag(tagdata, n) for n in range(0, NTAGS)]
    qr_codes = {}  # Dictionary to store all QR codes and colors
    if FTYPE == "SVG":
        qr_codes = save_vector(filename, tags)
    else:
        save_bitmap(filename, tags)







#"qr_family":{"Option":["tag16h5","tag25h9","tag36h11"], "Option_Num":0},

def creat_tags():

    global NTAGS

    global current_default

    qr_family_Option_NUM = current_default["qr_family"]['Option_Num']

    filename  = current_default["set_file_name"]+ str(".svg")  # Default filename (.svg, .png, .jpeg or .pgm)

    family    =  current_default['qr_family']['Option'][qr_family_Option_NUM]

    #NTAGS     = int(current_default["tag_generate"])       # Number of tags to create

    color_qr(filename , family , current_default["qr_color"], current_default["qr_size"])




#check if file exits owtherwise add content

def create_csv():

    if not os.path.exists(current_default["set_data_file_name"]+".csv"):

        # file does not exist, so create it

        with open(current_default["set_data_file_name"]+".csv", 'w', encoding='UTF8',  newline='') as f:

            writer = csv.writer(f)

            writer.writerow(current_default['data_header'])

            #return


def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance

def calculate_distances_and_save_to_csv(data, output_file):
    #global counter
    # Create a dictionary to map numbers to letters
    
    #data = data['0']
    data[str(count)].pop("Dont_Display_Num")
    print('data',data)
    number_to_letter = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I'}
    distances = []
    #current_default['data_format']
    data_list = ast.literal_eval(current_default['data_format'])
   
    for key1, values1 in data.items():
        for key2, points2 in values1.items():
            for key3, points3 in values1.items():
                if key2 < key3:
                    tag1 = f"1{number_to_letter[int(key2)]}"
                    tag2 = f"1{number_to_letter[int(key3)]}"
                    distance = calculate_distance(points2, points3)
                    
                    # Convert pixels to actual measurements
                    #pixels_to_cm_ratio = pixels_to_cm_ratio / length_in_pexels
                    calculated_distance_cm = distance * length_in_pexels
                    distances.append([data_list[0], count, data_list[2], tag1, tag2, f"{calculated_distance_cm:.0f}"])
    #print(output_file)
    # Save the distances to a CSV file
    file_exists = os.path.isfile(output_file)

    with open(output_file, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        if not file_exists:
            csvwriter.writerow(['Control', 'Snapshot', 'date', 'Source Key', 'Target Key', 'Distance'])
        csvwriter.writerows(distances)

    print(f"Distances saved to '{output_file}'.")


"""
    for key1, values1 in data.items():
        for key2, points2 in values1.items():
            for key3, points3 in values1.items():
                if key2 < key3:  # Check if the pair has not been calculated in reverse order
                    tag1 = f"1{number_to_letter[key2]}"
                    tag2 = f"1{number_to_letter[key3]}"
                    distance = calculate_distance(points2, points3)

                    #convert pexels to acual measerments
                    pixels_to_cm_ratio = pixels_to_cm_ratio / length_in_pexels

                    distances.append([data_list[0], copy.deepcopy(counter), data_list[2], tag1, tag2, f"{distance * pixels_to_cm_ratio:.0f}"])
"""


#data = {
#    0: {4: [1154, 1423], 6: [1849, 1422], 7: [660, 1335], 5: [1840, 1432]},
    # Add other dictionaries as needed
#}

#output_file = 'distances.csv'
#calculate_distances_and_save_to_csv(data, output_file)





#Snapshot_tick = 0
file_name = ""

def change_color(tag_id, tag_colors):
    # Convert dictionary values to tuples
    color = {int(key): tuple(value) for key, value in tag_colors.items()}
    if tag_id in color:
        return color[tag_id]
    else:
        return None

#all_data_entry = {}


#this draw the tags and even save it to the Final_All_data_saved
def draw_tags( image,tags):          
    #global Current_ALL_data_saved , all_data_entry , Final_All_data_saved
    global Final_All_data_saved 
    #if count < 0:
    #    count = 0

    t = datetime.now()

    families = current_default['qr_family']['Option'][current_default["qr_family"]['Option_Num']]

    for tag in tags:
        #this will remove the tags if pressed buttons and will distaply any manual pressed
        if str(tag.tag_id) in str(Final_All_data_saved[str(count)]["Dont_Display_Num"]):

            continue

        if tag.tag_id > 10:
            #print("Condition met for tag:", tag)
            return image

        # Do something here if the condition is met
        tag_family = tag.tag_family
        tag_id = tag.tag_id
        center = tag.center
        corners = tag.corners
        center = (int(center[0]), int(center[1]))
        corner_01 = (int(corners[0][0]), int(corners[0][1]))
        corner_02 = (int(corners[1][0]), int(corners[1][1]))

        corner_03 = (int(corners[2][0]), int(corners[2][1]))

        corner_04 = (int(corners[3][0]), int(corners[3][1]))

        cv2.circle(image, (center[0], center[1]), 5, (0, 0, 255), 2)

        cv2.line(image, (corner_01[0], corner_01[1]),(corner_02[0], corner_02[1]), (255, 0, 0), 2)

        cv2.line(image, (corner_02[0], corner_02[1]),(corner_03[0], corner_03[1]), (255, 0, 0), 2)

        cv2.line(image, (corner_03[0], corner_03[1]),(corner_04[0], corner_04[1]), (0, 255, 0), 2)

        cv2.line(image, (corner_04[0], corner_04[1]),(corner_01[0], corner_01[1]), (0, 255, 0), 2)

        # Define text string to display

        #text = str(tag_family) + ':' + str(tag_id) + ' (' + str(center[0]) + ',' + str(center[1]) + ')'
        text = str(tag_id) + ' (' + str(center[0]) + ',' + str(center[1]) + ')'

        # Display text with larger font size and thicker stroke

        font = cv2.FONT_HERSHEY_SIMPLEX

        font_scale = 3

        thickness = 10

        #print(tag_id)

        #color = (0, 255, 0)

        color = change_color(tag_id, current_default["qr_color"])

        text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)

        cv2.putText(image, text, (corner_01[0], corner_01[1] - 10 - text_size[1]), font, font_scale, color, thickness, cv2.LINE_AA)


        width = abs(corner_01[0] - corner_02[0])

        height = abs(corner_01[1] - corner_04[1])

        #print("Final_All_data_saved", Final_All_data_saved[])
        Final_All_data_saved[str(count)][str(tag_id)] = [center[0], center[1]]
    #this will display the manual numbers
    for number in Final_All_data_saved[str(count)]["Dont_Display_Num"]:        
        #loop thour each dont Display num and chow the draw circles if placed manully
        if number in Final_All_data_saved[str(count)]:
            Manual_cordinates = Final_All_data_saved[str(count)][str(number)]
            x = Manual_cordinates[0]
            y = Manual_cordinates[1]
            current_color = change_color(int(number), current_default["qr_color"])
            cv2.circle(image, (x, y), 25, current_color, 2)
            cv2.putText(image, f"({number} {x}, {y})", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 3, current_color, 10)
            #print("this is going throuth",x,y , number)



    return image 




# Callback function to handle mouse events
#draw circle is the manual way of placing the objects
def draw_circle(image, event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Draw a completely hollow circle with a smaller radius
        outer_radius = 40
        #New_tuple = [int(current_circle[0] * current_default["size_reduced"]), int(current_circle[1] * current_default['size_reduced'])]
        New_tuple = [int(x * current_default["size_reduced"]), int(y * current_default['size_reduced'])]
        
        current_button_pressed = Final_All_data_saved[str(count)]["Dont_Display_Num"][-1] 
        Final_All_data_saved[str(count)][current_button_pressed] = New_tuple


#make this a local function
#pixels_to_cm_ratio = None
#can make it work were exit the entire loop and redoing it bases on user input
#this draw the line to get the distance of the object
drawing = False
pt1 = (-1, -1)
pt2 = (-1, -1)
pixels_to_cm_ratio = 0.0
def draw_line(event, x, y, flags, img):
    #global drawing, pt1, pt2, original_img , distance , finished_line, current_num_pressed , pixels_to_cm_ratio
    global drawing, pt1, pt2, pixels_to_cm_ratio , length_in_pexels
    frame_height, frame_width, _ = img.shape
    if event == cv2.EVENT_LBUTTONDOWN:
        if not drawing:
            pt1 = (x, y)
            drawing = True
            original_img = img.copy()  # Store a copy of the original image
        else:
            pt2 = (x, y)
            drawing = False
            line_pt1 = (int(pt1[0] * current_default["size_reduced"]), int(pt1[1] * current_default["size_reduced"]))
            line_pt2 = (int(pt2[0] * current_default["size_reduced"]), int(pt2[1] * current_default["size_reduced"]))
            cv2.line(img, line_pt1, line_pt2, (0, 0, 255), 5)
            cv2.circle(img, line_pt1, 20, (255, 0, 0), 4)
            cv2.circle(img, line_pt2, 20, (255, 0, 0), 4)
            # Measurement prompt
            cv2image_resized = cv2.resize(img, (int(frame_width/int(current_default["size_reduced"])), int(frame_height/int(current_default['size_reduced']))))
            cv2.imshow('AprilTag Detect Demo', cv2image_resized)
            result = simpledialog.askfloat("Measurement", "Enter the measurement in centimeters:")
            if result is not None:
                pt1 = line_pt1
                pt2 = line_pt2
                pixels_to_cm_ratio = result
                midpoint = ((pt1[0] + pt2[0]) // 2, (pt1[1] + pt2[1]) // 2)  # Calculate midpoint using original coordinates
                cv2.putText(img, f"{pixels_to_cm_ratio:.2f} cm", midpoint, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
                drawing = True
                length_in_pexels = ((pt2[0] - pt1[0]) ** 2 + (pt2[1] - pt1[1]) ** 2) ** 0.5
                length_in_pexels = result / length_in_pexels
                print("length_in_pexels",length_in_pexels)
            else:
                drawing = False

Current_ALL_data_saved= None

def button_pressed(button_text):
    global clicked_skipped_button
    global clicked_Undo_button #, counter
    global Final_All_data_saved
    print("Button Pressed:", button_text)
    
    if button_text == "Next":
        # Get the current value from the dictionary or start with 0 if it doesn't exist
        clicked_skipped_button = True
        pass

    if button_text == "Undo":
        if count <= 0:
            print("this is less this")
            return
        else:
            clicked_Undo_button = True
        #current_button_pressed = Final_All_data_saved_History[counter]

    ##this detect if the number button have been clicked if true remove it from lists 
    #also removes it from the button text list
    if button_text in Final_All_data_saved[str(count)]["Dont_Display_Num"]:
        Final_All_data_saved[str(count)]["Dont_Display_Num"].remove(str(button_text))
        #Final_All_data_saved[str(count)].pop(str(button_text))

    elif button_text.isdigit():
        Final_All_data_saved[str(count)]["Dont_Display_Num"].append(str(button_text))
        del Final_All_data_saved[str(count)][str(button_text)]

#adding a new value via mouse it doesnt work fix
def spinbox_changed(value):
   #print("Spinbox Value Changed:", value)
    
    current_default["skip_sec"] = float(value)

#these are function that are global
clicked_skipped_button = False
clicked_Undo_button = False
Final_All_data_saved =  {}
stop_ui_thread_flag = False
Next_Frames_Capture = 0
count = 0 

def UI_video_feed(fps):
    global Next_Frames_Capture
    #print(num1)
    FPS = round(fps)
    # Create the main window
    #spin_box_skiped = current_default["skip_sec"]
   # print(current_default['qr_color'])
    window = tk.Tk()
    window.title("Button Example")

    color_background = "#8c0b42"
    window.configure(bg=color_background)

    # Create a frame to hold the buttons
    button_frame = tk.Frame(window)
    button_frame.pack(expand=True, fill="both")

    # Create ten buttons horizontally
    for i in range(0,10):
        color = current_default["qr_color"].get(str(i), [255, 255, 255])  # Get the color values for the button
        hex_color = '#%02x%02x%02x' % (color[0], color[1], color[2])  # Convert RGB to hexadecimal color
        button_text = f"{i}"
        button = tk.Button(button_frame, text=button_text, bg=hex_color, fg="black",
                           command=lambda btn_text=button_text: button_pressed(btn_text))
        button.pack(side="left", expand=True, padx=0, pady=0)

    # Create the Spinbox widget
    #spinbox_font = ("Comic Sans MS", 14)  # Change the font size
    #spinbox_padding = 5  # Adjust the padding around the Spinbox
    #spinbox = Spinbox(
    #    button_frame, from_=1, to=3600, font=spinbox_font, bd=0, relief="solid", width=10,
    #    command=lambda: spinbox_changed(spinbox.get())
    #)
    #spinbox.delete(0, tk.END)  # Clear the default value
    #spinbox.insert(tk.END, spin_box_skiped)  # Set the starting value
    #spinbox.configure(state="disabled")  # Disable the Spinbox
    #spinbox.pack(side="left", expand=True, padx=0, pady=spinbox_padding)
    # Create the two buttons and input box to replace the Spinbox

    input_frame = Frame(button_frame)
    input_frame.pack(side="left", expand=True, padx=0, pady=5)

    input_font = ("Comic Sans MS", 14)
    input_padding = 5

    input_box = Entry(input_frame, font=input_font, bd=0, relief="solid")
    input_box.insert(0, str(1))  # Set the starting value
    input_box.pack(side="left", expand=True, padx=0, pady=input_padding)

    #this will change the frame
    def decrease_value():
        global Next_Frames_Capture
        #current_value = int(input_box.get())
        #if current_value > 1:
            #input_box.delete(0, tk.END)
            #input_box.insert(0, str(current_value - 1))
        if Next_Frames_Capture == 0:
            pass 
        else:
            Next_Frames_Capture = int(Next_Frames_Capture - (FPS *  int(input_box.get())))
        
    print("Next_Frames_Capture",Next_Frames_Capture)
    #this will change the frame 
    def increase_value():
        global Next_Frames_Capture
         #pass increase_value():
        #current_value = int(input_box.get())
        #if current_value < 3600:
        #    input_box.delete(0, tk.END)
        #    input_box.insert(0, str(current_value + 1))
        if Next_Frames_Capture == 0:
            Next_Frames_Capture = int(FPS * int(input_box.get()))   
        else:
            Next_Frames_Capture = int(Next_Frames_Capture + (FPS *  int(input_box.get())))


    decrease_button = Button(input_frame, text="-", font=input_font, bd=0, relief="solid", command=decrease_value)
    decrease_button.pack(side="left", padx=5)

    #increase_button = Button(input_frame, text="+", font=input_font, bd=0, relief="solid", command=increase_value)
    #increase_button.pack(side="left", padx=5)


    


    custom_argument = "Custom Argument"
    # Create the Undo button
    undo_button = tk.Button(button_frame, text="Undo", bg="black", fg="white",
                            command=lambda: button_pressed("Undo"))
    undo_button.pack(side="left", expand=True, padx=0, pady=0)
    next_button = tk.Button(button_frame, text="Next", bg="black", fg="white",
                            command=lambda: button_pressed("Next"))
    next_button.pack(side="left", expand=True, padx=0, pady=0)

    # Start the main event loop
    if stop_ui_thread_flag == True:
        window.destroy()  # Close the main window
    else:
        window.mainloop()





#selectroi in opencv2
#also create a line in opencv2
# Function to start the video capture and display it in a frame
def start_video_feed(files):
    global clicked_skipped_button
    global clicked_Undo_button
    global Final_All_data_saved
    global stop_ui_thread_flag 
    #this keep track of the next and undo presses
    global count
    #this keep track of the frams
    global Next_Frames_Capture

    if len(files) == 0:
        #if video_window == None:
            #return
        #video_window.destroy()
        return

    File = files.pop(0)

    at_detector = Detector(

            families=current_default['qr_family']['Option'][current_default["qr_family"]['Option_Num']],

            nthreads=int(current_default["nthreads"]),

            quad_decimate=float(current_default["quad_decimate"]),

            quad_sigma=float(current_default["quad_sigma"]),

            refine_edges=int(current_default["refine_edges"]),

            decode_sharpening=float(current_default["decode_sharpening"]),

            debug=int(current_default["debug"]),    )

    # Open the video feed

    cap = cv2.VideoCapture(File)

    file_name = os.path.splitext(os.path.basename(File))[0]


    fps = cap.get(cv2.CAP_PROP_FPS)

    # Create a VideoCapture object to capture frames from the webcam

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Get the frame rate of the video
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Calculate the video length in seconds
    video_length = total_frames / fps

    video_length = round(video_length / current_default["skip_sec"], 2)

    ret, image = cap.read()
    copy_image = copy.deepcopy(image)

    cv2.namedWindow('AprilTag Detect Demo')
    cv2.setMouseCallback('AprilTag Detect Demo', draw_line, image)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    #print("Frames per second:", fps)

    

    while True:
        # Resize the debug image
        cv2image_resized = cv2.resize(image, (int(frame_width/int(current_default["size_reduced"])), int(frame_height/int(current_default['size_reduced']))))
        
        cv2.imshow('AprilTag Detect Demo', cv2image_resized)
        key = cv2.waitKey(1) & 0xFF
     
        if pixels_to_cm_ratio > 0.0:  # Check if distance is greater than 0.0
            #print("Distance is greater than 0.0. Exiting loop.")
            break
        if key == 27:  # Esc key
            break


    cv2.destroyAllWindows()


    #whow the new ui design in new thread 
    video_thread = threading.Thread(target=UI_video_feed,args=(fps,))
    video_thread.start()

    cv2.namedWindow("AprilTag Detect Demo")

    callback_with_image = partial(draw_circle, image)

    cv2.setMouseCallback("AprilTag Detect Demo", callback_with_image)

       # this creats a key for every frames of the video 
    frame_time = 0
    #print("video_length",video_length+1)
    for i in range(int(video_length)+1):
        Final_All_data_saved[str(i)] = {}  # Create a dictionary for each frame time
        Final_All_data_saved[str(i)]["Dont_Display_Num"] = []

   # return 

    New_tuple = None
    while pixels_to_cm_ratio > 0.0:
        ret, image = cap.read()
        if ret:
            if clicked_skipped_button == True:
                #count = int(cap.get(cv2.CAP_PROP_POS_FRAMES) + current_default["skip_sec"] * cap.get(cv2.CAP_PROP_FPS))
                Next_Frames_Capture = int(cap.get(cv2.CAP_PROP_POS_FRAMES) + current_default["skip_sec"] * cap.get(cv2.CAP_PROP_FPS))
                cap.set(cv2.CAP_PROP_POS_FRAMES, Next_Frames_Capture)
                clicked_skipped_button = False
                current_circle = None
                print("Next_Frames_Capture",Next_Frames_Capture)
                count = count + 1

            if clicked_Undo_button == True:
                Next_Frames_Capture = int(Next_Frames_Capture - (current_default["skip_sec"] * cap.get(cv2.CAP_PROP_FPS)))
                cap.set(cv2.CAP_PROP_POS_FRAMES, Next_Frames_Capture)
                clicked_Undo_button = False
                print("Next_Frames_Capture",Next_Frames_Capture)
                count  = count - 1

            # this is causing to be slow 
            cap.set(cv2.CAP_PROP_POS_FRAMES, Next_Frames_Capture)

            debug_image = copy.deepcopy(image)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            tags = at_detector.detect(
                image,
                estimate_tag_pose=False,
                camera_params=None,
                tag_size=None,
            )

            print("count",count)
            if count == int(video_length)+1:
                print("completee Final_All_data_saved",Final_All_data_saved)
                 # Loop through each key in the data and call the function
                for key, value in Final_All_data_saved.items():
                    #print("count",count)
                    count = key
                    calculate_distances_and_save_to_csv({key: value}, current_default["set_data_file_name"]+".csv")
                cv2.destroyAllWindows()
                break


            debug_image = draw_tags(debug_image, tags)
            key = cv.waitKey(1)

            if key == 27:  # ESC
                break

            #print("drawing", drawing)
            #drawing var should be remove or replace for drawline return
            if drawing:
                cv2.line(debug_image, pt1, pt2, (0, 0, 255), 5)
                midpoint = ((pt1[0] + pt2[0]) // 2, (pt1[1] + pt2[1]) // 2) 
                cv2.putText(debug_image, f"{pixels_to_cm_ratio:.2f} cm", midpoint, cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 10)
                cv2.circle(debug_image, pt1, 20, (255, 0, 0), 4)
                cv2.circle(debug_image, pt2, 20, (255, 0, 0), 4)

                    

            cv2image_resized = cv2.resize(debug_image, (int(frame_width/int(current_default["size_reduced"])), int(frame_height/int(current_default['size_reduced']))))
            cv2.imshow('AprilTag Detect Demo', cv2image_resized)
       
        else:
            cv2.destroyAllWindows()
            break

            #if count == 6:
                 

        """
        #close the video if there is no data frames
        else:
            if counter == 6:
                print("completee Final_All_data_saved",Final_All_data_saved)
                # Loop through each key in the data and call the function
                for key, value in Final_All_data_saved.items():
                    print("count",count)
                    counter = key
                    calculate_distances_and_save_to_csv({key: value}, current_default["set_data_file_name"]+".csv")

            cv2.destroyAllWindows()
            break
    """
    cv2.destroyAllWindows()


    return 




# Function to close the video feed window and release the video capture








if __name__ == '__main__':

    check_File_Settings()

    create_csv()

    UI_Design()
"""
    test = {'0': {'Dont_Display_Num': ['5'], '4': [1154, 1423], '6': [1849, 1422], '7': [660, 1335], '5': [2196, 1412]}, '1': {'Dont_Display_Num': [], '4': [1153, 1421], '6': [1849, 1419], '7': [659, 1322], '5': [2199, 1446]}, '2': {'Dont_Display_Num': [], '4': [1157, 1412], '5': [2208, 1437], '6': [1850, 1417], '7': [662, 1323]}, '3': {'Dont_Display_Num': ['5', '6'], '4': [1448, 1372], '7': [2569, 1252], '5': [864, 1288], '6': [1928, 1472]}, '4': {'Dont_Display_Num': ['5', '6', '7', '4'], '5': [1648, 120], '6': [848, 144], '7': [520, 732], '4': [1136, 1392]}, '5': {'Dont_Display_Num': ['4', '5', '6', '7'], '4': [1860, 52], '5': [2392, 484], '6': [3048, 688], '7': [2528, 1368]}}


     #calculate_distances_and_save_to_csv({key: value}, current_default["set_data_file_name"]+".csv")

    for key, value in test.items():
        print("count",count)
        counter = key
        calculate_distances_and_save_to_csv({key: value}, "test"+".csv")
        """