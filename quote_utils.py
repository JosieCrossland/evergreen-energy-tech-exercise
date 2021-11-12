def calculate_heat_loss(floor_area, heating_factor, insulation_factor):
    return floor_area * heating_factor * insulation_factor


def calculate_power_heat_loss(heat_loss, heating_degree_days):
    return round((heat_loss / heating_degree_days), 1)


def select_heat_pump(heat_pump_data, required_capacity):
    highest_capacity_pump = max(heat_pump_data, key=lambda item: item["outputCapacity"])
    sorted_pumps = sorted(heat_pump_data, key=lambda item: item["outputCapacity"])

    if required_capacity > highest_capacity_pump.get("outputCapacity"):
        return {"label": "required capacity exceeds current heat pump range"}

    for heat_pump in sorted_pumps:
        if required_capacity <= heat_pump.get("outputCapacity"):
            return heat_pump
