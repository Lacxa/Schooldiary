import os
import random
import re
import string

import phonenumbers
from kivy import utils
from kivy.clock import Clock
from beem import sms as SM
from kivy.core.window import Window
from kivy.core.window.window_x11 import EventLoop
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.tab import MDTabsBase

from beem import OTP as tp
from database import Transfer as TR
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.textfield import MDTextField
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type

if utils.platform != 'android':
    Window.size = [360, 640]


class Tab(MDBoxLayout, MDTabsBase):
    pass


class Emerge(MDBoxLayout):
    pass


class NumberOnlyField(MDTextField):
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):

        pat = self.pat

        if "." in self.text:
            s = re.sub(pat, "", substring)

        else:
            s = ".".join([re.sub(pat, "", s) for s in substring.split(".", 1)])

        return super(NumberOnlyField, self).insert_text(s, from_undo=from_undo)


class MainApp(MDApp):
    user_pin = StringProperty('')
    size_x, size_y = Window.size

    # APP
    screens = ['inclass']
    screens_size = NumericProperty(len(screens) - 1)
    current = StringProperty(screens[len(screens) - 1])
    t_phone = StringProperty("")
    t_name = StringProperty("")

    phone = StringProperty("")

    # class
    class_name = StringProperty("")
    class_level = StringProperty("")
    class_fetch = StringProperty("")

    # student
    student_id = StringProperty("")
    attend_id = ListProperty([])
    read = StringProperty("")
    stidd = StringProperty("")

    def build(self):
        pass

    def on_start(self):
        self.attend_id = []
        self.keyboard_hooker()
        Clock.schedule_once(lambda x: self.register_check(), .1)

    def add_class(self, name):
        TR.classes(TR(), name)
        self.remember_class(name)

    def id_generator(self):
        num = string.digits
        letter = string.ascii_letters

        rr = num + letter

        z = random.choice(rr)
        a = random.choice(rr)
        v = random.choice(rr)
        f = random.choice(rr)
        t = random.choice(rr)
        w = random.choice(rr)

        self.student_id = z + a + v + f + t + w

    def add_student(self, idd, name, phone):
        if not self.phone_number_check_admin(phone):
            toast("Enter valid phone number")
        elif name == "":
            toast("Enter name")
        else:
            TR.add_student(TR(), idd, self.class_name, name, phone)

    def get_class(self, mm):
        print("called")
        self.display_student()
        self.display_attendance()
        self.display_result()

    def listen_class(self, level):
        import firebase_admin
        firebase_admin._apps.clear()
        from firebase_admin import credentials, initialize_app, db
        if not firebase_admin._apps:
            cred = credentials.Certificate("school-diary-f3a73-firebase-adminsdk-xvqli-73aadbafa6.json")
            initialize_app(cred, {'databaseURL': 'https://school-diary-f3a73-default-rtdb.firebaseio.com/'})
            self.search = db.reference('Diary').child("classes").child(level).child("students").listen(self.get_class)
            print("fuction")

    def send_txt(self, sms):
        data = TR.get_phone_number(TR(), self.class_name)
        for i, y in data.items():
            self.phone = y["Parent_Phone"]
            print(self.phone)

            if SM.send_sms(self.phone, sms):
                toast("send successful")

    def display_student(self):
        self.root.ids.studs.data = {}
        students = TR.get_class(TR(), self.class_name)

        if not students:
            self.root.ids.studs.data.append(
                {
                    "viewclass": "Student",
                    "name": "No student Yet!",

                }
            )
        else:
            for i, y in students.items():
                self.root.ids.studs.data.append(
                    {
                        "viewclass": "Student",
                        "name": y["Name"],
                        "id": i

                    }
                )

    def display_attendance(self):
        self.root.ids.attend.data = {}
        students = TR.get_class(TR(), self.class_name)

        if not students:
            self.root.ids.attend.data.append(
                {
                    "viewclass": "Atendx",
                    "name": "No student Yet!",

                }
            )
        else:
            for i, y in students.items():
                self.root.ids.attend.data.append(
                    {
                        "viewclass": "Atend",
                        "name": y["Name"],
                        "id": i

                    }
                )

    def display_result(self):
        self.root.ids.results.data = {}
        students = TR.get_class(TR(), self.class_name)

        if not students:
            self.root.ids.results.data.append(
                {
                    "viewclass": "Result",
                    "name": "No student Yet!",

                }
            )
        else:
            for i, y in students.items():
                self.root.ids.results.data.append(
                    {
                        "viewclass": "Result",
                        "name": y["Name"],
                        "idd": i

                    }
                )

    def upd_homework(self, work):
        if work == "":
            toast("Enter homework")

        else:
            TR.update_homework(TR(), self.class_name, work)
            toast("updated")

    def update_result(self, math, eng, history, science, geo):
        TR.update_result(TR(), self.class_name, self.stidd, math, eng, history, science, geo)

    def attend(self, save):
        self.attend_id.append(save)
        print(self.attend_id)

    def student(self, idd):
        self.stidd = idd
        print(self.stidd)

    def remove_attend(self, stud):

        self.attend_id.remove(stud)
        print(self.attend_id)

    def attendance(self):
        if not self.attend_id:
            toast("Select Students")
        else:
            TR.update_attendance(TR(), self.read, self.attend_id)
            toast("Attendance accepted")

    def validate_user(self, phone, name):
        if not self.phone_number_check_admin(phone):
            toast("Enter your phone number correctly")
        elif name == "":
            toast("please enter your password")
        else:
            self.t_phone = phone
            self.t_name = name
            self.phone_verify(phone)

    def user_login(self, phone, passe):

        if TR.get_login(TR(), phone, passe):
            self.screen_capture("home")
        else:
            toast("Invalid login")

    def phone_verify(self, phone):
        toast('wait a moment')
        tp.req.otp_req(tp.req(), phone)
        self.screen_capture("Verify")

    def verify(self, pin):
        if tp.req.verfy(tp.req(), pin):
            Clock.schedule_once(lambda x: self.register_caller(self.t_phone, self.t_name), 1)
        else:
            toast("Try again")

    def phone_number_check_admin(self, phone):
        new_number = ""
        if phone != "" and len(phone) == 10:
            for i in range(phone.__len__()):
                if i == 0:
                    pass
                else:
                    new_number = new_number + phone[i]
            number = "+255" + new_number
            if not carrier._is_mobile(number_type(phonenumbers.parse(number))):
                toast("Please check your phone number!", 1)
                return False
            else:
                self.public_number = number
                return True
        else:
            toast("enter phone number!")

    def register_caller(self, phone, name):
        try:
            TR.register(TR(), phone, name)
            self.screen_capture("login")
        except:
            toast('OPPs!, No connection')

    def remember_class(self, name):
        with open("class.txt", "w") as fl:
            fl.write(name)
            self.class_name = name
        fl.close()

    def register_check(self):
        sm = self.root
        file_size = os.path.getsize("class.txt")
        if file_size == 0:
            pass
        else:
            self.readf()

    def readf(self):
        with open("class.txt", "r") as fl:
            read = fl.readlines()
            self.read = read[0]
            self.class_name = self.read
            self.listen_class(self.class_name)
            self.screen_capture("inclass")

        fl.close()

    def keyboard_hooker(self, *args):
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *largs):
        print(self.screens_size)
        if key == 27 and self.screens_size > 0:
            print(f"your were in {self.current}")
            last_screens = self.current
            self.screens.remove(last_screens)
            print(self.screens)
            self.screens_size = len(self.screens) - 1
            self.current = self.screens[len(self.screens) - 1]
            self.screen_capture(self.current)
            return True
        elif key == 27 and self.screens_size == 0:
            toast('Press Home button!')
            return True

    def screen_capture(self, screen):
        sm = self.root
        sm.current = screen
        if screen in self.screens:
            pass
        else:
            self.screens.append(screen)
        print(self.screens)
        self.screens_size = len(self.screens) - 1
        self.current = self.screens[len(self.screens) - 1]
        print(f'size {self.screens_size}')
        print(f'current screen {screen}')


MainApp().run()
