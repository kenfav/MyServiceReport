from datetime import timedelta
import sqlite3

class MainApp:
    def __init__(self):
        self.report = {}
        self.resposta = ''
        self.con = sqlite3.connect('MyServiceReport.db')
        self.cursor = self.con.cursor()
        self.cursor.execute('''
                            SELECT count(name) FROM sqlite_master WHERE type='table' AND name='reports'
                            ''')
        if self.cursor.fetchone()[0]==1:
            pass
        else:
            self.cursor.execute("CREATE TABLE reports (data DATE, publicacoes SHORT, videos SHORT, horas INT, revisitas SHORT, estudos SHORT);")

    def mainmenu(self):
        print("My Service Report")
        print("="*10)
        print()
        print("MENU:")
        print("Digite o que voce deseja fazer: ")
        print("[1] Ingresar horas")
        print("[2] Ver relatorio mensal")
        self.resposta = input("Digite a sua opcao: ")

    def run(self):
        while True:
            self.mainmenu()
            if self.resposta=="1":
                self.report["mes"] = input("Digite o mes(MM): ")
                self.report["dia"] = input("Digite o dia(DD): ")
                self.report["publicaciones"] =  int(input("Digite a quantidade de publicacioes: "))
                self.report["videos"] = int(input("Digite a quantidade de videos: "))
                horas = input("Digite a quantidade de horas e minutos HH:MM:")
                self.report["horas"] = timedelta(hours=int(horas[:1]), minutes=int(horas[2:]))
                self.report["revisitas"] = int(input("Digite a quantidade de revisitas: "))
                self.report["estudos"] = int(input("Digite a quantidade de estudos diferentes durante o mes: "))
                self.add_to_database()
            elif self.resposta=="2":
                print(self.cursor.execute("SELECT * FROM reports").fetchall())
            else:
                print("FINALIZADO")
                break
    def add_to_database(self, db_table_name='reports', v1=self.report['data'], v2=self.report['publicacoes'], v3=self.report['videos'], v4=self.report['horas'], v5=self.report['revisitas'], v6=self.report['estudos']):
       self.cursor.execute(f"INSERT INTO reports VALUES('{v1}','{v2}','{v3}','{v4}','{v5}','{v6}')")

MainApp().run()

