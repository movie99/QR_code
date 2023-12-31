"""
this code the the UI and storing data on the program
"""
#https://stackoverflow.com/questions/63107313/is-there-an-alternative-to-pyinstaller-for-python-3-8
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import *
from tkinter import filedialog
from tkinter import colorchooser
from tkinter import simpledialog, messagebox
import base64
import io
import json
import os
import uuid



#this LIB is the backend fucn when presssed 
from UI_Backend import create_spinbox_values , combobox_changed ,Button_pressed , Spinbox_changed , Entry_Changed ,CheckButton_changed ,create_spinbox_values , custom_button_UI ,custom_button_UI_2
#from QR_detection import write_data


from PIL import Image as pil_image
from PIL import Image, ImageTk


def read_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    else:
        with open(file_path, 'w') as file:
            initial_content = Default_settings
            initial_content_str = json.dumps(initial_content)
            file.write(initial_content_str)
        return initial_content_str

# next page 
def show_frame_page(frame, width, height):
    frame.tkraise()
    root.geometry(f"{width}x{height}")




def UI_Gen(frame, All_Labels=None, ALL_Combobox=None, All_Entry=None, All_Spinbox=None, All_button=None, All_Check_Box=None, custom_lists_buttons=None, custom_lists_buttons2= None, width=None,height=None):
    #print(All_Labels)
    # create labels
    if All_Labels:
        for key, value in All_Labels.items():
            if "image" in value:
                print("going throught image")
                print("style: ",value["style"])
                label = ttk.Label(frame, style=value['style'])
                label.grid(row=value["row"], column=value["column"], sticky=value["sticky"])
                # print("this is true")
            else:
                label = ttk.Label(frame, text=key, style=value['style'])
                label.grid(row=value["row"], column=value["column"], sticky=value["sticky"])

    if All_Entry:
        # create entries
        for index, (key, value) in enumerate(All_Entry.items()):
            # 'index' will give you the loop iteration number
            #print(f"Iteration {index + 1}: Key = {key}, Value = {value}")
            #print("key", key)
            #print("value", value)
            random_id = str(uuid.uuid4())
            print("Random ID:", random_id)
            
            key_name = key
            key = current_default[str(key)]
            print("key", key)
            entry = ttk.Entry(frame, textvariable=str(random_id)+"", style=value['style'])
            entry.grid(row=value["row"], column=value["column"], sticky=value["sticky"])
            entry.bind("<KeyRelease>", lambda event, m=key_name, c=entry: Entry_Changed(event, m, c))
            entry.insert(0, key)

        # create spinboxes
    if All_Spinbox:
        for key, value in All_Spinbox.items():
            key_name = key
            key = current_default[str(key)]
            selected_value = tk.DoubleVar(value=key)
            spinbox = ttk.Spinbox(frame, values=create_spinbox_values(value["start_stop_setp"]), textvariable=selected_value, style=value["style"], command=lambda c=key_name, m=selected_value: Spinbox_changed(m.get(), c), state="readonly")
            spinbox.grid(row=value["row"], column=value["column"], sticky=value["sticky"])
            frame.columnconfigure(value["column"], weight=1)
    if All_button: 
        # creates buttons with custom pages
        for key, value in All_button.items():
            button = ttk.Button(frame, text=key, style=value["style"], command=lambda m=key , f = frame, w = width, h = height: Button_pressed(m,f,w,h))
            button.grid(row=value["row"], column=value["column"], sticky=value["sticky"])

    # create comboboxes
    if ALL_Combobox:
        for key, value in ALL_Combobox.items():
            combobox = ttk.Combobox(frame, values=value["Option"], state="readonly")
            combobox.grid(row=value["row"], column=value["column"], sticky=value["sticky"])
            combobox.bind("<<ComboboxSelected>>", combobox_changed)
            combobox.current(current_default['qr_family']['Option_Num'])
            #combobox.grid_forget()

    if All_Check_Box:
        for key, value in All_Check_Box.items():
            key_name = key
            var2 = tk.BooleanVar(value=current_default['Save_Snapshot'])
            spinbox = tk.Checkbutton(frame, onvalue=True, offvalue=False, variable=var2, command=lambda c=key_name, m=var2: CheckButton_changed(m.get(), c))
            spinbox.grid(row=value["row"], column=value["column"], sticky=value["sticky"])
            frame.columnconfigure(value["column"], weight=1)
        # custom colors horizontal list button
        print(current_default["qr_color"])

    if custom_lists_buttons:
        for key, value in custom_lists_buttons.items():
            # Create a frame to hold the buttons
            button_frame = ttk.Frame(frame)
            button_frame.grid(row=value["row"], column=value["column"], sticky="ew")

            # Configure the frame to fill the cell horizontally
            frame.columnconfigure(value["column"], weight=1)

            # Configure the button_frame to expand and fill space, only horizontally.
            # Set weight for all columns to 1 to divide space equally
            for col in range(10):
                button_frame.columnconfigure(col, weight=1)

            for i in range(10):
                button_style = f"Button{i}" + ".TButton"
                color = current_default['qr_color'].get(str(i), [0, 0, 0])
                hex_color = '#%02x%02x%02x' % (color[0], color[1], color[2])
                style = ttk.Style()
                # Adjust the padding to change the height, (left, top, right, bottom)
                style.configure(button_style, background=hex_color, padding=(1, 1, 1, 1))

                button2 = ttk.Button(button_frame, text=f"{i}", style=button_style)
                button2.configure(command=lambda idx=i, btn=button2: custom_button_UI(btn, idx))

                # Grid the button with sticky='ew' so it expands only horizontally
                button2.grid(row=0, column=i, sticky="ew")
    #print(custom_lists_buttons2)    

    if custom_lists_buttons2 and isinstance(custom_lists_buttons2, dict):
        for key, value in custom_lists_buttons2.items():
            # Create a frame to hold the buttons
            button_frame = ttk.Frame(frame)
            button_frame.grid(row=value["row"], column=value["column"], sticky="ew")

            # Configure the frame to fill the cell horizontally
            frame.columnconfigure(value["column"], weight=1)

            # Configure the button_frame to expand and fill space, only horizontally.
            # Set weight for all columns to 1 to divide space equally
            for col in range(10):
                button_frame.columnconfigure(col, weight=1)

            for i in range(10):
                button_style = f"Button{i}" + ".TButton"
                color = current_default['qr_color'].get(str(i), [0, 0, 0])
                hex_color = '#%02x%02x%02x' % (color[0], color[1], color[2])
                style = ttk.Style()
                # Adjust the padding to change the height, (left, top, right, bottom)
                style.configure(button_style, background=hex_color, padding=(1, 1, 1, 1))

                button2 = ttk.Button(button_frame, text=f"{i}", style=button_style)
                button2.configure(command=lambda idx=i, btn=button2: custom_button_UI_2(btn, idx))

                # Grid the button with sticky='ew' so it expands only horizontally
                button2.grid(row=0, column=i, sticky="ew")

    




    #label = ttk.Label(frame, text=string, style="New_Custom.TLabel")
    #label.grid(row=8, column=0, sticky="nsew")

def Measurement_UI(root, bg_color,width=100, height=100):
    frame = tk.Frame(root,width=100, height=100)
    frame.grid(row=0, column=0, sticky='nsew')
    frame.configure(bg=bg_color)

    All_Labels = {
       "Measurement in CM": {"style": 'New_Custom.TLabel', "row": 0, "column": 0, "sticky": "nsew"},

    }


    All_Entry = {
        "Measurement": {"style": 'New_Custom.TEntry', "row": 0, "column": 1, "sticky": "nsew"},

    }

    All_button = {
        "ok": {"style": 'New_Custom.TButton', "row": 1, "column": 0, "sticky": "nsew"},
        "canceled": {"style": 'New_Custom.TButton', "row": 1, "column": 1, "sticky": "nsew"},
    }

    print("new frame")
    UI_Gen(frame, All_Labels=All_Labels, ALL_Combobox=None, All_Entry=All_Entry, All_Spinbox=None, All_button=All_button, All_Check_Box=None, custom_lists_buttons=None,width = 100 ,height = 100)
    return frame


def Video_Frame(root, bg_color,width=600, height=50):
    frame = tk.Frame(root,width=600, height=50)
    frame.grid(row=0, column=0, sticky='nsew')
    frame.configure(bg=bg_color)

    custom_lists_buttons2 = {
        "color_detect": {"style": 'New_Custom.TButton', "amount_of_buttons": 10, "row": 0, "column": 1, "sticky": "nsew"}
    }

    All_Entry = {
        "minuse": {"style": 'New_Custom.TEntry', "row": 0, "column": 2, "sticky": "nsew"},

    }

    All_button = {
        "-": {"style": 'New_Custom.TButton', "row": 0, "column": 3, "sticky": "nsew"},
        "undo": {"style": 'New_Custom.TButton', "row": 0, "column": 4, "sticky": "nsew"},
        "Next": {"style": 'New_Custom.TButton', "row": 0, "column": 5, "sticky": "nsew"},
    }

    print("new frame")
    UI_Gen(frame, All_Labels=None, ALL_Combobox=None, All_Entry=All_Entry, All_Spinbox=None, All_button=All_button, All_Check_Box=None, custom_lists_buttons2=custom_lists_buttons2, width = 600 ,height = 50)
    return frame




def Excel_Frame(root, bg_color,width=200, height=300):
    frame = tk.Frame(root,width=200, height=300)
    frame.grid(row=0, column=0, sticky='nsew')
    frame.configure(bg=bg_color)

    All_Labels = {
        "IMAGE": {"image": new_image, "style": 'New_Custom.TLabel', "row": 0, "column": 0, "sticky": "nsew"},
        "Exel Settings": {"style": 'New_Custom.TLabel', "row": 0, "column": 1, "sticky": "nsew"},
        "Experiment Name": {"style": 'New_Custom.TLabel', "row": 1, "column": 0, "sticky": "nsew"},
        "Round": {"style": 'New_Custom.TLabel', "row": 2, "column": 0, "sticky": "nsew"},
        "Date OF Video": {"style": 'New_Custom.TLabel', "row": 3, "column": 0, "sticky": "nsew"},
        "Date Logged": {"style": 'New_Custom.TLabel', "row": 4, "column": 0, "sticky": "nsew"},
        "Initial": {"style": 'New_Custom.TLabel', "row": 5, "column": 0, "sticky": "nsew"},
        "Time video started": {"style": 'New_Custom.TLabel', "row": 6, "column": 0, "sticky": "nsew"},
        "Treatment": {"style": 'New_Custom.TLabel', "row": 7, "column": 0, "sticky": "nsew"},
    }

    All_button = {
        "Previous page": {"style": 'New_Custom.TButton', "row": 15, "column": 0, "sticky": "nsew"},
       # "Test page": {"style": 'New_Custom.TButton', "row": 15, "column": 6, "sticky": "nsew"},
    }

    All_Entry = {
        "Experiment_Name": {"style": 'New_Custom.TEntry', "row": 1, "column": 1, "sticky": "nsew"},
        "Round": {"style": 'New_Custom.TEntry', "row": 2, "column": 1, "sticky": "nsew"},

        "Dates_OF_Vid": {"style": 'New_Custom.TEntry', "row": 3, "column": 1, "sticky": "nsew"},
        "Date_Logged": {"style": 'New_Custom.TEntry', "row": 4, "column": 1, "sticky": "nsew"},

        "Initial": {"style": 'New_Custom.TEntry', "row": 5, "column": 1, "sticky": "nsew"},
        "Time_vide_started": {"style": 'New_Custom.TEntry', "row": 6, "column": 1, "sticky": "nsew"},
        "Treatment": {"style": 'New_Custom.TEntry', "row": 7, "column": 1, "sticky": "nsew"},
    }

    ALL_Combobox = {}
    UI_Gen(frame, All_Labels=All_Labels, ALL_Combobox=ALL_Combobox, All_Entry=All_Entry, All_Spinbox=None, All_button=All_button, All_Check_Box=None, custom_lists_buttons=None,width = width ,height = height)
    return frame



def UI_Main(root, bg_color,width=700, height=300):

    frame = tk.Frame(root,width=700, height=700)
    frame.grid(row=0, column=0, sticky='nsew')
    frame.configure(bg=bg_color)


    All_Labels = {
        "IMAGE": {"image": new_image, "style": 'New_Custom.TLabel', "row": 0, "column": 0, "sticky": "nsew"},
        "QR gen and Type": {"style": 'New_Custom.TLabel', "row": 0, "column": 1, "sticky": "nsew"},
        "QR Settings": {"style": 'New_Custom.TLabel', "row": 0, "column": 3, "sticky": "nsew"},
        "Save & Start": {"style": 'New_Custom.TLabel', "row": 0, "column": 5, "sticky": "nsew"},
        "QR Type Family": {"style": 'New_Custom.TLabel', "row": 1, "column": 0, "sticky": "nsew"},
        "Set File Name": {"style": 'New_Custom.TLabel', "row": 2, "column": 0, "sticky": "nsew"},
        "Tags Generate": {"style": 'New_Custom.TLabel', "row": 3, "column": 0, "sticky": "nsew"},
        "color picker": {"style": 'New_Custom.TLabel', "row": 4, "column": 0, "sticky": "nsew"},
        "qr size": {"style": 'New_Custom.TLabel', "row": 5, "column": 0, "sticky": "nsew"},
        "nthreads": {"style": 'New_Custom.TLabel', "row": 1, "column": 2, "sticky": "nsew"},
        "Quad decimage": {"style": 'New_Custom.TLabel', "row": 2, "column": 2, "sticky": "nsew"},
        "Quad sigma": {"style": 'New_Custom.TLabel', "row": 3, "column": 2, "sticky": "nsew"},
        "refined edges": {"style": 'New_Custom.TLabel', "row": 4, "column": 2, "sticky": "nsew"},
        "decode sharpening": {"style": 'New_Custom.TLabel', "row": 5, "column": 2, "sticky": "nsew"},
        "debug": {"style": 'New_Custom.TLabel', "row": 6, "column": 2, "sticky": "nsew"},
        "size_reduced": {"style": 'New_Custom.TLabel', "row": 1, "column": 4, "sticky": "nsew"},
        "skip_sec": {"style": 'New_Custom.TLabel', "row": 2, "column": 4, "sticky": "nsew"},
        "Save Snapshots": {"style": 'New_Custom.TLabel', "row": 3, "column": 4, "sticky": "nsew"},
        "Save Settings ": {"style": 'New_Custom.TLabel', "row": 4, "column": 4, "sticky": "nsew"},
        "Select Vid": {"style": 'New_Custom.TLabel', "row": 5, "column": 4, "sticky": "nsew"},
    }
    ALL_Combobox = {
        "qr_family": {"Option": ["tag16h5", "tag25h9", "tag36h11"], "Option_Num": 0, "row": 1, "column": 1, "sticky": "nsew"}
    }
    All_Entry = {
        "set_file_name": {"style": 'New_Custom.TEntry', "row": 2, "column": 1, "sticky": "nsew"},
    }
    All_Spinbox = {
        "tag_generate": {"start_stop_setp": (0, 11.0, 1.0, 1), "style": 'New_Custom.TSpinbox', "row": 3, "column": 1, "sticky": "nsew"},
        "nthreads": {"start_stop_setp": (0, 10.0, 1.0, 1), "style": 'New_Custom.TSpinbox', "row": 1, "column": 3, "sticky": "nsew"},
        "quad_decimate": {"start_stop_setp": (0, 30.0, 0.1, 1.0), "style": 'New_Custom.TSpinbox', "row": 2, "column": 3, "sticky": "nsew"},
        "quad_sigma": {"start_stop_setp": (0, 30.0, 0.1, 1.0), "style": 'New_Custom.TSpinbox', "row": 3, "column": 3, "sticky": "nsew"},
        "refine_edges": {"start_stop_setp": (0, 11.0, 1.0, 1), "style": 'New_Custom.TSpinbox', "row": 4, "column": 3, "sticky": "nsew"},
        "decode_sharpening": {"start_stop_setp": (0, 30.0, 0.1, 1.0), "style": 'New_Custom.TSpinbox', "row": 5, "column": 3, "sticky": "nsew"},
        "debug": {"start_stop_setp": (0, 30.0, 0.1, 1.0), "style": 'New_Custom.TSpinbox', "row": 6, "column": 3, "sticky": "nsew"},
        "size_reduced": {"start_stop_setp": (1, 3000.0, 1.0, 1.0), "style": 'New_Custom.TSpinbox', "row": 1, "column": 5, "sticky": "nsew"},
        "skip_sec": {"start_stop_setp": (0, 3000.0, 1.0, 1.0), "style": 'New_Custom.TSpinbox', "row": 2, "column": 5, "sticky": "nsew"},
        "qr_size": {"start_stop_setp": (0, 30.0, 0.1, 1.0), "style": 'New_Custom.TSpinbox', "row": 5, "column": 1, "sticky": "nsew"},
    }
    All_button = {
        "Save All Default": {"style": 'New_Custom.TButton', "row": 4, "column": 5, "sticky": "nsew"},
        "Video Selected": {"style": 'New_Custom.TButton', "row": 5, "column": 5, "sticky": "nsew"},
        "Next Page": {"style": 'New_Custom.TButton', "row": 8, "column": 5, "sticky": "nsew"},
        "Generate": {"style": 'New_Custom.TButton', "row": 6, "column": 1, "sticky": "nsew"}
    }
    All_Check_Box = {
        "Save_Snapshot": {"style": 'New_Custom.TButton', "row": 3, "column": 5, "sticky": "nsew"},
    }
    custom_lists_buttons = {
        "color_detect": {"style": 'New_Custom.TButton', "amount_of_buttons": 10, "row": 4, "column": 1, "sticky": "nsew"}
    }

    #UI_Main_Back()
    UI_Gen(frame,All_Labels,ALL_Combobox,All_Entry,All_Spinbox,All_button,All_Check_Box,custom_lists_buttons,width,height)




    #print("frame1",frame1)
    #print("frame2",frame2)
    #show_frame_page(frame2 if frame == frame1 else frame1)
    #label = ttk.Label(frame, text="Page2", style="New_Custom.TLabel")
    #label.grid(row=0, column=0)
    #button = ttk.Button(frame, text="Button", command=lambda: show_frame_page(frame2 if frame == frame1 else frame1))
    #button.grid(row=1, column=0)


    return frame


def check_File_Settings():
    global current_default
    File_Default_name = "Settings.json"
    current_default = json.loads(read_file(File_Default_name))
    #print("current_default",current_default)

# Initially, show the first page
#show_frame(page1frame)


root = tk.Tk()
style = ttk.Style()
style.theme_create("New_Custom", parent="alt", settings={
    "TLabel": {"configure": {"foreground": "#FFFFFF", "background": "#8c0b42", "font": ("Comic Sans MS", 13, "bold")}},
    "TSpinbox": {"configure": {"arrowsize": 20, "selectbackground": "#858282", "fieldbackground": "white", "background": "#FFFFFF", "font": ("Comic Sans MS", 13, "bold"), "width": 5}},
    "TEntry": {"configure": {"foreground": "#858282", "background": "#FFFFFF", "font": ("Comic Sans MS", 13, "bold")}},
    "TButton": {
        "configure": {
            "foreground": "white",
            "background": "black",
            "font": ("Comic Sans MS", 13, "bold"),
            "bordercolor": "red",  # set border color
            "borderwidth": 2,  # set border width
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
    "TCombobox": {"configure": {"arrowsize": 20, "foreground": "white", "font": ("Comic Sans MS", 13, "bold")}},
    "TLabel2": {"configure": {"foreground": "#FFFFFF", "background": "#8c0b42", "font": ("Comic Sans MS", 13, "bold")}}
})


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
        "data_header":[
            'Experiment name',
            'Round',
            'Date of video',
            'Date Logged',
            'Qr Family',
            'NThreads',
            'Quad Decimage',
            'Quad Sigma',
            'Refine Edges',
            'Decode Sharpening',
            'Debug',
            'Initials',
            'Scan time interval (s)',
            'Time Video Start',
            'Time from start',
            'Scan #',
            'Treatment',
            'Individual 1',
            'Individual 2',
            'Distance (cm)'
        ],
        "data_format":"['Young', '1', 'day,month,year', 'Snapshot_', 'Neighbor_1', 'Neighbor_2', 'Distance_cm', 'block','half']",

        "skip_sec":180.0,
        "qr_keys":"[0,1,2,3]",
        "Save_Snapshot":False,
        "Experiment_Name":"Name",
        "Round":"1",
        "Dates_OF_Vid":"Date",
        "Date_Logged":"Logged",
        "Initial":"Initial",
        "Time_vide_started":"00:00",
        "Treatment":"Treatment",
        "minuse":1,
        "Measurement":""


}
# this is your current default settings stored in memory

current_default = {}

check_File_Settings()


style.theme_use("New_Custom")


image_base64string = """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

"""

path_icon = PhotoImage(data = image_base64string) 
image_bytes = base64.b64decode(image_base64string)
img = pil_image.open(io.BytesIO(image_bytes))
resized_image = img.resize((64, 70), pil_image.LANCZOS)  
#print("running")
new_image= ImageTk.PhotoImage(resized_image)
hex_str = "44 45 56 20 61 6C 65 78 30 32 40 6E 6D 73 75 2E 65 64 75"
string = bytes.fromhex(hex_str).decode('utf-8')
#This is New_Custom themes for tkinter

root.title("Title of Your Application")

#creates new pages
frame1 = UI_Main(root, "#8c0b42",width=1065, height=260)
frame2 = Excel_Frame(root, "#8c0b42",width=400, height=300)
frame3 = Video_Frame(root, "#8c0b42",width=600, height=50)
frame4 = Measurement_UI(root, "#8c0b42",width=100, height=100)


root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)


show_frame_page(frame1,1065,260)




root.mainloop()
