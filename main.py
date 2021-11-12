import json
from quote_utils import (
    calculate_heat_loss,
    get_heating_days,
    calculate_power_heat_loss,
    select_heat_pump,
    calculate_total_installation_cost,
    format_cost_breakdown,
)

HEAT_PUMP_FILE_NAME = "heat-pumps.json"
HOUSES_FILE_NAME = "houses.json"
VAT_RATE = 5


def load_data(file_name):
    with open(file_name) as file:
        data = json.load(file)
    return data


def generate_report(houses_data, heat_pump_data):
    for house in houses_data:
        submission_id = house.get("submissionId")
        floor_area = house.get("floorArea")
        heating_factor = house.get("heatingFactor")
        insulation_factor = house.get("insulationFactor")
        design_region = house.get("designRegion")

        heat_loss = calculate_heat_loss(floor_area, heating_factor, insulation_factor)
        heating_days = get_heating_days(design_region)

        if heating_days is None:
            print(
                f"""
    --------------------------------------
    {submission_id}
    --------------------------------------
      Heating Loss = {heat_loss}
      Warning: Could not find design region
    """
            )
            continue

        power_heat_loss = calculate_power_heat_loss(heat_loss, heating_days)
        recommended_pump = select_heat_pump(heat_pump_data, power_heat_loss)
        total_installation_cost = calculate_total_installation_cost(
            recommended_pump, VAT_RATE
        )
        cost_breakdown = format_cost_breakdown(recommended_pump)

        print(
            f"""
    --------------------------------------
    {submission_id}
    --------------------------------------
      Estimated Heat Loss = {heat_loss}
      Design Region = {design_region}
      Power Heat Loss = {power_heat_loss}
      Recommended Heat Pump = {recommended_pump.get("label")}
      Cost Breakdown
        {cost_breakdown}
      Total Cost, including VAT = {total_installation_cost}
    """
        )


def quote_generation_handler():
    houses_data = load_data(HOUSES_FILE_NAME)
    heat_pump_data = load_data(HEAT_PUMP_FILE_NAME)
    generate_report(houses_data, heat_pump_data)


if __name__ == "__main__":
    quote_generation_handler()
