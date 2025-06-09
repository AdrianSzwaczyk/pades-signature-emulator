import psutil

def get_usb_devices():
    """! 
    @brief Detecting USB devices connected to the system.

    @details This function uses the psutil library to list all disk partitions and filters them to find removable devices (so basicly typical USB drivers).

    @return A list of found and filtered USB device paths.
    """
    partitions = psutil.disk_partitions()
    usb_devices = [p.device for p in partitions if 'removable' in p.opts]
    return usb_devices