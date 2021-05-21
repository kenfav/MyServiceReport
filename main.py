from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

class MyServiceReportApp(ScreenManager):
    pass

class MainScreen(Screen):
    def do_registry_activity(self, *args):
       lista = [] 
       for arg in args:
           lista.append(arg)
       print(lista)
       return lista


class MainMenu(Screen):
    pass


class My(App):
    def build(self):
        return MyServiceReportApp()


My().run()
