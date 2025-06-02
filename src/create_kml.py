'''
This script generates a KML file from sensor data, 
including placemarks for each data point and a path line connecting them.
'''
import time
import os
from xml.sax import saxutils
import parse

# Make sure save directory exists
os.makedirs("kml_saves", exist_ok=True)

current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
print("Current time:", current_time)
SCHEMA_NAME = f"Sensor_Data_{current_time.replace(' ', '_').replace(' ', '_')}"
FILE_NAME = f"kml_saves/save_{current_time}.kml"

fields = [
    ("Name", "string"),
    ("Latitude", "double"),
    ("Longitude", "double"),
    ("Altitude", "double"),
    ("Inside_Temp", "double"),
    ("Outside_Temp", "double"),
    ("Pressure", "double"),
    ("Ozone_Concentration", "double"),
    ("CO2_Quality", "double"),
    ("Temperature", "double"),
    ("Humidity", "double"),
]

display_names = [
    "Time",
    "Latitude", 
    "Longitude",
    "Altitude",
    "Inside Temp",
    "Outside Temp",
    "Pressure",
    "Ozone Concentration",
    "CO2 Quality",
    "Temperature",
    "Humidity",
]

def escape(s):
    return saxutils.escape(str(s))

def create_kml():
    coords_list = []
    placemarks = []

    for row in parse.get_all_rows():
        try:
            lat = float(row[1])
            lon = float(row[2])
        except (IndexError, ValueError):
            continue
        coords_list.append((lon, lat))
        # ExtendedData for this placemark
        extended_data = ""
        for i, (field, _) in enumerate(fields):
            if i < len(row):
                extended_data += f'<SimpleData name="{escape(field)}">{escape(row[i])}</SimpleData>\n' #pylint: disable=line-too-long
        placemark = f"""
        <Placemark>
            <name>{escape(row[0])}</name>
            <ExtendedData>
                <SchemaData schemaUrl="#{SCHEMA_NAME}">
                    {extended_data}
                </SchemaData>
            </ExtendedData>
            <Point>
                <altitudeMode>absolute</altitudeMode>
                <coordinates>{lon},{lat},{escape(row[3])}</coordinates>
            </Point>
        </Placemark>
        """
        placemarks.append(placemark)

    # Path line
    linestring = ""
    if coords_list:
        # Use actual altitude for each point in the path
        rows = list(parse.get_all_rows())
        coords_str = " ".join([
            f"{float(row[2])},{float(row[1])},{escape(row[3])}"
            for row in rows[1:]  # Skip header row
            if len(row) > 3
        ])
        linestring = f"""
        <Placemark>
            <name>Path</name>
            <Style>
                <LineStyle>
                    <color>ff0000ff</color>
                    <width>3</width>
                </LineStyle>
            </Style>
            <LineString>
                <extrude>0</extrude>
                <altitudeMode>absolute</altitudeMode>
                <coordinates>
                    {coords_str}
                </coordinates>
            </LineString>
        </Placemark>
        """

    # Schema definition
    schema_fields = ""
    for (field, typ), display in zip(fields, display_names):
        schema_fields += f'<SimpleField name="{escape(field)}" type="{typ}"><displayName>{escape(display)}</displayName></SimpleField>\n' #pylint: disable=line-too-long

    schema = f"""
    <Schema name="{SCHEMA_NAME}" id="{SCHEMA_NAME}">
        {schema_fields}
    </Schema>
    """

    # KML document
    kml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
    <name>{escape(SCHEMA_NAME)}</name>
    {schema}
    {''.join(placemarks)}
    {linestring}
</Document>
</kml>
"""

    print(f"Saving KML file to {FILE_NAME}")
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        f.write(kml_content)
    print(f"KML file saved successfully with schema name: {SCHEMA_NAME}")
