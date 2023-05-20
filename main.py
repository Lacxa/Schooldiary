import random
import re
import string

import phonenumbers
from kivy import utils
from kivy.clock import Clock
from kivy.core.window import Window
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

    # APP
    screens = ['entrance']
    screens_size = NumericProperty(len(screens) - 1)
    current = StringProperty(screens[len(screens) - 1])
    t_phone = StringProperty("")
    t_name = StringProperty("")

    # class
    class_name = StringProperty("")
    class_level = StringProperty("class3")

    # student
    student_id = StringProperty("")
    attend_id = ListProperty([])

    def build(self):
        pass

    def on_start(self):
        pass
        # self.display_student()

    def remember_me(self, phone, dust, name):
        with open("credential/admin.txt", "w") as fl:
            fl.write(phone + "\n")
            fl.write(dust)
        with open("credential/admin_info.txt", "w") as ui:
            ui.write(name)
        fl.close()
        ui.close()

    def add_class(self, name):
        TR.classes(TR(), name)

    def get_class(self, classes):
        self.class_name = TR.get_class(TR(), classes)

    def listen_class(self):
        import firebase_admin
        firebase_admin._apps.clear()
        from firebase_admin import credentials, initialize_app, db
        if not firebase_admin._apps:
            cred = credentials.Certificate("school-diary-f3a73-firebase-adminsdk-xvqli-73aadbafa6.json")
            initialize_app(cred, {'databaseURL': 'https://school-diary-f3a73-default-rtdb.firebaseio.com/'})
            ref = db.reference('Diary').child("Teacher").child("classes").listen(self.get_class)

    def validate_user(self, phone, name):
        if not self.phone_number_check_admin(phone):
            toast("please enter your phone number correctly")
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
            self.screen_capture("login")
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
        from database import Transfer as TR
        try:
            TR.register(TR(), phone, name)
            self.screen_capture("home")
        except:
            toast('OPPs!, No connection')

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

    def add_student(self, idd, level, name, phone):
        TR.add_student(TR(), idd, level, name, phone)
        self.class_level = level

    def display_student(self):
        self.root.ids.studs.data = {}
        students = TR.get_class(TR(), self.class_level)

        if not students:
            self.root.ids.studs.data.append(
                {
                    "viewclass": "Student",
                    "name": "No student Yet!",
                    "route": "",
                    "lcn": "",
                    "price": "",
                    "seats": ""
                }
            )
            self.root.ids.attend.data.append(
                {
                    "viewclass": "Atend",
                    "name": "No student Yet!",
                    "route": "",
                    "lcn": "",
                    "price": "",
                    "seats": ""
                }
            )
        else:
            for i, y in students.items():
                self.root.ids.studs.data.append(
                    {
                        "viewclass": "Student",
                        "name": y["Name"]

                    }
                )
            for i, y in students.items():
                self.root.ids.attend.data.append(
                    {
                        "viewclass": "Atend",
                        "name": y["Name"],
                        "id": i

                    }
                )

    def upd_homework(self, level, work):
        if level == "":
            toast("Enter class level")

        elif work == "":
            toast("Enter work")

        else:
            TR.update_homework(TR(), level, work)

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
