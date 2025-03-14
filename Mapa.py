import tkintermapview as tkmap



class Mapa:
    def __init__(self,sekcia):
        self.mapa = tkmap.TkinterMapView(sekcia, width=750, height=600)
        self.mapa.grid(row=1, column= 0)
        
         
        self.mapa.set_tile_server("https://tile.freemap.sk/C/{z}/{x}/{y}.jpeg")

        self.mapa.set_zoom(12)
        self.mapa.set_position(48.646913850679994,17.876049019396305)

        
        
    def ZobrazTrasu(self,paTrasa):
       
        self.mapa.set_position(paTrasa[len(paTrasa)//3][0], paTrasa[len(paTrasa)//3][1])
        self.mapa.set_marker(paTrasa[0][0],paTrasa[0][1])
        self.mapa.set_marker(paTrasa[-1][0],paTrasa[-1][1])
        
        polygon = self.mapa.set_polygon(paTrasa,
                                outline_color="cyan",
                                fill_color= None,
                                border_width=4,
                               )

        
        

    def GetMapa(self):
        return self.mapa

   
    

 
    

