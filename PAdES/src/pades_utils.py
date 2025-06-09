"""!
@file pades_utils.py
@brief Utility functions for file browsing and USB detection used in the PADES application.

@details
This module provides helper functions to:
- Browse for public key and PDF files using file dialogs
- Detect removable USB devices and search for private keys
- Update GUI elements based on available USB devices

Used libraries:
- 'psutil' for detecting available USB devices
- 'tkinter.filedialog' for file selection dialogs
- 'os' for path handling and filesystem operations
"""

import psutil
from tkinter import filedialog
import os

def browse_public_key_file(entry):
    """!
    @brief Opens a file dialog to select a public key file with .PEM extension and inserts the path into a GUI box.

    @param entry: Tkinter library Entry widget where the selected file path will be inserted.
    """
    file_path = filedialog.askopenfilename(
        title="Select Public Key",
        filetypes=[("PEM files", "*.pem")],
        initialdir=os.getcwd()
    )
    if file_path:
        entry.delete(0, 'end')
        entry.insert(0, file_path)

def browse_pdf_file(pdf_path_entry):
    """!
    @brief Opens a file dialog to select a PDF file (only with .PDF extension) and inserts the path into a GUI box.

    @param pdf_path_entry: Tkinter library Entry widget where the selected PDF path will be inserted.
    """
    downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    file_path = filedialog.askopenfilename(
        initialdir=downloads_dir,
        filetypes=[("PDF files", "*.pdf")]
    )
    if file_path:
        pdf_path_entry.delete(0, 'end')
        pdf_path_entry.insert(0, file_path)
        
def get_usb_devices():
    """!
    @brief Detects currently mounted removable USB storage devices.

    @details This function uses the `psutil` library to list all disks and filters them to find those that are removable (so the USB devices).

    @return list[str]: A list of connected device paths.
    """
    partitions = psutil.disk_partitions()
    usb_devices = [p.device for p in partitions if 'removable' in p.opts]
    return usb_devices

def find_usb_with_key(usb_devices):
    """!
    @brief Looks for the list of USB devices for one containing an encrypted private key.

    @param usb_devices list[str]: A list of USB device paths to search. Those paths are returned by get_usb_devices() function.

    @return str | None: The path to the USB device containing a private key, or None in case there is no USB devices or none of them contains private key.
    """
    for device in usb_devices:
        key_dir = os.path.join(device, "keys")
        if os.path.isdir(key_dir):
            for f in os.listdir(key_dir):
                if f.endswith("_private_key.enc"):
                    return device
    return None

def update_usb_devices(usb_path_entry):
    """! 
    @brief Allows to update the list of USB devices currently connected to the computer. It auto-selects one containing a private key.

    @details It makes sure that if there is a USB device connected with encrypted private key, it will be selected by default in the GUI and if 
    there are no USB devices connected, the box will be empty.
    It uses the get_usb_devices() function to retrieve the list of USB devices and the find_usb_with_key() function to filter them and to get path of 
    a device with a private key.

    @param usb_path_entry: Tkinter library Combobox widget to update and populate with USB devices.
    """
    usb_devices = get_usb_devices()
    usb_path_entry['values'] = usb_devices
    auto_device = find_usb_with_key(usb_devices)
    if auto_device:
        usb_path_entry.set(auto_device)
    elif usb_devices:
        usb_path_entry.current(0)
    else:
        usb_path_entry.set("")