import os
from Registry import Registry


# ------------------------------------------------------------
# 1. INSTALLED APPLICATIONS (SOFTWARE)
# ------------------------------------------------------------
def get_installed_apps(path):
    print("\n=== Installed Applications ===")
    try:
        reg = Registry.Registry(path)
        uninstall_key = reg.open("Microsoft\\Windows\\CurrentVersion\\Uninstall")

        for subkey in uninstall_key.subkeys():
            values = {v.name(): v.value() for v in subkey.values()}
            app = values.get("DisplayName")
            version = values.get("DisplayVersion")
            if app:
                print(f"- {app} (Version: {version})")
    except Exception as e:
        print(f"[Error] Could not read installed applications: {e}")


# ------------------------------------------------------------
# 2. USER ACCOUNTS (SAM)
# ------------------------------------------------------------
def get_user_accounts(path):
    print("\n=== User Accounts (SAM) ===")
    try:
        reg = Registry.Registry(path)
        names_key = reg.open("SAM\\Domains\\Account\\Users\\Names")

        for user in names_key.subkeys():
            print(f"- {user.name()}")

    except Exception as e:
        print(f"[Error] Could not read SAM users: {e}")


# ------------------------------------------------------------
# 3. USB DEVICE HISTORY (SYSTEM)
# ------------------------------------------------------------
def get_usb_history(path):
    print("\n=== USB Device History ===")
    try:
        reg = Registry.Registry(path)
        usb_key = reg.open("Enum\\USBSTOR")

        for device in usb_key.subkeys():
            print(f"Device: {device.name()}")
            for instance in device.subkeys():
                try:
                    fname = instance.value("FriendlyName").value()
                except:
                    fname = "Unknown"
                print(f"  Instance: {instance.name()} | Friendly Name: {fname}")

    except Exception as e:
        print(f"[Error] Could not read USB history: {e}")


# ------------------------------------------------------------
# 4. RUN MRU HISTORY (NTUSER.DAT)
# ------------------------------------------------------------
def get_command_history(path):
    print("\n=== User Run Dialog History (NTUSER.DAT) ===")
    try:
        reg = Registry.Registry(path)
        run_key = reg.open("Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RunMRU")

        for v in run_key.values():
            if v.name() != "MRUList":
                print(f"- {v.value()}")

    except Exception as e:
        print(f"[Error] Could not read RunMRU: {e}")


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
def main():
    print("=== Windows Registry Forensic Analyzer ===")

    folder = r"D:\Gam3a\forsencis\extraction1"

    files = {
        "SAM": os.path.join(folder, "SAM"),
        "SYSTEM": os.path.join(folder, "SYSTEM"),
        "SOFTWARE": os.path.join(folder, "SOFTWARE"),
        "NTUSER.DAT": os.path.join(folder, "NTUSER.DAT")
    }

    # Check files
    for name, path in files.items():
        if not os.path.exists(path):
            print(f"[Warning] {name} not found at: {path}")

    # Run each module if hive exists
    if os.path.exists(files["SOFTWARE"]):
        get_installed_apps(files["SOFTWARE"])

    if os.path.exists(files["SAM"]):
        get_user_accounts(files["SAM"])

    if os.path.exists(files["SYSTEM"]):
        get_usb_history(files["SYSTEM"])

    if os.path.exists(files["NTUSER.DAT"]):
        get_command_history(files["NTUSER.DAT"])

    print("\n=== Analysis Complete ===")


if __name__ == "__main__":
    main()
