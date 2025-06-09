"""!
@file gui.py
@brief This file contains the GUI for the RSA key generation application.
@details This application contains a graphical user interface (GUI) that allows users to generate RSA keys, encrypt the private key with a PIN, 
and save the keys to a USB device and a specified public key path. The GUI is built using Tkinter.
"""

from tkinter import Tk, Label, Entry, Button, filedialog, messagebox, IntVar, ttk
from tkinter.ttk import Progressbar
from key_generation import *
from key_encryption import *
from key_saving import *
from utils import *
import os
import threading

def update_usb_devices():
    """! 
    @brief Allows to update the list of USB devices currently connected to the computer.

    @details It makes sure that if there is at least one USB device connected, it will be selected by default in the GUI and if 
    there are no USB devices connecter, the box will be empty.
    """
    usb_devices = get_usb_devices()
    usb_path_entry['values'] = usb_devices
    if usb_devices:
        usb_path_entry.current(0)
    else:
        usb_path_entry.set("")

def browse_public_key_path():
    """! 
    @brief Allows to choose a directory where the public key will be saved.

    @details Retrieves the current path from the GUI field as the initial directory.
    If the user selects a folder, it replaces default directory path with the new path.
    """
    initial_dir = pub_key_path_entry.get()
    pub_key_path = filedialog.askdirectory(initialdir=initial_dir)
    if pub_key_path:
        pub_key_path_entry.delete(0, 'end')
        pub_key_path_entry.insert(0, pub_key_path)

def generate_and_save_keys():
    """! 
    @brief Main logic for GUI, data validation, key generation, encryption and keys saving.

    @details This function retrieves user inputs from the GUI, which includes:
    - PIN to encrypt the private key
    - USB path where the private key will be saved
    - Public key save location
    - Key name for the generated keys
    Those inputs are validated and if error occurs, it shows a specific error message.

    If the data is correct, it proceeds to generate RSA keys using the generate_rsa_keys() function from key_generation.py  file.
    The generated keys are then encrypted using the encrypt_private_key() function from key_encryption.py file, where the PIN is used to derive the encryption key.
    After encryption, the keys are saved using the save_keys() function from key_saving.py file, where the private key is saved on the USB device and the public key
    is saved in the specified path.

    During the process, the GUI is updated to show progress bar and status messages. If any step fails, an error message is displayed, so that the user can be informed about
    all the issues during the process.

    If the keys are successfully generated, encrypted, and saved, a success message is displayed with the paths to the saved keys and information about any other
    action taken, such as clearing keys directory on the USB drive.
    """
    pin = pin_entry.get()
    usb_path = usb_path_entry.get()
    public_key_path = pub_key_path_entry.get()
    key_name = key_name_entry.get()
    
    if not os.path.exists(usb_path):
        messagebox.showerror("Error", "Invalid USB path")
        return
    if not os.access(usb_path, os.W_OK):
        messagebox.showerror("Error", "No write access to the USB path")
        return
    if not key_name:
        messagebox.showerror("Error", "Key name cannot be empty")
        return
    
    progress_label.config(text="Generating keys...")
    progress_label.update_idletasks()
    private_key, public_key = generate_rsa_keys()
    if private_key is None or public_key is None:
        messagebox.showerror("Error", "Key generation failed")
        return
    
    def progress_callback(current, total):
        progress_var.set(current)
        progress_bar.update_idletasks()
    
    progress_label.config(text="Encrypting private key...")
    progress_label.update_idletasks()
    progress_bar["maximum"] = 600000
    private_key = encrypt_private_key(private_key, pin, progress_callback)
    if private_key is None:
        messagebox.showerror("Error", "Encryption failed")
        return
    
    progress_label.config(text="Saving keys...")
    progress_label.update_idletasks()

    priv_key_path, pub_key_path, was_cleared = save_keys(private_key, public_key, usb_path, public_key_path, key_name)
    if priv_key_path is None or pub_key_path is None:
        messagebox.showerror("Error", "Key saving failed")
        return

    progress_label.config(text="Keys saved!")
    cleared_info = "\n\nPrevious keys on USB drive were removed." if was_cleared else ""
    messagebox.showinfo("Success", f"Encrypted private key saved to:\n{priv_key_path}\n\nPublic key saved to:\n{pub_key_path}{cleared_info}")

    
def handle_generate_button_click():
    """! 
    @brief Function handles the generate button click event in the GUI.

    @details Disables GUI inputs, shows a progress bar and loading indicator, and launches the key generation process in a new thread.
    When the process is complete, it restores the GUI to its original state, enabling inputs and hiding the progress bar.
    """
    def task():
        generate_and_save_keys()
        progress_label.config(text="")
        root.config(cursor="")
        root.update()
        progress_bar.grid_remove()
        progress_label.grid_remove()
        pin_entry.config(state="normal")
        key_name_entry.config(state="normal")
        usb_path_entry.config(state="readonly")
        pub_key_path_entry.config(state="normal")
        generate_button.config(state="normal")
        refresh_button.config(state="normal")
        browse_button.config(state="normal")
        progress_var.set(0)

    root.config(cursor="wait")
    progress_bar.grid(row=6, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
    progress_label.grid(row=7, column=0, columnspan=3, pady=5)
    root.update()

    pin_entry.config(state="disabled")
    key_name_entry.config(state="disabled")
    usb_path_entry.config(state="disabled")
    pub_key_path_entry.config(state="disabled")
    generate_button.config(state="disabled")
    refresh_button.config(state="disabled")
    browse_button.config(state="disabled")

    threading.Thread(target=task).start()

def main():
    """!
    @brief Initializes the GUI for the RSA key generation application. Creates all necessary components and starts the Tkinter main loop.

    @details
    This function sets up the main window, adds labels, entry fields, buttons, and a progress bar. All the components are arranged and configured to allow the user 
    to enter a key name, a PIN for the private key, select a USB drive, and specify a path for saving the public key.
    """
    global root, pin_entry, key_name_entry, usb_path_entry, pub_key_path_entry
    global progress_label, progress_bar, progress_var
    global generate_button, refresh_button, browse_button

    root = Tk()
    root.title("RSA Key Generator")

    Label(root, text="Enter a key name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    key_name_entry = Entry(root)
    key_name_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

    Label(root, text="Enter a PIN for your private key:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    pin_entry = Entry(root, show="*")
    pin_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

    Label(root, text="Select your USB drive:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    usb_path_entry = ttk.Combobox(root, state="readonly")
    usb_path_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
    update_usb_devices()

    Label(root, text="Public key save location:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    pub_key_path_entry = Entry(root)
    pub_key_path_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
    browse_button = Button(root, text="Browse", command=browse_public_key_path)

    default_key_path = os.path.join(os.getcwd(), "keys")
    if not os.path.exists(default_key_path):
        os.mkdir(default_key_path)
    pub_key_path_entry.insert(0, default_key_path)
    browse_button.grid(row=3, column=2, padx=10, pady=5)

    root.grid_columnconfigure(1, weight=1)

    progress_var = IntVar()
    progress_label = Label(root, text="Processing...")
    progress_bar = Progressbar(root, variable=progress_var, maximum=600000)

    refresh_button = Button(root, text="Refresh USB Devices", command=update_usb_devices)
    refresh_button.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
    generate_button = Button(root, text="Generate and Save Keys", command=handle_generate_button_click)
    generate_button.grid(row=5, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

    root.mainloop()

if __name__ == "__main__":
    main()