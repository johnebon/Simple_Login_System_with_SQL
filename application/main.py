from kivy.config import Config
Config.set('graphics', 'width', '320')
Config.set('graphics', 'height', '180')
Config.set('graphics', 'resizable', '0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from kivy.lang import Builder
import sqlite3
import subprocess as sp
import os
import kivy

#переход в директорию проекта
os.chdir('kivy/application/')

Builder.load_file('main.kv')

class FirstScreen(Screen):
    def login(self):
        """login function (check row in database)"""
        usr = self.ids.input_usr.text.strip()
        pwd = self.ids.input_pwd.text.strip()
        if len(usr) > 0 and len(pwd) > 0:
            with sqlite3.connect('main.db') as db: # kivy/app для нужной директории
                cur = db.cursor()
                cur.execute("""CREATE TABLE IF NOT EXISTS users(
                    username TEXT,
                    password TEXT
                )""")
                cur.execute(f"SELECT username FROM users WHERE username='{usr}' AND password='{pwd}'")
                if not cur.fetchone():
                    self.manager.current = 'error'
                else:
                    self.manager.current = 'signedin'


                db.commit()
                
        self.ids.input_usr.text = ''
        self.ids.input_pwd.text = ''

    def register(self):
        """register function (add new row to databse)"""
        usr = self.ids.input_usr.text.strip()
        pwd = self.ids.input_pwd.text.strip()
        if len(usr) > 0 and len(pwd) > 0:
            with sqlite3.connect('main.db') as db:
                    cur = db.cursor()
                    cur.execute("""CREATE TABLE IF NOT EXISTS users(
                            username TEXT,
                            password TEXT
                        )""")
                    cur.execute(f"SELECT * FROM users WHERE username='{usr}'")
                    value = cur.fetchall()
                    if value != []:
                        self.manager.current = 'error'
                    else:
                        cur.execute(f"INSERT INTO users VALUES('{usr}', '{pwd}')")
                        db.commit()
                        self.manager.current = 'signedup'
        else:
            self.manager.current = 'error'
            
        self.ids.input_usr.text = ''
        self.ids.input_pwd.text = ''

class SignedIn(Screen):
    def back(self):
        self.manager.current = 'fs'

class SignedUp(Screen):
    def back(self):
        self.manager.current = 'fs'

class Error(Screen):
    def back(self):
        self.manager.current = 'fs'

class MainApp(App):
    def build(self):
        self.icon = 'password-icon.jpeg'
        #Window.clearcolor = .25, .25, .25, 1
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(FirstScreen(name='fs'))
        sm.add_widget(SignedIn(name='signedin'))
        sm.add_widget(SignedUp(name='signedup'))
        sm.add_widget(Error(name='error'))
        return sm


if __name__ == '__main__':
    MainApp().run()