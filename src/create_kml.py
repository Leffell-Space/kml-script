import time
import simplekml
import parse
import os

# Make sure save directory exists
os.makedirs("kml_saves", exist_ok=True)

current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
print("Current time:", current_time)
schema_name = f"Sensor_Data_{current_time.replace('-', '_').replace(' ', '_')}"
file_name = f"kml_saves/save_{current_time}.kml"

def create_kml():
    kml = simplekml.Kml()
    
    # Create schema with name only
    schema = kml.newschema(name=schema_name)
    
    # Get the actual ID that SimpleKML assigned
    schema_url = f"#{schema.name}"  # simplekml uses the name as the ID by default
    print(f"Schema URL: {schema_url}")
    
    # Define field mappings with proper types
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
    
    # Define display names (what appears in Google Earth)
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
    
    # Create SimpleFields
    for i, ((field_name, field_type), display_name) in enumerate(zip(fields, display_names)):
        simple_field = schema.newsimplefield(name=field_name, type=field_type)
        simple_field.displayname = display_name
    
    coords_list = []
    for row in parse.get_all_rows():
        try:
            lat = float(row[1])
            lon = float(row[2])
        except (IndexError, ValueError):
            continue
            
        coords_list.append((lon, lat))
        
        # Create placemark with proper name (time)
        placemark = kml.newpoint(name=row[0], coords=[(lon, lat)])
        
        # Create extended data with proper schema reference
        extended_data = placemark.extendeddata
        sd = extended_data.schemadata()
        sd.schemaurl = schema_url  # Use the schema URL derived from the name
        
        # Add simple data using field names
        for i, (field_name, _) in enumerate(fields):
            if i < len(row): 
                try:
                    # Handle numeric fields properly
                    if i > 0:  # Everything except the time field
                        sd.newsimpledata(field_name, str(row[i]).strip())
                    else:
                        sd.newsimpledata(field_name, row[i])
                except Exception as e:
                    print(f"Error adding data for field {field_name}: {e}")
                    sd.newsimpledata(field_name, str(row[i]))
    
    # Create path line if we have coordinates
    if coords_list:
        line = kml.newlinestring(name="Path")
        line.coords = coords_list
        line.altitudemode = simplekml.AltitudeMode.absolute
        line.extrude = 0
        line.style.linestyle.width = 3
        line.style.linestyle.color = simplekml.Color.red
    
    # Save the KML file
    print(f"Saving KML file to {file_name}")
    kml.save(file_name)
    print(f"KML file saved successfully with schema name: {schema_name}")

create_kml()