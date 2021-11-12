import json

HEAT_PUMP_FILE_NAME = "heat_pumps.json"
HOUSES_FILE_NAME = "houses.json"
VAT_RATE = 5


def load_data(file_name):
    with open(file_name) as file:
        data = json.load(file)
    return data


def quote_generation_handler():
    houses_data = load_data(HOUSES_FILE_NAME)
    heat_pump_data = load_data(HEAT_PUMP_FILE_NAME)


if __name__ == "__main__":
    quote_generation_handler()
