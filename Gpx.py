import gpxpy
import pandas as pd
class Gpx:

    def __init__(self, paGpxSubor):
        self.gpx = gpxpy.parse(paGpxSubor)

    def SpracujSubor(self):
        latitude = []
        longitude = []
        elevation = []
        distance = []
        speed = []
        heart_rate = []
      
    
    
        for track in self.gpx.tracks:
            for segment in track.segments:
                for i, point in enumerate(segment.points):
                    latitude.append(point.latitude)
                    longitude.append(point.longitude)
                    elevation.append(point.elevation)
                    
                    
                    if point == segment.points[0]:
                        distance.append(0)
                        speed.append(0)
                    else: 
                        distance.append(distance[-1]+point.distance_3d(segment.points[i-1]))

                        speed1 = point.speed_between(segment.points[i-1])
                        if point == segment.points[-1]:
                            speed2 = speed1
                        else:
                            speed2 = point.speed_between(segment.points[i+1])
                        speed.append((speed1+speed2)/2)
                    
                    for extension in point.extensions:
                        
                        for child in list(extension):
                            
                            if 'hr' in child.tag:
                    
                                heart_rate.append(int(child.text))
                                
            
        self.data = {
            'latitude': latitude,
            'longitude': longitude,
            'elevation': elevation,
            'distance': distance,
            'speed': speed,
            'heart_rate': heart_rate
        }
        self.df = pd.DataFrame(self.data, columns=['latitude', 'longitude', 'elevation', 'distance', 'speed', 'heart_rate'])

        
        
    
    def GetTrasa(self):

        trasa = list(zip(self.df['latitude'], self.df['longitude']))
        return trasa
    
    def GetElev(self):
        elev = list(self.df['elevation'])
        return elev
        
    def GetDistPoint(self):
        cumDist = list(self.df['distance'])
        return cumDist

    
    def GetDatum(self):
        return self.gpx.time  

    def GetTrvanie(self):
        trvanie = self.gpx.get_duration()

        hodiny = int(trvanie/3600)
        minuty = int((trvanie%3600)/60)
        sekundy = int(trvanie%60)
        return ("{}:{}:{}".format(hodiny,minuty,sekundy))
    
    def PremenSekundy(self,trvanie):
        hodiny = int(trvanie/3600)
        minuty = int((trvanie%3600)/60)
        sekundy = int(trvanie%60)
        return ("{}:{}:{}".format(hodiny,minuty,sekundy))
    
    def GetPrevysenie(self):
        prevysenie = self.gpx.get_uphill_downhill()
        return prevysenie
    
    def GetVzdialenost(self):
        vzdialenost = self.gpx.length_3d()
        return round(vzdialenost/1000,2)
    
    def GetRychlost(self):
        speed = list(self.df['speed']) 
        return speed
    
    def GetMaxRychlost(self):
        maxRych = sorted(self.df['speed'],reverse=True)
        odstranene = maxRych[int(len(maxRych)*0.001):]
        return round(max(odstranene)*3.6,2)
    
    def GetTep(self):
        tep = list(self.df['heart_rate'])
        return tep
    
    def GetPriemernyTep(self):
        priemer = sum(self.GetTep())/len(self.GetTep())
        return round(priemer,2)
    