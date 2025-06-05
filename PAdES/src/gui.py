from tkinter import Tk, Label, Entry, Button, messagebox, IntVar, ttk, Radiobutton, StringVar
from tkinter.ttk import Progressbar
from sign_pdf import sign_pdf
from decrypt_key import decrypt_private_key
from utils import browse_pdf_file, update_usb_devices, browse_public_key_file
import os
import threading
from verify_signature import verify_pdf_signature

def update_mode():
    mode = mode_var.get()
    if mode == "sign":
        pin_entry.grid()
        usb_path_entry.grid()
        sign_button.grid()
        refresh_button.grid()
        verify_button.grid_remove()
        pin_label.grid()
        usb_label.grid()
        public_key_label.grid_remove()
        public_key_entry.grid_remove()
        public_key_browse.grid_remove()
    else:
        pin_entry.grid_remove()
        usb_path_entry.grid_remove()
        sign_button.grid_remove()
        refresh_button.grid_remove()
        verify_button.grid()
        pin_label.grid_remove()
        usb_label.grid_remove()
        public_key_label.grid()
        public_key_entry.grid()
        public_key_browse.grid()

def sign_document():
    pin = pin_entry.get()
    pdf_path = pdf_path_entry.get()
    usb_path = usb_path_entry.get()

    if not os.path.isfile(pdf_path):
        messagebox.showerror("Error", "Invalid PDF file path")
        return
    if not os.path.exists(usb_path):
        messagebox.showerror("Error", "Invalid USB path")
        return

    progress_label.config(text="Decrypting key...")
    progress_label.update_idletasks()

    def progress_callback(current, total):
        progress_var.set(current)
        progress_bar.update_idletasks()

    private_key = decrypt_private_key(usb_path, pin, progress_callback)
    if private_key is None:
        messagebox.showerror("Error", "Failed to decrypt private key")
        return

    progress_label.config(text="Signing PDF...")
    success = sign_pdf(pdf_path, private_key)

    if success:
        progress_label.config(text="PDF signed successfully!")
        messagebox.showinfo("Success", "PDF has been signed successfully.")
    else:
        messagebox.showerror("Error", "Failed to sign the PDF")

def handle_sign_button_click():
    def task():
        sign_document()
        progress_label.config(text="")
        root.config(cursor="")
        root.update()
        progress_bar.grid_remove()
        progress_label.grid_remove()
        pin_entry.config(state="normal")
        pdf_path_entry.config(state="normal")
        usb_path_entry.config(state="readonly")
        sign_button.config(state="normal")
        refresh_button.config(state="normal")
        browse_button.config(state="normal")
        progress_var.set(0)

    root.config(cursor="wait")
    progress_bar.grid(row=8, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
    progress_label.grid(row=9, column=0, columnspan=3, pady=5)
    root.update()

    pin_entry.config(state="disabled")
    pdf_path_entry.config(state="disabled")
    usb_path_entry.config(state="disabled")
    sign_button.config(state="disabled")
    refresh_button.config(state="disabled")
    browse_button.config(state="disabled")

    threading.Thread(target=task).start()

def handle_verify_button_click():
    pdf_path = pdf_path_entry.get()
    public_key_path = public_key_entry.get()
    if not os.path.isfile(pdf_path):
        messagebox.showerror("Error", "Please select a PDF file to verify first")
        return
    if not public_key_path or not os.path.isfile(public_key_path):
        messagebox.showerror("Error", "Please select a valid public key file")
        return

    valid, message = verify_pdf_signature(pdf_path, public_key_path)
    if valid:
        messagebox.showinfo("Verification", message)
    else:
        messagebox.showerror("Verification Failed", message)

root = Tk()
root.title("PAdES PDF Signer")

mode_var = StringVar(value="sign")
radio_frame = ttk.Frame(root)
radio_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="w")
Radiobutton(radio_frame, text="Sign", variable=mode_var, value="sign", command=update_mode).pack(side="top", anchor="w")
Radiobutton(radio_frame, text="Verify", variable=mode_var, value="verify", command=update_mode).pack(side="top", anchor="w")

Label(root, text="Select PDF file:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
pdf_path_entry = Entry(root)
pdf_path_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
browse_button = Button(root, text="Browse", command=lambda: browse_pdf_file(pdf_path_entry))
browse_button.grid(row=1, column=2, padx=10, pady=5)

public_key_label = Label(root, text="Select public key:")
public_key_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
public_key_entry = Entry(root)
public_key_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
public_key_browse = Button(root, text="Browse", command=lambda: browse_public_key_file(public_key_entry))
public_key_browse.grid(row=2, column=2, padx=10, pady=5)

pin_label = Label(root, text="Enter your private key PIN:")
pin_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
pin_entry = Entry(root, show="*")
pin_entry.grid(row=3, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

usb_label = Label(root, text="Select USB device:")
usb_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
usb_path_entry = ttk.Combobox(root, state="readonly")
usb_path_entry.grid(row=4, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
update_usb_devices(usb_path_entry)

root.grid_columnconfigure(1, weight=1)

progress_var = IntVar()
progress_label = Label(root, text="Processing...")
progress_bar = Progressbar(root, variable=progress_var, maximum=600000)

refresh_button = Button(root, text="Refresh USB Devices", command=lambda: update_usb_devices(usb_path_entry))
refresh_button.grid(row=5, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
sign_button = Button(root, text="Sign PDF", command=handle_sign_button_click)
sign_button.grid(row=6, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
verify_button = Button(root, text="Verify Signature", command=handle_verify_button_click)
verify_button.grid(row=7, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

update_mode()

root.mainloop()
