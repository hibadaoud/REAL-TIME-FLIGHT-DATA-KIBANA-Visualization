import json
import csv

def transform_json_to_csv(input_file, output_csv_file):
    # Define the columns to drop
    columns_to_drop = [
        "percent", "utc", "cs_flight_iata", "cs_flight_number", "cs_airline_iata",
        "arr_estimated_ts", "arr_time_ts", "arr_actual_utc", "arr_estimated_utc",
        "arr_time_utc", "arr_baggage", "arr_gate", "arr_terminal",
        "dep_actual_ts", "dep_estimated_ts", "dep_time_ts", "dep_actual_utc",
        "dep_estimated_utc", "dep_time_utc", "dep_gate", "dep_terminal", "squawk",
        "hex", "reg_number", "flag", "lat", "lng", "alt", "dir", "speed", "v_speed",
        "flight_number", "dep_icao", "dep_iata", "arr_icao", "arr_iata", "airline_icao",
        "airline_iata", "aircraft_icao", "updated", "status", "type"
    ]

    # Define the required columns to keep
    required_columns = [
        "flight_iata", "flight_icao", "dep_name", "dep_city", "dep_country", 
        "arr_name", "arr_city", "arr_country", "airline_name", "delayed", 
        "dep_delayed", "arr_delayed", "arr_time", "arr_estimated", "arr_actual", 
        "dep_time", "dep_estimated", "dep_actual"
    ]

    # Read the input JSON file
    with open(input_file, 'r') as infile:
        data = json.load(infile)

    # Transform the JSON data
    transformed_data = []
    for record in data:
        transformed_record = {key: record[key] for key in required_columns if key in record}
        transformed_data.append(transformed_record)

    # Write the transformed data to the output CSV file
    with open(output_csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=required_columns)
        writer.writeheader()  # Write CSV header
        writer.writerows(transformed_data)  # Write rows

# Usage example
input_file = "fetched_data.json"  # Replace with your input file path
output_csv_file = "transformed_data.csv"  # Replace with your output CSV file path
transform_json_to_csv(input_file, output_csv_file)
