import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class Grafy:


    def GrafElev(self, data_Elev,data_dist, paOkno):
        y = data_Elev
        #zmena metrov na km
        x = [hodnota/1000 for hodnota in data_dist]
        
        fig = Figure(figsize=(7, 2.5), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(x, y, linestyle='-', color= "green")
        ax.set_xlabel('Vzdialenosť (km)')
        ax.set_ylabel('Nadmorská výška (m)')
        ax.set_title('Nadmorská výška')
        ax.grid(True)

        
        canvas = FigureCanvasTkAgg(fig, master=paOkno)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0,column=0,sticky=tk.W)

        
    def GrafRychlost(self,data_speed,data_dist,paOkno):
        #zmena m/s na km/h
        y = [hodnota*3.6 for hodnota in data_speed]
        x = [hodnota/1000 for hodnota in data_dist]
        
        fig = Figure(figsize=(7, 2.5), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(x, y, color= "blue")
        ax.set_xlabel('Vzdialenosť (km)')
        ax.set_ylabel('Rýchlosť (km/h)')
        ax.set_title('Rýchlosť')
        ax.grid(True)
        
    
        canvas = FigureCanvasTkAgg(fig, master=paOkno)
        canvas.draw()
        canvas.get_tk_widget().grid(row=2,column=0,sticky=tk.W)

    def GrafTep(self,data_tep,data_dist,paOkno):
        y = data_tep
        x = [hodnota/1000 for hodnota in data_dist]
       
        fig = Figure(figsize=(7, 2.5), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(x, y, color= "red")
        ax.set_xlabel('Vzdialenosť (km)')
        ax.set_ylabel('Tep')
        ax.set_title('Srdcový tep')
        ax.grid(True)
        
    
        canvas = FigureCanvasTkAgg(fig, master=paOkno)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1,column=0)
        