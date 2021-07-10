from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivy.config import Config
import MyService
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout


Config.set('graphics', 'width', '450')
Config.set('graphics', 'heigth', '800')


class MyServiceReportApp(ScreenManager):

    def listar_atividades(self):
        self.lista_actividades = My.db.ordenar_lista_atividade()
        
        listbox = self.get_screen(name='list_activity').ids.listbox
        listbox.clear_widgets()
        
        for n in self.lista_actividades:
            listbox.add_widget(AtividadesDoMes(
                text=f'Date: {n[1][:10]}\nPublications: {n[2]}\nVideos: {n[3]}\nTime: {n[4]}\nReturn Visits: {n[5]}', myid=n[0]))

    def delete_widget(self, the_widget):
        self.get_screen(
            name='list_activity').ids.listbox.remove_widget(the_widget)
        My.db.remove_from_database(the_widget.myid)


class AtividadesDoMes(BoxLayout):
    myid = NumericProperty(None)

    def __init__(self, text='', myid=None, **kwargs):
        super().__init__(**kwargs)
        self.ids.mylabel.text = text
        self.myid = myid


class MainScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.activity_summary(My.db.soma_mes())
    videos = StringProperty('Videos Shown')
    publicacoes = StringProperty('Publications')
    horas = StringProperty('Hours')
    revisitas = StringProperty('Return Visits')
    estudos = StringProperty('Bible Studies')

    def do_registry_activity(self, *args):
        lista = []
        for arg in args:
            lista.append(arg)
        try:
            print(lista)
            My.db.add_to_database(lista)
            self.activity_summary()
            self.clear_fields()
        except (ValueError, NameError):
            self.clear_fields()
            Factory.ErrorPopUp().open()

    def clear_fields(self):
        self.ids.report1.text = ''
        self.ids.report2.text = ''
        self.ids.report3.text = ''
        self.ids.report4.text = ''
        self.ids.report5.text = ''

    def activity_summary(self, valor=None):
        if valor == None:
            valor = My.db.soma_mes()
        print(f" o valor atual e:{valor}")
        soma_publicacoes, soma_videos, total_horas, soma_revisitas, soma_estudos = valor
        self.videos = f"Videos Shown: {soma_videos}"
        self.publicacoes = f"Publications: {soma_publicacoes}"
        self.horas = f"Hours: {total_horas}"
        self.revisitas = f"Return Visits: {soma_revisitas}"
        self.estudos = f"Bible Studies: {soma_estudos}"


class MainMenu(Screen):
    pass


class ListActivity(Screen):
    pass


class TelaListActivity(ScrollView):
    pass


class ErrorPopUp(Popup):
    pass


class My(App):
    db = MyService.MainApp('MyServiceReport.db')

    def build(self):
        return MyServiceReportApp()


My().run()
