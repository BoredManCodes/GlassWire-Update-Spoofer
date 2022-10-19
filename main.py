import subprocess
import sys
from selenium import webdriver
import winreg
from selenium.webdriver.common.by import By

REG_PATH = r"SOFTWARE\GlassWire"


def set_reg(name, value):
    try:
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0,
                                      winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
        winreg.CloseKey(registry_key)
        return True
    except WindowsError:
        return False


def get_reg(name):
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0,
                                      winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(registry_key, name)
        winreg.CloseKey(registry_key)
        return value
    except WindowsError:
        return None


glasswire_download_page = "https://www.glasswire.com/download/"
options = webdriver.ChromeOptions()
# options.add_argument("--window-size=1920x1080")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
# options.add_argument('--headless')
driver = webdriver.Chrome('./chromedriver.exe', options=options)
driver.get(glasswire_download_page)
version_xpath = "/html/body/div[1]/div[3]/div/div[2]/div[1]/div[2]/div/div[3]/span"
version_area = driver.find_element(By.XPATH, version_xpath)
version_string = f"{version_area.text.strip('Version ').split(', ')[0]}.0"
driver.quit()
print(f"Latest Available Version: >{version_string}<")
print(f"Current Version Installed: >{get_reg('LastInstallationVersion')}<")
set_reg('LastInstallationVersion', str(version_string))
print(f"Set Current Version Installed to: >{get_reg('LastInstallationVersion')}<")
print("Starting Glasswire after spoofing update")
subprocess.Popen('"C:\Program Files (x86)\GlassWire\GlassWire.exe" -hide')
sys.exit(0)
