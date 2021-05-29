from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivy.config import Config
import MyService

Config.set('graphics','width', '450')
Config.set('graphics','heigth', '800')
class MyServiceReportApp(ScreenManager):
    pass

class ErrorPopUp(Popup):
    pass

class MainScreen(Screen):
    def do_registry_activity(self, *args):
        lista = []
        for arg in args:
            lista.append(arg)
        try:
            print(lista)
            My.db.add_to_database(lista)
            self.clear_fields()
        except (ValueError,NameError):
            print('to aqui')
            self.clear_fields()
            Factory.ErrorPopUp().open()

    def clear_fields(self):
        self.ids.report1.text = ''
        self.ids.report2.text = ''
        self.ids.report3.text = ''
        self.ids.report4.text = ''
        self.ids.report5.text = ''

    def activity_summary(self):
        print(My.db.soma_mes())

class MainMenu(Screen):
    pass


class My(App):
    db = MyService.MainApp('MyServiceReport.db')
    def build(self):
        return MyServiceReportApp()



My().run()
