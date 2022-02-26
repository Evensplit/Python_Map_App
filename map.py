from ast import For
from asyncore import read
from turtle import fillcolor
import folium
import pandas
data = pandas.read_csv("Volcanoes.csv")
#the variable lat and lon now changes the "LAT" data frame series into a list format rather than a column layout
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])

#function to determine icon color depending on the elevation of the volcano
def color_change(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'
        
    
#html added to pop up text to jazz it up a bit
html = """<h4>Volcano information:</h4> Height: %s m """

map = folium.Map(location = [38.58, -99.09], zoom_start = 6, tiles = "Stamen Terrain")

#create feature groups to give abilty multiple features in one group
#here we created 2 fg (feature groups), one for Volcanoes and one for Population.  This allows
#us to use the layerControl function properly.

fgV = folium.FeatureGroup(name = "Volcanoes") #fvG (feature group volcanoes)
fgP = folium.FeatureGroup(name = 'Population')#fvP (feature group population)

#for loop to add multiple markers to the  map from the data base
#zip function allows loop to iterate through 2 or more lists one at a time
for ln, lt, el in zip(lat,lon, elev):
    iframe = folium.IFrame(html = html % str(el), width = 200, height = 100)
    fgV.add_child(folium.CircleMarker(location = [ln, lt,], radius = 6, popup = folium.Popup(iframe),
    fill = True, fill_color = color_change(el), color = 'blue',fill_opacity = 1))

# we added the child fg, it helps keep code organized and helps later if you want to add control 
# layer(also to switch it on on off) or other features as well
#adding a child object geo json that adds a border around map
fgP.add_child(folium.GeoJson(data = open('world.json', 'r', encoding = 'utf-8-sig').read(), 
style_function = lambda x: {"fillColor" : 'green'if x['properties'] ['POP2005'] < 10000000 else 'blue' 
if x['properties'] ['POP2005'] < 200000000 <= 10000000 else 'red'}))
map.add_child(fgV)  
map.add_child(fgP) 
#adding layer_control() to add and adjust map layer, childadd must be coded after map.add_child(fg) function
map.add_child(folium.LayerControl())
map.save("Map1.html")