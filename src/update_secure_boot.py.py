import plistlib
import os
import sys
import subprocess
import shutil
from datetime import datetime
import getpass


def find_efi_partition():
    try:
        output = subprocess.check_output(["diskutil", "list"]).decode()
        for line in output.splitlines():
            if "EFI" in line:
                parts = line.split()
                efi_device = parts[0].replace(":", "")
                efi_device = "/dev/disk0s%s" % efi_device
                return efi_device
    except subprocess.CalledProcessError as e:
        print(f"Failed to list disks: {e}")
        sys.exit(1)

    print("No EFI partition found.")
    sys.exit(1)

def is_efi_device_mounted(efi_device):
    try:
        output = subprocess.check_output(["mount"]).decode()
        for line in output.splitlines():
            if efi_device in line:
                return True
        return False
    except subprocess.CalledProcessError as e:
        print(f"Failed to list disks: {e}")
        sys.exit(1)

def mount_efi_partition(efi_device):
    mount_point = "/Volumes/EFI"
    mount_path_exists = os.path.exists(mount_point)
    efi_device_mounted = is_efi_device_mounted(efi_device)
    if not mount_path_exists or not efi_device_mounted:
        # Prompt user for password
        password = getpass.getpass("Enter your password for elevated privileges: ")
    try:
        if not mount_path_exists:
            subprocess.run(f'echo {password} | sudo -S mkdir -p {mount_point}', shell=True, check=True)
        if not efi_device_mounted:
            # Use echo to pass the password to sudo
            subprocess.run(f'echo {password} | sudo -S mount_msdos {efi_device} {mount_point}', shell=True, check=True)
        print(f"Mounted EFI partition at {mount_point}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to mount EFI partition: {e}")
        sys.exit(1)


def backup_config(config_path):
    if os.path.exists(config_path):
        backup_path = f"{config_path}.{datetime.now().strftime('%Y%m%d%H%M%S')}.bak"
        shutil.copy2(config_path, backup_path)
        print(f"Backup created: {backup_path}")
    else:
        print(f"No config file found at {config_path} to backup.")


def update_secure_boot_model(config_path, new_value):
    with open(config_path, 'rb') as plist_file:
        config = plistlib.load(plist_file)

    config["Misc"]["Security"]['SecureBootModel'] = new_value

    with open(config_path, 'wb') as plist_file:
        plistlib.dump(config, plist_file)

    print(f"Updated SecureBootModel to {new_value} in {config_path}")


if __name__ == "__main__":
    efi_device = find_efi_partition()
    password = getpass.getpass("Enter your password for elevated privileges: ")
    mount_efi_partition(efi_device)

    config_path = "/Volumes/EFI/EFI/OC/config.plist"  # Update the path accordingly

    if len(sys.argv) != 2 or sys.argv[1] not in ["Default", "Disabled"]:
        print("Usage: python update_secure_boot.py [Default|Disabled]")
        sys.exit(1)



    backup_config(config_path)

    secure_boot_value = sys.argv[1]

    update_secure_boot_model(config_path, secure_boot_value)
