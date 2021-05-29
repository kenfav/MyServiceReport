import calendar
from datetime import datetime
import sqlite3


class MainApp:
    def __init__(self, banco_de_dados):
        self.report = {}
        self.year = datetime.now().year
        self.con = sqlite3.connect(banco_de_dados)
        self.cursor = self.con.cursor()
        self.cursor.execute('''
                            SELECT count(name) FROM sqlite_master WHERE type='table' AND name='reports'
                            ''')
        if self.cursor.fetchone()[0] == 1:
            pass
        else:
            self.cursor.execute('''
                                CREATE TABLE "reports" (
                                        "data"	DATE NOT NULL,
                                        "publicacoes"	SHORT,
                                        "videos"	SHORT,
                                        "horas"	INT NOT NULL,
                                        "revisitas"	SHORT,
                                        "estudos"	SHORT
                                );''')

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

    def add_to_database(self,values=None):
        if values:
            values = self.convert_values_to_database(values)
            self.cursor.execute("""
                                INSERT OR IGNORE INTO reports (data,
                                publicacoes, videos, horas,
                                revisitas, estudos)
                                VALUES (?,?,?,?,?,0)""",(values))
        else:
            self.cursor.execute("""
                                INSERT OR IGNORE INTO reports
                                (data, publicacoes, videos,
                                horas, revisitas, estudos)
                                VALUES (:data, :publicacoes,
                                :videos, :horas, :revisitas,
                                :estudos)""")
        self.con.commit()

    def dispose(self):
        self.cursor.close()
        self.con.close()

    def soma_mes(self):
        today = datetime.today()
        mes = today.month
        first_day = datetime(self.year, mes, 1)
        last_day = self.last_day_of_month(first_day)

        self.cursor.execute("SELECT * FROM reports WHERE data BETWEEN ? AND ?", (first_day, last_day))
        my_activity = self.cursor.fetchall()
        print(my_activity)
        soma_videos = 0
        soma_publicacoes = 0
        soma_horas = 0
        soma_revisitas = 0
        soma_estudos = 0
        for _, videos, publicacoes, horas, revisitas, estudos in my_activity:
                soma_videos += videos
                soma_publicacoes += publicacoes
                soma_horas += horas
                soma_revisitas += revisitas
                soma_estudos += estudos
                total_horas = str(soma_horas//60)+':'+ str(soma_horas%60)
        return (soma_videos, soma_publicacoes, total_horas, soma_revisitas, soma_estudos)


