'''Parses a CSV file and provides functions to retrieve data based on time or field values.'''
import csv
from datetime import datetime, timedelta

PATH = '/Users/ari/Downloads/DATA.CSV - DATA.CSV.csv'

def parse_csv_columns(file_path):
    """
    Parses the CSV file at the given file path and returns a dictionary
    where each key is a column name and each value is a list of column values,
    excluding rows where the "Time" column is "0:00:00".
    """
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        columns = {field: [] for field in reader.fieldnames}
        for row in reader:
            if row["Time"] != "0:00:00":
                for field in reader.fieldnames:
                    columns[field].append(row[field])
        return columns

def refer_to(time):
    """
    Returns the row of data corresponding to the given time as a list of values.
    If the time is not found, returns an error message.
    """
    columns = parse_csv_columns(PATH)
    if time in columns["Time"]:
        index = columns["Time"].index(time)
        return [columns[field][index] for field in columns]
    return "There is no data for that time"

def approx_refer_to(time):
    """
    Finds and returns the row of data closest to the given time.
    If the time format is invalid or no valid times are found, returns an error message.
    """
    columns = parse_csv_columns(PATH)
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
        return refer_to(closest_time)
    return "No valid times found"


def get_time(field, value):
    """
    Returns a list of times where the specified field matches the given value.
    If the field is not found, returns an error message.
    """
    columns = parse_csv_columns(PATH)
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

def get_all_rows():
    """
    Returns all rows from the CSV as a list of lists, where each inner list represents a row.
    """
    columns = parse_csv_columns(PATH)
    num_rows = len(columns["Time"])
    fieldnames = list(columns.keys())
    rows = []
    for i in range(num_rows):
        row = [columns[field][i] for field in fieldnames]
        rows.append(row)
    return rows
