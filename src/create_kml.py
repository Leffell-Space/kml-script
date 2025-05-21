import time
import simplekml
import parse as parse

current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print("Current time:", current_time)
file_name = ".kml_saves/save_" + current_time.replace(":", "-") + ".kml"  # avoid colons in filename

def create_kml():
    kml = simplekml.Kml()
    
    schema = kml.newschema(name=file_name)
    # schema.id = "YourSchemaID"  # optional, not required unless referencing elsewhere

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

    coords_for_line = []

    for row in parse.get_all_rows():
        if row[0] == "Time":
            continue
        lat = row[1]
        lon = row[2]
        alt = row[3]
        coords_for_line.append((lon, lat, alt))  # KML uses (lon, lat, alt)

        placemark = kml.newpoint(name=row[0], coords=[(lon, lat, alt)])
        placemark.altitudemode = simplekml.AltitudeMode.absolute
        placemark.description = (
            f"Time: {row[0]}<br>Latitude: {row[1]}<br>Longitude: {row[2]}<br>Alt: {row[3]}<br>"
            f"Inside Temp: {row[4]}<br>Outside Temp: {row[5]}<br>Pressure: {row[6]}<br>"
            f"Ozone Concentration: {row[7]}<br>CO2 Quality: {row[8]}<br>Temperature: {row[9]}<br>Humidity: {row[10]}"
        )
        schemadata = placemark.extendeddata.schemadata
        schemadata.schemaurl = "#" + schema.name
        for i, (name, _) in enumerate(fields):
            schemadata.newsimpledata(name=name, value=str(row[i]))

    # Add line connecting all points
    linestring = kml.newlinestring(name="Flight Path")
    linestring.coords = coords_for_line
    linestring.altitudemode = simplekml.AltitudeMode.absolute
    linestring.extrude = 1  # Optional: drop to ground
    linestring.style.linestyle.color = simplekml.Color.red
    linestring.style.linestyle.width = 3

    kml.save(file_name)
    # print(f"Saved KML to: {file_name}")

create_kml()
