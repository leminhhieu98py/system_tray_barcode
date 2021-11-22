# Import the required libraries
import os
from tkinter import *
from tkinter import filedialog

from pystray import MenuItem as item
import pystray
from PIL import Image
from barcode_reader import *


os.environ['PYSTRAY_BACKEND'] = 'gtk'

# Create an instance of tkinter frame or window
win = Tk()
win.title("Barcode File Management")
win.iconbitmap("@/home/thomas/Downloads/Telegram Desktop/hieu/hieu/barcode-scan-file-with-system-tray-icon-main/barcode.xbm")
# win.iconbitmap("/barcode.ico")

# Set the size of the window
win.geometry("600x250")

# config Grid
win.columnconfigure(0, weight=4)
win.columnconfigure(1, weight=2)



icon = None

def read_file(path):
    file = open(path, "r")
    text = file.read()
    file.close()
    return text

def write_file(path, content):
    file = open(path, "w")
    file.writelines(content)
    print("writing...")
    file.close()


root_folder_path = read_file("root.txt")
target_folder_path = read_file("target.txt")




# Define a function for quit the window
def quit_window(icon):
    icon.stop()
    win.destroy()


# Define a function to show the window again
def show_window(icon):
    win.after(0, win.deiconify())


def select_root_folder():
    # update root path
    global root_folder_path
    root_folder_path = ""
    win.filename = filedialog.askdirectory(title="Choose root folder for files to scan") #return full path here
    root_folder_path = win.filename
    write_file("root.txt", root_folder_path)

    # update root on display
    display_root_label(root_folder_path)


def select_target_folder():
    global target_folder_path
    target_folder_path = ""
    win.filename = filedialog.askdirectory(title="Choose target folder for scanned files") #return full path here
    target_folder_path = win.filename
    write_file("target.txt", target_folder_path)
    # update root on display
    display_target_label(target_folder_path)


def auto_scan_watch_dog():
    print("watch dog")


def auto_scan_activation():
    win.withdraw()
    auto_scan_watch_dog()


def manual_scan_activation():
    if root_folder_path != "" and target_folder_path != "":
        scan_engine(root_folder_path, target_folder_path)
    else:
        print("chon path")


def display_root_label(label):
    root_label = Label(win, height=2, width=45, padx="8px", text= label, anchor=W)
    root_label.grid(column=0, row=0, sticky=SW, padx=5, pady=5)


def display_target_label(label):
    target_label = Label(win, height=2, width=45, padx="8px", text= label, anchor=W)
    target_label.grid(column=0, row=1, sticky=SW, padx=5, pady=5)


# Hide the window and show on the system taskbar
def hide_window():
    global icon
    win.withdraw()
    image = Image.open("/barcode.xbm")
    # image = Image.open("/barcode.ico")
    menu = (item('Scan new file', scan_new_file), item('Show application', show_window), item('Quit', quit_window))
    icon = pystray.Icon("name", image, "Barcode File Management", menu)
    icon.run()


def display_other_components():
    # Declare components
    root_select_btn = Button(win, height=2, text="Select root folder", command=select_root_folder)
    target_select_btn = Button(win, height=2, text="Select target folder", command=select_target_folder)
    auto_scan_btn = Button(win, height=2, width=10, text="Auto scan", command=auto_scan_activation)
    manual_scan_btn = Button(win, height=2, width=10, text="Manual scan", command=manual_scan_activation)


    # Style components
    root_select_btn.grid(column=1, row=0, sticky=EW, padx=5, pady=5)
    target_select_btn.grid(column=1, row=1, sticky=EW, padx=5, pady=5)
    auto_scan_btn.place(relx=0.3, rely=0.8, anchor=CENTER)
    manual_scan_btn.place(relx=0.7, rely=0.8, anchor=CENTER)

display_other_components()
display_root_label(root_folder_path)
display_target_label(target_folder_path)


win.protocol('WM_DELETE_WINDOW', hide_window)
win.mainloop()
