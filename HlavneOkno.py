import tkinter as tk
from tkinter import filedialog
import Mapa
import pandas as pd
import Gpx
import Grafy


class HlavneOkno:
   
    def __init__(self):
        #nastavenie hlavneho okna
        self.okno = tk.Tk()
        self.okno.geometry("1000x900+200+100")
        self.okno.configure(bg="lightblue")
       
        
        self.NastavMenu()
        
        
        self.sekcia_mapa = tk.Frame(self.okno)
        self.sekcia_mapa.grid(row=0,column=0, padx= 10, pady=10)
        self.sekcia_mapa.configure(bg="lightblue")
        
        #nastavuje subor s aktivitou na None pre pripad ze uzivatel nevyberie ziaden subor a ukonci program
        self.subor = None
        self.gpx = None

    #metoda ako reakcia na stlacenie tlacidla 'Nahraj aktivitu' v menu
    def VyberSubor(self):
        self.subor = filedialog.askopenfile(title="Vyber GPX subor",filetypes=[("GPX soubory", "*.gpx")])
        
        # Ak bol vybrany nejaky subor, tak ho spracuje
        if self.subor:
            
            self.gpx = Gpx.Gpx(self.subor)
            self.gpx.SpracujSubor()
            
            self.ZobrazMapu()
            self.ZobrazTrasu(self.gpx.GetTrasa())
            self.NastavKomponenty()

            self.grafy = Grafy.Grafy()
            self.ZobrazGrafy()
        
    #metoda ako reakcia na stlacenie tlacidla 'Uloz aktivitu' v menu
    def UlozAktivitu(self):

        #nacita subor s celkovymi statistikami ulozenych aktivit
        dataGlob = pd.read_csv('GlobalStats.csv')

        dataGlob['date'] = pd.to_datetime(dataGlob['date'])
        
        
        #kontroluje ci je vytvoreny objekt gpx, tzn. ci je aktualne nacitana nejaka aktivita 
        # a ci uz nahodou nie je ulozena v subore
        if self.gpx and not dataGlob['date'].isin([self.gpx.GetDatum()]).any():  

            self.gpx.df.to_csv("{}.csv".format(self.gpx.GetDatum().date()), index= False)
           
            velkost = len(dataGlob)

            dataGlob.loc[velkost,'date'] = pd.to_datetime(self.gpx.GetDatum())
            dataGlob.loc[velkost,'Celkova_vzdialenost'] = self.gpx.GetVzdialenost()
            dataGlob.loc[velkost,'Celkovy_cas'] = self.gpx.gpx.get_duration()
            dataGlob.loc[velkost,'Nastupane_metre'] = int(self.gpx.gpx.get_uphill_downhill().uphill)

            dataGlob.to_csv('GlobalStats.csv',index=False)
            

    def ZobrazGlobalStats(self):

        dataGlob = pd.read_csv('GlobalStats.csv')
       
        fontNadpis = ("Helvetica",19, "bold")
        fontHodnota = ("Helvetica",15)
        Farba = "green yellow"

        vedlOkno = tk.Toplevel(bg=Farba)
        vedlOkno.geometry("270x150")
        vedlOkno.title("Celkové štatistiky")

        pocet_nadpis = tk.Label(vedlOkno, text= "Počet aktivít: ", bg= Farba, font=fontNadpis)
        pocet_nadpis.grid(row=0, column=0)
        pocet = tk.Label(vedlOkno, text= len(dataGlob), bg= Farba, font=fontHodnota)
        pocet.grid(row=0, column=1)

        vzdialenost_nadpis = tk.Label(vedlOkno, text= "Vzdialenosť: ", bg= Farba, font=fontNadpis)
        vzdialenost_nadpis.grid(row=1, column=0)
        vzdialenost = tk.Label(vedlOkno, text= ("{}km".format(sum(dataGlob['Celkova_vzdialenost']))), bg= Farba, font=fontHodnota)
        vzdialenost.grid(row=1, column=1)

        trvanie_nadpis = tk.Label(vedlOkno, text= "Trvanie: ", bg= Farba, font=fontNadpis)
        trvanie_nadpis.grid(row=2, column=0)
        trvanie = tk.Label(vedlOkno, text= self.PremenSekundy(sum(dataGlob['Celkovy_cas'])), bg= Farba, font=fontHodnota)
        trvanie.grid(row=2, column=1)
        
        prevysenie_nadpis = tk.Label(vedlOkno, text= "Stúpanie: ", bg= Farba, font=fontNadpis)
        prevysenie_nadpis.grid(row=3, column=0)
        prevysenie = tk.Label(vedlOkno, text= ("{}m".format(sum(dataGlob['Nastupane_metre']))), bg= Farba, font=fontHodnota)
        prevysenie.grid(row=3, column=1)


        

    def NastavMenu(self):
        Hlmenu = tk.Menu(self.okno)
        Hlmenu.add_command(label='Nahraj aktivitu',command=self.VyberSubor)
        Hlmenu.add_command(label='Ulož aktivitu', command =self.UlozAktivitu)
        Hlmenu.add_command(label='Celkové šatistiky', command =self.ZobrazGlobalStats)
        self.okno.config(menu=Hlmenu)
        
    def ZobrazMapu(self):
        self.mapa_instancia = Mapa.Mapa(self.sekcia_mapa)
        

    def ZobrazTrasu(self,paTrasa):
    
        self.mapa_instancia.ZobrazTrasu(paTrasa)

    def PremenSekundy(self,trvanie):
        hodiny = int(trvanie/3600)
        minuty = int((trvanie%3600)/60)
        sekundy = int(trvanie%60)
        return ("{}:{}:{}".format(hodiny,minuty,sekundy))
    

    def NastavKomponenty(self):
        Farba_sekcia_stats = "navajo white"
        fontNadpis = ("Helvetica",19, "bold")
        fontHodnota = ("Helvetica",15)

        
        sekcia_stats = tk.LabelFrame(self.sekcia_mapa, text= "Štatistiky", width= 300, height= 400,bg= Farba_sekcia_stats, font=fontNadpis)
        sekcia_stats.grid(row=0,column=0)
        
        Ddate = self.gpx.GetDatum().date()
        Dhour = self.gpx.GetDatum().hour
        Dminute = self.gpx.GetDatum().minute
        Dsecond = self.gpx.GetDatum().second

        
        datum_nadpis = tk.Label(sekcia_stats, text= "Dátum: ", bg= Farba_sekcia_stats, font=fontNadpis)
        datum_nadpis.grid(row=0, column=0)
        datum = tk.Label(sekcia_stats, text= ("{}".format(Ddate)), bg= Farba_sekcia_stats, font=fontHodnota)
        datum.grid(row=0, column=1)
        
        trvanie_nadpis = tk.Label(sekcia_stats, text= "Trvanie: ", bg= Farba_sekcia_stats, font=fontNadpis)
        trvanie_nadpis.grid(row=1, column=0)
        trvanie = tk.Label(sekcia_stats, text= self.gpx.GetTrvanie(), bg= Farba_sekcia_stats, font=fontHodnota)
        trvanie.grid(row=1, column=1)
        
        prevysenie_nadpis = tk.Label(sekcia_stats, text= "Stúpanie: \nKlesanie: ", bg= Farba_sekcia_stats, font=fontNadpis)
        prevysenie_nadpis.grid(row=2, column=0)
        prevysenie = tk.Label(sekcia_stats, text= ("{}m\n{}m".format(int(self.gpx.GetPrevysenie().uphill),int(self.gpx.GetPrevysenie().downhill))), bg= Farba_sekcia_stats, font=fontHodnota)
        prevysenie.grid(row=2, column=1)

        vzdialenost_nadpis = tk.Label(sekcia_stats, text= "Vzdialenosť: ", bg= Farba_sekcia_stats, font=fontNadpis)
        vzdialenost_nadpis.grid(row=3, column=0)
        vzdialenost = tk.Label(sekcia_stats, text= ("{}km".format(self.gpx.GetVzdialenost())), bg= Farba_sekcia_stats, font=fontHodnota)
        vzdialenost.grid(row=3, column=1)

        max_rychlost_nadpis = tk.Label(sekcia_stats, text= "Max.Rýchlosť: ", bg= Farba_sekcia_stats, font=fontNadpis)
        max_rychlost_nadpis.grid(row=4, column=0)
        max_rychlost = tk.Label(sekcia_stats, text= ("{}km/h".format(self.gpx.GetMaxRychlost())), bg= Farba_sekcia_stats, font=fontHodnota)
        max_rychlost.grid(row=4, column=1)

        priemerny_tep_nadpis = tk.Label(sekcia_stats, text= "Priem.Tep: ", bg= Farba_sekcia_stats, font=fontNadpis)
        priemerny_tep_nadpis.grid(row=5, column=0)
        priemerny_tep = tk.Label(sekcia_stats, text= self.gpx.GetPriemernyTep(), bg= Farba_sekcia_stats, font=fontHodnota)
        priemerny_tep.grid(row=5, column=1)

    def ZobrazGrafy(self):
        sekcia_grafy = tk.Frame(self.okno)
        sekcia_grafy.grid(row=0, column=2, padx=10, pady=10)
        self.okno.grid_rowconfigure(0,weight=3)
        self.okno.grid_columnconfigure(2,weight=2)

        self.grafy.GrafElev(self.gpx.GetElev(),self.gpx.GetDistPoint(),sekcia_grafy)
        self.grafy.GrafRychlost(self.gpx.GetRychlost(),self.gpx.GetDistPoint(),sekcia_grafy)
        self.grafy.GrafTep(self.gpx.GetTep(),self.gpx.GetDistPoint(),sekcia_grafy)
        
    
    def Spusti(self):
        self.okno.mainloop()
    
        
    def GetSubor(self):
        return self.subor
    
    def GetOkno(self):
        return self.okno

