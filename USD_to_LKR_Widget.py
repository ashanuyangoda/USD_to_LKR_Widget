from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from tkinter import *
from tkinter.ttk import Label, LabelFrame

root = Tk()
root.overrideredirect(True)
root.title("USD to LKR")
root.geometry('240x90+1200+700')
root.resizable(0,0)
root.config(background='#524582')

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
    driver.get("https://www.cbsl.gov.lk/en/rates-and-indicators/exchange-rates")
    driver.switch_to.frame("myiFrame4")
    labels_update = driver.find_elements(By.XPATH, "/html/body/div/p")
    a.config(text=labels_update[0].text)
    b.config(text=labels_update[1].text)
    c.config(text=labels_update[2].text)


update_btn = Button(frame2, text="UPDATE", fg='#367BC3', bg='#38BFA7', height=2, width=10, command=clicked, font=("Safety", 8))
update_btn.grid()

root.mainloop()

driver.quit()