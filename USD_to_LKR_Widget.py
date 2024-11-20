from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from tkinter import *
from tkinter.ttk import Label
from tkinter import messagebox

import subprocess
import ctypes
import sys
import os
import shutil
import requests
from zipfile import ZipFile


def update_in_admin():
    # Hide the console window
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

    if ctypes.windll.shell32.IsUserAnAdmin():
        # check the existing version from the chromedriver.exe file
        command1 = fr"C: && cd C:\Program Files (x86) && chromedriver.exe -v"
        process = subprocess.run(command1, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
        output = process.stdout
        # extract string of the version part only
        version_exist = output[11:28].strip('r( ')
        print("Exist Version: ", version_exist)
        # stable version check via internet
        r1 = requests.get("https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE")
        version_stable = r1.text
        print("Latest Stable Version: ", version_stable)

        # check the versions
        if version_stable == version_exist:
            # if versions are the same then stop update process
            print("You have the latest version!")
        else:
            # if verisons are different start update process
            print("Update!")
            try:
                # delete existing chromedriver.exe file (older version)
                command2 = r"C: && cd C:\Program Files (x86) && del chromedriver.exe"
                subprocess.run(command2, shell=True, stdout=subprocess.PIPE, universal_newlines=True)

            except Exception as msg1:
                print(msg1)

            try:
                # Adding stable version number to the url
                r2 = requests.get(
                    f'https://storage.googleapis.com/chrome-for-testing-public/{version_stable}/win64/chromedriver-win64.zip')
                # Download the content zip file
                print("Downloading Stable version!")
                with open('C:/Program Files (x86)/chromedriver-win64.zip', 'wb') as f1:
                    f1.write(r2.content)
            except Exception as msg2:
                print(msg2)

            filename = "C:/Program Files (x86)/chromedriver-win64.zip"
            with ZipFile(filename, 'r') as z:
                # Extract the zip file to the root folder
                z.extract('chromedriver-win64/chromedriver.exe', 'C:/Program Files (x86)')
                print(f"{z.namelist()[2]} Extracted!")
                # Move the chromedriver.exe file to the destination folder from the extracted folder
                try:
                    print("Moved file to the destination!")
                    shutil.move('C:/Program Files (x86)/chromedriver-win64/chromedriver.exe',
                                'C:/Program Files (x86)')

                except Exception as msg3:
                    print(msg3)

            # Removing Temporary files and folders
            command4 = r"C: && cd C:\Program Files (x86) && del /f /q chromedriver-win64.zip"
            subprocess.run(command4, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
            os.rmdir('C:/Program Files (x86)/chromedriver-win64')
            print("Removed Temporary files and folders!")
            print("Done!")
    else:
        # Restart the script with admin privileges
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()


if __name__ == '__main__':
    try:
        root = Tk()
        root.overrideredirect(True)
        root.title("USD to LKR")
        root.geometry('240x90+1200+700')
        root.resizable(0,0)
        root.config(background='#524582')

        try:
            update_in_admin()
        except:
            pass
        else:

            options = webdriver.ChromeOptions()
            options.add_argument("--headless=new")  # Chrome will not open due to headless option

            driver = webdriver.Chrome(service=Service(executable_path=r"C:\Program Files (x86)\chromedriver.exe"), options=options)
            driver.get("https://www.cbsl.gov.lk/en/rates-and-indicators/exchange-rates")

            driver.switch_to.frame("myiFrame4")
            labels = driver.find_elements(By.XPATH, "/html/body/div/p")


            def exit_com(event):
                root.quit()


            root.bind("<Button-3>", exit_com)
            root.bind("<F12>", exit_com)
            frame1 = Frame(root, bg='#524582')
            frame2 = Frame(frame1, bg='#524582')
            frame1.bind("<Button-3>", exit_com)
            frame2.bind("<Button-3>", exit_com)
            frame1.pack()
            frame2.pack(side=RIGHT)

            dd = Label(frame1, text="Exchange Rate USD/LKR", background="#524582", font=("Safety", 8))
            dd.config(foreground='#367BC3')
            dd.pack()
            a = Label(frame1, text=labels[0].text, background="#524582", font=("Safety", 8))
            a.config(foreground='#38BFA7')
            a.pack()
            b = Label(frame1, text=labels[1].text, background="#524582", font=("Safety", 8))
            b.config(foreground='#38BFA7')
            b.pack()
            c = Label(frame1, text=labels[2].text, background="#524582", font=("Safety", 8))
            c.config(foreground='#8FE1A2')
            c.pack()
            d = Label(frame1, text="Click F12 or Right click to Close", background="#524582", font=("Arial", 7))
            d.pack()


            def clicked():
                try:
                    driver.get("https://www.cbsl.gov.lk/en/rates-and-indicators/exchange-rates")
                    driver.switch_to.frame("myiFrame4")
                    labels_update = driver.find_elements(By.XPATH, "/html/body/div/p")
                    a.config(text=labels_update[0].text)
                    b.config(text=labels_update[1].text)
                    c.config(text=labels_update[2].text)
                except:
                    messagebox.showerror("USD to LKR Widget", "No Internet!\nPlease Turn on the Internet and \ntry to click UPDATE!")
                    a.config(text="Indicative              ---    ")
                    b.config(text="Buy                     ---    ")
                    c.config(text="Sell                    ---    ")


            update_btn = Button(frame2, text="UPDATE", fg='#367BC3', bg='#38BFA7', height=2, width=10, command=clicked, font=("Safety", 8))
            update_btn.grid()

            root.mainloop()

            driver.quit()

    except:
        messagebox.showerror("USD to LKR Widget", "No Internet!\nPlease Turn on the Internet and try to run again!")
