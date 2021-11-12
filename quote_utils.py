from typing import List, Optional
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

MAX_RETRIES = 3


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


def format_cost_breakdown(heat_pump):
    raw_costs = heat_pump.get("costs")
    breakdown = ""
    for item in raw_costs:
        costs = list(item.values())
        breakdown += ", ".join(map(str, costs))
        breakdown += "\n\t\t"

    return breakdown


def get_heating_days(design_region: str) -> Optional[int]:
    headers = {"x-api-key": "f661f74e-20a7-4e9f-acfc-041cfb846505"}
    url = f"https://063qqrtqth.execute-api.eu-west-2.amazonaws.com/v1/weather?location={design_region}"

    retry_strategy = Retry(
        total=MAX_RETRIES,
        status_forcelist=[418, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)

    try:
        response = http.get(url, headers=headers)
        if response.status_code == requests.codes.ok:
            data = response.json()
            heating_days = data.get("location").get("degreeDays")
            return int(heating_days)
        elif response.status_code == requests.codes.not_found:
            return None
        else:
            response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e.response.text)
