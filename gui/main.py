from tkinter import *
from tkinter import filedialog

import os
import sys
import time
from tkinter import messagebox
from unittest import expectedFailure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    UnexpectedAlertPresentException,
    NoSuchElementException,
)
from webdriver_manager.chrome import ChromeDriverManager

import csv


class WhatsApp(object):
    def __init__(self, browser=None):
        self.BASE_URL = "https://web.whatsapp.com/"
        # self.suffix_link = "https://wa.me/"
        self.suffix_link = "https://web.whatsapp.com/send?phone="

        if not browser:
            browser = webdriver.Chrome(
                ChromeDriverManager().install(),
                options=self.chrome_options,
            )

        self.browser = browser

        self.wait = WebDriverWait(self.browser, 600)
        self.login()
        self.mobile = ""

    @property
    def chrome_options(self):
        chrome_options = Options()
        if sys.platform == "win32":
            chrome_options.add_argument("--profile-directory=Default")
            chrome_options.add_argument("--user-data-dir=C:/Temp/ChromeProfile")
        else:
            chrome_options.add_argument("start-maximized")
            chrome_options.add_argument("--user-data-dir=./User_Data")
        return chrome_options

    def login(self):
        self.browser.get(self.BASE_URL)
        self.browser.maximize_window()

    def logout(self):
        prefix = "//div[@id='side']/header/div[2]/div/span/div[3]"
        dots_button = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    f"{prefix}/div[@role='button']",
                )
            )
        )
        dots_button.click()

        logout_item = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    f"{prefix}/span/div[1]/ul/li[last()]/div[@role='button']",
                )
            )
        )
        logout_item.click()

    def get_phone_link(self, mobile) -> str:

        return f"{self.suffix_link}{mobile}"

    def catch_alert(self, seconds=3):

        try:
            WebDriverWait(self.browser, seconds).until(EC.alert_is_present())
            alert = self.browser.switch_to_alert.accept()
            return True
        except Exception as e:
            print(e)
            return False

    def find_user(self, mobile) -> None:

        try:
            self.mobile = mobile
            link = self.get_phone_link(mobile)
            self.browser.get(link)
            # return
            self.catch_alert()
            return
            action_button = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="action-button"]'))
            )
            action_button.click()
            time.sleep(2)
            go_to_web = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="fallback_block"]/div/div/a')
                )
            )
            go_to_web.click()
            time.sleep(1)
            return
        except UnexpectedAlertPresentException as bug:
            print(bug)
            time.sleep(1)
            self.find_user(mobile)

    def find_by_username(self, username):

        try:
            search_box = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="side"]/div[1]/div/label/div/div[2]')
                )
            )
            search_box.clear()
            search_box.send_keys(username)
            search_box.send_keys(Keys.ENTER)
        except Exception as bug:
            error = f"Exception raised while finding user {username}\n{bug}"
            print(error)

    def username_exists(self, username):

        try:
            search_box = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="side"]/div[1]/div/label/div/div[2]')
                )
            )
            search_box.clear()
            search_box.send_keys(username)
            search_box.send_keys(Keys.ENTER)
            opened_chat = self.browser.find_element_by_xpath(
                "/html/body/div/div[1]/div[1]/div[4]/div[1]/header/div[2]/div[1]/div/span"
            )
            title = opened_chat.get_attribute("title")
            if title.upper() == username.upper():
                return True
            else:
                return False
        except Exception as bug:
            error = f"Exception raised while finding user {username}\n{bug}"
            print(error)

    def send_message(self, message):

        try:
            inp_xpath = (
                '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]'
            )

            input_box = self.wait.until(
                EC.presence_of_element_located((By.XPATH, inp_xpath))
            )
            print(input_box)
            input_box.send_keys(message + Keys.ENTER)
            return
            print(f"Message sent successfuly to {self.mobile}")
            self.browser.get("https://web.whatsapp.com/")
            self.catch_alert()
            return

        except (NoSuchElementException, Exception) as bug:
            print(bug)
            print(f"Failed to send a message to {self.mobile}")

        finally:
            print("send_message() finished running ")

    def find_attachment(self):
        clipButton = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="main"]/footer//*[@data-icon="clip"]/..')
            )
        )
        clipButton.click()

    def send_attachment(self):
        # Waiting for the pending clock icon to disappear
        self.wait.until_not(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="main"]//*[@data-icon="msg-time"]')
            )
        )

        sendButton = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div/span',
                )
            )
        )
        sendButton.click()

    def send_picture(self, picture):

        try:
            filename = os.path.realpath(picture)
            self.find_attachment()
            # To send an Image
            imgButton = self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="main"]/footer//*[@data-icon="attach-image"]/../input',
                    )
                )
            )
            imgButton.send_keys(filename)
            self.send_attachment()
            print(f"Picture has been successfully sent to {self.mobile}")
        except (NoSuchElementException, Exception) as bug:
            print(bug)
            print(f"Failed to send a picture to {self.mobile}")

        finally:
            print("send_picture() finished running ")

    def send_video(self, video):

        try:
            filename = os.path.realpath(video)
            self.find_attachment()
            # To send a Video
            video_button = self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="main"]/footer//*[@data-icon="attach-image"]/../input',
                    )
                )
            )
            video_button.send_keys(filename)
            self.send_attachment()
            print(f"Video has been successfully sent to {self.mobile}")
        except (NoSuchElementException, Exception) as bug:
            print(bug)
            print(f"Failed to send a video to {self.mobile}")
        finally:
            print("send_video() finished running ")

    def send_file(self, filename):

        try:
            filename = os.path.realpath(filename)
            self.find_attachment()
            document_button = self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="main"]/footer//*[@data-icon="attach-document"]/../input',
                    )
                )
            )
            document_button.send_keys(filename)
            self.send_attachment()
        except (NoSuchElementException, Exception) as bug:
            print(bug)
            print(f"Failed to send a PDF to {self.mobile}")
        finally:
            print("send_file() finished running ")


def create_msg(name, hr_name, script_msg, num_script_var, var_values):

    script_msg = [msg.replace("CANDIDATE NAME", name) for msg in script_msg]
    script_msg = [msg.replace("HR NAME", hr_name) for msg in script_msg]
    a = ""
    for i in range(num_script_var):
        a = i + 1
        script_msg = [msg.replace(str(a) + "*", var_values[i]) for msg in script_msg]
    return script_msg

    # print(name, script_msg, num_script_var, var_values)


root = Tk()
# root.geometry('700x500')
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
# setting tkinter root size
root.geometry("%dx%d" % (width, height))
root.title("Tej WhatsApp")


global file_name


def shoot():
    logs_frame = Frame(root)

    for w in logs_frame.winfo_children():
        w.destroy()

    logs_frame.pack(padx=100)

    success_box = Scrollbar(logs_frame)
    error_box = Scrollbar(logs_frame)

    success_box.pack(side="left", fill=BOTH)
    error_box.pack(side="right", fill=BOTH)

    success_listbox = Listbox(logs_frame)
    error_listbox = Listbox(logs_frame)

    success_listbox.pack(side="left", fill=BOTH)
    error_listbox.pack(side="left", fill=BOTH)

    success_box.update_idletasks()
    error_box.update_idletasks()
    logs_frame.update_idletasks()

    try:
        msg = WhatsApp()
        rows = []
        with open(file_name, "r") as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                rows.append(row)

        hr_name = rows[0][1]

        script_msg = []
        script_msg = [i for i in rows[1]]
        script_msg = script_msg[1:]
        script_msg

        num_script_var = int(rows[2][1])

        data = []
        for i in range(4, len(rows)):
            candidate_name = rows[i][0]
            number = "91" + rows[i][1]
            status = rows[i][2]
            # print(rows[i])
            if status == "No":
                Meessages = create_msg(
                    candidate_name, hr_name, script_msg, num_script_var, rows[i][3:]
                )

                msg.find_user(number)
                for message in Meessages:
                    msg.send_message(message)
                    msg.catch_alert()
                success_listbox.insert(END, f"Messges sent to {candidate_name}")

        error_listbox.config(yscrollcommand=error_box.set)
        success_listbox.config(yscrollcommand=success_box.set)

        success_box.config(command=success_listbox.yview)
        error_box.config(command=error_listbox.yview)
    except:
        error_listbox.insert(END, f"Unable to send {candidate_name}")


def FileSelect():
    errors = [
        "Sahi file SELECT KER !!!",
        "Kya ker raha hai baad mei soo jana, SAHI FILE SELECT KERRRR !!!",
        "Tu rahne de, Phone utta aur message kerna START KER DE !!!",
    ]
    level = 0

    def select():
        nonlocal level
        filename = filedialog.askopenfilename()
        if not filename.endswith(".csv"):
            shoot_sleep["state"] = "disabled"
            # prevent children to append again on details_frame
            for w in detail_frame.winfo_children():
                w.destroy()

            messagebox.showerror("error", errors[level])
            level += 1
            if level > 2:
                root.destroy()
        else:
            level = 0
            global file_name
            file_name = filename
            # active the state of the shoot & sleep button
            shoot_sleep["state"] = "active"

            # prevent children to append again on details_frame
            for w in detail_frame.winfo_children():
                w.destroy()

            show_details()

    return select


def show_details():

    try:
        rows = []
        with open(file_name, "r") as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                rows.append(row)

        hr_name = rows[0][1]
        script_msg = []
        script_msg = [i for i in rows[1]]
        script_msg = script_msg[1:]
        final_messages = []

        already_done = 0

        num_script_var = int(rows[2][1])

        for i in range(4, len(rows)):
            candidate_name = rows[i][0]
            number = "91" + rows[i][1]
            status = rows[i][2]
            # print(rows[i])
            if status == "No":
                final_messages.append(
                    create_msg(
                        candidate_name, hr_name, script_msg, num_script_var, rows[i][3:]
                    )
                )
                print("asdfafd")
            else:
                already_done += 1

        left_detail_frame = Frame(detail_frame)
        right_detail_frame = Frame(detail_frame)

        name_lable = Label(left_detail_frame, text="HR Name", font="Helvetica 14 bold")
        name = Label(left_detail_frame, text=hr_name, font="Helvetica 14")
        name_lable.grid(row=5, column=3, padx=10)
        name.grid(row=5, column=4)

        name_lable = Label(
            left_detail_frame, text="Total Candidate", font="Helvetica 14 bold"
        )
        name = Label(left_detail_frame, text=str(len(rows) - 4), font="Helvetica 14")
        name_lable.grid(row=6, column=3, padx=10)
        name.grid(row=6, column=4)

        name_lable = Label(
            left_detail_frame, text="Already Done", font="Helvetica 14 bold"
        )
        name = Label(left_detail_frame, text=str(already_done), font="Helvetica 14")
        name_lable.grid(row=7, column=3, padx=10)
        name.grid(row=7, column=4)

        done_count = Label(
            right_detail_frame, text="0", foreground="blue", font="Helvetica4 40 bold"
        )
        total_count = Label(
            right_detail_frame,
            text=f"/  {len(rows) - 4 - already_done}",
            font="Helvetica 40 bold",
        )
        done_count.grid(row=7, column=10)
        total_count.grid(row=7, column=11, padx=10)

        left_detail_frame.pack(side="left")
        right_detail_frame.pack(side="right", pady=20)

        detail_frame.pack(fill="x", padx=300, pady=20)
    except:
        messagebox.showerror("error", "Please check correct format !")

    return


files_menu = Frame(root)
# bottom_frame = Frame(root)
detail_frame = Frame(root)

l2 = Label(root, text="Select the CSV filesafdsa: ")
l2.pack(side="bottom")
# bottom_frame.pack(fill='both', side='top')


l1 = Label(files_menu, text="Select the CSV file: ")
l1.pack(
    fill="x",
    side="left",
)


sel = FileSelect()


fileSelectButton = Button(files_menu, text="Select File", command=sel)
fileSelectButton.pack(fill="x", side="left")


shoot_sleep = Button(files_menu, text="Shoot & Sleep", command=shoot, state="disabled")
shoot_sleep.pack(fill="x", side="right")

files_menu.pack(fill="x", padx=100, pady=10)

root.mainloop()
