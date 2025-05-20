import csv
from datetime import datetime, timedelta

def parse_csv_columns(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        columns = {field: [] for field in reader.fieldnames}
        for row in reader:
            if row["Time"] != "0:00:00":
                for field in reader.fieldnames:
                    columns[field].append(row[field])
        return columns

def referTo(time):
    columns = parse_csv_columns('/Users/ari/Downloads/DATA.CSV - DATA.CSV.csv')
    if time in columns["Time"]:
        index = columns["Time"].index(time)
        return [columns[field][index] for field in columns]
    else:
        return "There is no data for that time"
    
def approxReferTo(time):
    columns = parse_csv_columns('/Users/ari/Downloads/DATA.CSV - DATA.CSV.csv')
    time_format = "%H:%M:%S"
    try:
        target_time = datetime.strptime(time, time_format)
    except ValueError:
        return "Invalid time format"
    min_diff = timedelta.max
    closest_time = None
    for t in columns["Time"]:
        try:
            current_time = datetime.strptime(t, time_format)
            diff = abs(current_time - target_time)
            if diff < min_diff:
                min_diff = diff
                closest_time = t
        except ValueError:
            continue
    if closest_time:
        return referTo(closest_time)
    else:
        return "No valid times found"


def getTime(field, value):
    columns = parse_csv_columns('/Users/ari/Downloads/DATA.CSV - DATA.CSV.csv')
    if field not in columns:
        return f"Field '{field}' not found"
    times = []
    for i, v in enumerate(columns[field]):
        try:
            if float(v) == float(value):
                times.append(columns["Time"][i])
        except ValueError:
            continue
    return times
