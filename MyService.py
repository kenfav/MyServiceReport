import calendar
from datetime import datetime
import sqlite3


class MainApp:
    def __init__(self, banco_de_dados):
        self.banco_de_dados = banco_de_dados
        self.report = {}
        self.year = datetime.now().year
        try:
            self.con = sqlite3.connect(banco_de_dados)
            self.cursor = self.con.cursor()
            self.cursor.execute('''
                                CREATE TABLE IF NOT EXISTS "reports" (
                                        "Id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                        "data"	DATE NOT NULL,
                                        "publicacoes"	SHORT,
                                        "videos"	SHORT,
                                        "horas"	INT NOT NULL,
                                        "revisitas"	SHORT,
                                        "estudos"	SHORT
                                );''')
            self.con.commit()
        except sqlite3.Error:
            print('Error creating DataBase.')
        finally:
            if self.con:
                self.cursor.close()
                self.con.close()

    def last_day_of_month(self, date):
        _, lastday = calendar.monthrange(date.year, date.month)
        return datetime(self.year, date.month, lastday)

    def convert_to_integer(self, value):
        if value.isnumeric():
            return int(value)
        elif value == '':
            return 0
        else:
            return value

    def convert_values_to_database(self, values):
        data, publicacoes, videos, horas, revisitas = values
        if data != '':
            data = datetime.strptime(data, '%d-%m-%y')
        publicacoes = self.convert_to_integer(publicacoes)
        videos = self.convert_to_integer(videos)
        revisitas = self.convert_to_integer(revisitas)
        try:
            horas = horas.lower()
            if horas.islower():
                raise NameError('Incorrect time format')
        except:
            NameError
            raise

        if ':' in horas:
            horas_in_a_list = str(horas).split(":")
            horas = int(horas_in_a_list[0])*60+int(horas_in_a_list[1])
        else:
            if horas.isnumeric():
                if 0 < int(horas) <= 24:
                    horas = int(horas)*60
                else:
                    print("HORAS IS NOT CORRECT")
                    horas = None
                    raise NameError
            else:
                print("horas format is not correct")
                horas = None
                raise NameError
        return (data, publicacoes, videos, horas, revisitas)

    def add_to_database(self, values=None):
        if values:
            values = self.convert_values_to_database(values)
            try:
                self.con = sqlite3.connect(self.banco_de_dados)
                self.cursor = self.con.cursor()
                self.cursor.execute("""
                                    INSERT OR IGNORE INTO reports (data,
                                    publicacoes, videos, horas,
                                    revisitas, estudos)
                                    VALUES (?,?,?,?,?,0)""", (values))
                self.con.commit()
            except sqlite3.Error as error:
                print('Problem when connecting to dadabase.', error)
            finally:
                if self.con:
                    self.cursor.close()
                    self.con.close()

    def remove_from_database(self, id=None):
        if not id:
            raise ValueError('Please insert an Id')
        else:
            try:
                self.con = sqlite3.connect(self.banco_de_dados)
                self.cursor = self.con.cursor()
                print("Connected to SQLite")
                self.cursor.execute("""
                                    DELETE from reports where id = ?""", (id,))
                self.con.commit()
            except sqlite3.Error as error:
                print("Failed to delete multiple records from sqlite table", error)
            finally:
                if self.con:
                    self.cursor.close()
                    self.con.close()

    def dispose(self):
        self.cursor.close()
        self.con.close()

    def pegar_atividade_mensal(self, mes=None):
        try:
            self.con = sqlite3.connect(self.banco_de_dados)
            self.cursor = self.con.cursor()

            if mes == None:
                today = datetime.today()
                mes = today.month
                first_day = datetime(self.year, mes, 1)
                last_day = self.last_day_of_month(first_day)
                self.cursor.execute(
                    "SELECT * FROM reports WHERE data BETWEEN ? AND ?", (first_day, last_day))
                my_activity = self.cursor.fetchall()
                return my_activity
            else:
                first_day = datetime.fromisoformat(
                    str(self.year)+'-'+mes+'-01')
                last_day = self.last_day_of_month(first_day)
                self.cursor.execute(
                    "SELECT * FROM reports WHERE data BETWEEN ? AND ?", (first_day, last_day))
                my_activity = self.cursor.fetchall()
                return my_activity
        except sqlite3.Error as error:
            print('Problem when connecting to the database', error)
        finally:
            if self.con:
                self.cursor.close()
                self.con.close()

    def soma_mes(self, mes=None):
        my_activity = self.pegar_atividade_mensal(mes)
        print(my_activity)
        soma_videos = 0
        soma_publicacoes = 0
        soma_horas = 0
        soma_revisitas = 0
        soma_estudos = 0
        if not my_activity:
            print('There is no activity for this month!')
            return (0, 0, '00:00', 0, 0)
        for _, __, videos, publicacoes, horas, revisitas, estudos in my_activity:
            soma_videos += videos
            soma_publicacoes += publicacoes
            soma_horas += horas
            soma_revisitas += revisitas
            soma_estudos += estudos
            if soma_horas % 60 == 0:
                total_horas = str(soma_horas//60)+':' + \
                    str(soma_horas % 60) + '0'
            else:
                total_horas = str(soma_horas//60)+':' + str(soma_horas % 60)
        return (soma_videos, soma_publicacoes, total_horas, soma_revisitas, soma_estudos)

    def ordenar_lista_criterio(self, lista):
        return lista[1]

    def ordenar_lista_atividade(self, lista=None):
        if not lista:
            lista = self.pegar_atividade_mensal()
            lista.sort(key=self.ordenar_lista_criterio)
            return lista
        else:
            lista.sort(key=self.ordenar_lista_criterio)
            return lista
