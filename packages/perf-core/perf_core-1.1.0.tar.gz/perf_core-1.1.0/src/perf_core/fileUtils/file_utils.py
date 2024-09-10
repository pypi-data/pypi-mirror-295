import json


def write_output_to_file(out_data, filename="data_output.json"):
    with open(filename, "w") as json_file:
        json.dump(out_data, json_file)
