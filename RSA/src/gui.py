from tkinter import Tk, Label, Entry, Button, filedialog, messagebox, IntVar, ttk
from tkinter.ttk import Progressbar
from key_generation import *
from key_encryption import *
from key_saving import *
from utils import *
import os
import threading

def update_usb_devices():
    usb_devices = get_usb_devices()
    usb_path_entry['values'] = usb_devices
    if usb_devices:
        usb_path_entry.current(0)

def browse_public_key_path():
    initial_dir = pub_key_path_entry.get()
    pub_key_path = filedialog.askdirectory(initialdir=initial_dir)
    if pub_key_path:
        pub_key_path_entry.delete(0, 'end')
        pub_key_path_entry.insert(0, pub_key_path)

def generate_and_save_keys():
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
    progress_bar["maximum"] = 600000
    private_key = encrypt_private_key(private_key, pin, progress_callback)
    if private_key is None:
        messagebox.showerror("Error", "Encryption failed")
        return
    
    priv_key_path, pub_key_path = save_keys(private_key, public_key, usb_path, public_key_path, key_name)
    if priv_key_path is None or pub_key_path is None:
        messagebox.showerror("Error", "Key saving failed")
        return
    
    progress_label.config(text="Keys saved!")
    messagebox.showinfo("Success", f"Encrypted private key saved to:\n{priv_key_path}\n\nPublic key saved to:\n{pub_key_path}")
    
def handle_generate_button_click():
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
pub_key_path_entry.insert(0, os.path.join(os.getcwd(), "keys"))
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