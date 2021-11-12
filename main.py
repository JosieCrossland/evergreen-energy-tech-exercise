import json
from quote_utils import generate_report

HEAT_PUMP_FILE_NAME = "heat-pumps.json"
HOUSES_FILE_NAME = "houses.json"


def load_data(file_name: str) -> dict:
    with open(file_name) as file:
        data = json.load(file)
    return data


def quote_generation_handler() -> None:
    houses_data = load_data(HOUSES_FILE_NAME)
    heat_pump_data = load_data(HEAT_PUMP_FILE_NAME)
    generate_report(houses_data, heat_pump_data)


if __name__ == "__main__":
    quote_generation_handler()
