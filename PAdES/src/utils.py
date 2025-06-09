import psutil
from tkinter import filedialog
import os

def browse_public_key_file(entry):
    file_path = filedialog.askopenfilename(
        title="Select Public Key",
        filetypes=[("PEM files", "*.pem")],
        initialdir=os.getcwd()
    )
    if file_path:
        entry.delete(0, 'end')
        entry.insert(0, file_path)

def browse_pdf_file(pdf_path_entry):
    downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    file_path = filedialog.askopenfilename(
        initialdir=downloads_dir,
        filetypes=[("PDF files", "*.pdf")]
    )
    if file_path:
        pdf_path_entry.delete(0, 'end')
        pdf_path_entry.insert(0, file_path)
        
def get_usb_devices():
    partitions = psutil.disk_partitions()
    usb_devices = [p.device for p in partitions if 'removable' in p.opts]
    return usb_devices

def find_usb_with_key(usb_devices):
    for device in usb_devices:
        key_dir = os.path.join(device, "keys")
        if os.path.isdir(key_dir):
            for f in os.listdir(key_dir):
                if f.endswith("_private_key.enc"):
                    return device
    return None

def update_usb_devices(usb_path_entry):
    usb_devices = get_usb_devices()
    usb_path_entry['values'] = usb_devices
    auto_device = find_usb_with_key(usb_devices)
    if auto_device:
        usb_path_entry.set(auto_device)
    elif usb_devices:
        usb_path_entry.current(0)
    else:
        usb_path_entry.set("")