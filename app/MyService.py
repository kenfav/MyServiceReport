from datetime import timedelta, datetime
import sqlite3


class MainApp:
    def __init__(self, banco_de_dados):
        self.report = {}
        self.resposta = ''
        self.year = datetime.now().year
        self.con = sqlite3.connect(banco_de_dados)
        self.cursor = self.con.cursor()
        self.cursor.execute('''
                            SELECT count(name) FROM sqlite_master WHERE type='table' AND name='reports'
                            ''')
        if self.cursor.fetchone()[0] == 1:
            pass
        else:
            self.cursor.execute(
                "CREATE TABLE reports (data DATE, publicacoes SHORT, videos SHORT, horas INT, revisitas SHORT, estudos SHORT);")

    def mainmenu(self):
        print("My Service Report")
        print("="*10)
        print()
        print("MENU:")
        print("Digite o que voce deseja fazer: ")
        print("[1] Ingresar horas")
        print("[2] Ver relatorio mensal")
        self.resposta = input("Digite a sua opcao: ")
        print(f"Voce escolheu a opcao {self.resposta}")
        print("-="*30)
        print()

    def run(self):
        self.mainmenu()
        if self.resposta == "1":
            mes = input("Digite o mes(MM): ")
            dia = input("Digite o dia(DD): ")
            self.report["data"] = datetime.fromisoformat(
                str(f"{self.year}-{mes}-{dia}"))
            self.report["publicacoes"] = int(
                input("Digite a quantidade de publicacioes: "))
            self.report["videos"] = int(
                input("Digite a quantidade de videos: "))
            horas = str(
                input("Digite a quantidade de horas e minutos HH:MM:")).split(":")
            self.report["horas"] = int(horas[0])*60+int(horas[1])
            self.report["revisitas"] = int(
                input("Digite a quantidade de revisitas: "))
            self.report["estudos"] = int(
                input("Digite a quantidade de estudos diferentes durante o mes: "))
            self.add_to_database('reports', self.report['data'], self.report['publicacoes'],
                                 self.report['videos'], self.report['horas'], self.report['revisitas'], self.report['estudos'])
        elif self.resposta == "2":
            self.cursor.execute("SELECT * FROM reports")
            my_activity = self.cursor.fetchall()
            somahoras = 0
            for tupla in my_activity:
                print(
                    f"No dia {tupla[0]} sua atividade foi:\nPublicacoes: {tupla[1]}\nVideos: {tupla[2]}\nHoras: {tupla[3]//60}:{tupla[3]%60}\nRevisitas: {tupla[4]}\n")
                somahoras += int(tupla[3])
                print()
                print("-="*30)
                print()
            print(
                f"O total de horas ate agora e de {somahoras//60}:{somahoras%60}")

    def add_to_database(self, db_table_name, v1, v2, v3, v4, v5, v6):
        self.cursor.execute(
            f"INSERT INTO {db_table_name} VALUES('{v1}','{v2}','{v3}','{v4}','{v5}','{v6}')")
        self.con.commit()
        self.cursor.close()
        self.con.close()


while True:
    start_app = MainApp('MyServiceReport.db')
    start_app.run()
    if start_app.resposta and start_app.resposta != "2" and start_app.resposta != "1":
        break
