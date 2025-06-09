import os
import shutil

def save_keys(private_key, public_key, usb_path, public_key_path, key_name):
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