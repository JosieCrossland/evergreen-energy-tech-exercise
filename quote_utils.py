from typing import List


def calculate_heat_loss(
    floor_area: int, heating_factor: int, insulation_factor: float
) -> float:
    return floor_area * heating_factor * insulation_factor


def calculate_power_heat_loss(heat_loss: float, heating_degree_days: int) -> float:
    return round((heat_loss / heating_degree_days), 1)


def select_heat_pump(heat_pump_data: List[dict], required_capacity: float) -> dict:
    highest_capacity_pump = max(heat_pump_data, key=lambda item: item["outputCapacity"])
    sorted_pumps = sorted(heat_pump_data, key=lambda item: item["outputCapacity"])

    if required_capacity > highest_capacity_pump.get("outputCapacity"):
        return {"label": "required capacity exceeds current heat pump range"}

    for heat_pump in sorted_pumps:
        if required_capacity <= heat_pump.get("outputCapacity"):
            return heat_pump


def calculate_total_installation_cost(heat_pump: dict, vat_rate: int) -> float:
    costs = heat_pump.get("costs")
    net_total = 0
    for cost_item in costs:
        for key in cost_item.keys():
            if key == "cost":
                net_total += cost_item.get(key)

    vat = (net_total / 100) * vat_rate

    return round(net_total + vat, 2)
