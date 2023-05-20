from datetime import datetime


class Transfer:
    current_time = str(datetime.now())
    date, time = current_time.strip().split()
    week_day = ""
    day = ""
    point = '1'
    bought = '1'
    loyal = '1'
    orders = '1'
    number = 0
    order_id = '123'

    def register(self, phone, name):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("school-diary-f3a73-firebase-adminsdk-xvqli-73aadbafa6.json")
                initialize_app(cred, {'databaseURL': 'https://school-diary-f3a73-default-rtdb.firebaseio.com/'})
                ref = db.reference('Diary').child("Teacher").child(phone)
                ref.set(
                    {
                        'password': name,
                        'phone': phone,

                    })

    def get_login(self, phone, passe):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("school-diary-f3a73-firebase-adminsdk-xvqli-73aadbafa6.json")
                initialize_app(cred, {'databaseURL': 'https://school-diary-f3a73-default-rtdb.firebaseio.com/'})
                ref = db.reference('Diary').child("Teacher").child(phone)

                data = ref.get()

                if phone in data:

                    if passe == data[phone]["password"]:
                        return True
                else:
                    return False

    def classes(self, name):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("school-diary-f3a73-firebase-adminsdk-xvqli-73aadbafa6.json")
                initialize_app(cred, {'databaseURL': 'https://school-diary-f3a73-default-rtdb.firebaseio.com/'})
                ref = db.reference('Diary').child("classes").child(name)
                ref.set(
                    {
                        'class': name,

                    })

    def add_student(self, idd, level, name, phone):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("school-diary-f3a73-firebase-adminsdk-xvqli-73aadbafa6.json")
                initialize_app(cred, {'databaseURL': 'https://school-diary-f3a73-default-rtdb.firebaseio.com/'})
                ref = db.reference('Diary').child("student").child(idd)
                ref.set(
                    {
                        'ID': idd,
                        'Name': name,
                        "Parent_Phone": phone,

                    })
                ref = db.reference('Diary').child("classes").child(level).child("students").child(idd)
                ref.set(
                    {
                        'ID': idd,
                        'Name': name,
                        "Parent_Phone": phone,
                    }
                )

    def get_class(self, level):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("school-diary-f3a73-firebase-adminsdk-xvqli-73aadbafa6.json")
                initialize_app(cred, {'databaseURL': 'https://school-diary-f3a73-default-rtdb.firebaseio.com/'})
                ref = db.reference('Diary').child("classes").child(level).child("students")
                data = ref.get()

                return data

    def update_homework(self, level, work):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("school-diary-f3a73-firebase-adminsdk-xvqli-73aadbafa6.json")
                initialize_app(cred, {'databaseURL': 'https://school-diary-f3a73-default-rtdb.firebaseio.com/'})
                ref = db.reference('Diary').child("classes").child(level).child("students").child("homework")
                ref.set({
                    "Homework": work,
                }
                )


# Transfer.get_class(Transfer() ,"class3")
