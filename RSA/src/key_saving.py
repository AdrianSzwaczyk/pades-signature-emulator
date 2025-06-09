import os
import shutil

def save_keys(private_key, public_key, usb_path, public_key_path, key_name):
    """! 
    @brief Function is responsible for saving the private key on the USB device and public key in specified by the user path.

    @details Private key is saved in the "keys" catalog on the USB device. If the "keys" folder already exists, all the files inside it are delated
    to ensure that the folder is empty before saving the new keys. The public key is saved in the specified path provided by the user. Function uses shutil library, 
    which is part of default library to remove files and directories.

    @param private_key (bytes)  The private key to save, generated from generate_rsa_keys().
    @param public_key (bytes)  The public key to save, generated from generate_rsa_keys().
    @param usb_path (str)  The path to the USB device where the private key will be saved, the device was chosen from the list by user.
    @param public_key_path (str)  The path where the public key will be saved, specified by the user.
    @param key_name (str)  The name to use for the saved keys.

    @return Tuple ([str | None, str | None, bool]) containing the paths to the saved private and public keys, and a boolean indicating if the keys folder was cleared to 
    show this information on the success text box. If an error occurs it returns (None, None, False).
    """
    try:
        keys_folder = os.path.join(usb_path, "keys")
        folder_was_cleared = False

        if not os.path.exists(keys_folder):
            os.makedirs(keys_folder)
        else:
            for filename in os.listdir(keys_folder):
                file_path = os.path.join(keys_folder, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    folder_was_cleared = True
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    folder_was_cleared = True

        priv_key_path = os.path.join(keys_folder, f"{key_name}_private_key.enc")
        pub_key_path = os.path.join(public_key_path, f"{key_name}_public_key.pem")
        
        with open(priv_key_path, "wb") as priv_file:
            priv_file.write(private_key)
        
        with open(pub_key_path, "wb") as pub_file:
            pub_file.write(public_key)
            
        return priv_key_path, pub_key_path, folder_was_cleared
    
    except Exception as e:
        print(f"Error saving keys: {e}")
        return None, None, False