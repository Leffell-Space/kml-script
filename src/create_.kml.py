import os.path as isfile
import time
import simplekml
import src.parse as parse

current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print("Current time:", current_time)
file_name = ".kml_saves/save_" + current_time + ".kml"

def create_kml():
    kml = simplekml.Kml()
    
    schema = kml.newschema(name=file_name)
    #schema.id

    fields = [
    ("Time", "string"),
    ("Latitude", "float"),
    ("Longitude", "float"),
    ("Alt", "string"),
    ("Inside Temp", "string"),
    ("Outside Temp", "string"),
    ("Pressure", "string"),
    ("Ozone Concentration", "string"),
    ("CO2 Quality", "string"),
    ("Temperature", "string"),
    ("Humidity", "string"),
]
    for name, typ in fields:
        schema.newsimplefield(name=name, type=typ)

    for row in parse.get_all_rows():
        placemark = kml.newpoint(name=row[0], coords=[(row[2], row[1])])
        placemark.description = f"Time: {row[0]}<br>Latitude: {row[1]}<br>Longitude: {row[2]}<br>Alt: {row[3]}<br>Inside Temp: {row[4]}<br>Outside Temp: {row[5]}<br>Pressure: {row[6]}<br>Ozone Concentration: {row[7]}<br>CO2 Quality: {row[8]}<br>Temperature: {row[9]}<br>Humidity: {row[10]}"
        for i, (name, _) in enumerate(fields):
            placemark.extendeddata.schemadata.newsimpledata(name=name, value=str(row[i]))


    kml.save(file_name)

create_kml()