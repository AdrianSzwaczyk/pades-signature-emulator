import psutil

def get_usb_devices():
    partitions = psutil.disk_partitions()
    usb_devices = [p.device for p in partitions if 'removable' in p.opts]
    return usb_devices