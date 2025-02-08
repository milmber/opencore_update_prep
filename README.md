# opencore_update_prep
Script to prepare for MacOS 14 and later updates by configuring OpenCore Settings.

At the moment this script only supports
1. Fnding and mounting the EFI partition
2. Creating a backup of the "config.plist" file
3. Setting the "SecureBootModel" value in the "config.plist" file

# Usage

## Before Updating MacOS

1. Run `python update_secure_boot.py Disable`
2. Enter your administrative password to allow the EFI partition to be mounted.
3. Verify the change in the "config.plist" file
4. Reboot for changes to take effect

### After Updating MacOS

1. Run `python update_secure_boot.py Default`
2. Enter your administrative password to allow the EFI partition to be mounted.
3. Verify the change in the "config.plist" file
4. Reboot for changes to take effect