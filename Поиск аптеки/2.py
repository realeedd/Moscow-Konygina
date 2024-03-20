import sys

from geocoder import get_coordinates
from mapapi_show import show_map
import requests
import math


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = a
    b_lon, b_lat = b

    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor
    distance = math.sqrt(dx * dx + dy * dy)

    return distance


def find_businesses(ll, spn, request, locale="ru_RU"):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "3c4a592e-c4c0-4949-85d1-97291c87825c"
    search_params = {
        "apikey": api_key,
        "text": request,
        "lang": locale,
        "ll": ll,
        "spn": spn,
        "type": "biz"
    }

    response = requests.get(search_api_server, params=search_params)
    if not response:
        raise RuntimeError(
            f"""Ошибка выполнения запроса:
            {search_api_server}
            Http статус: {response.status_code} ({response.reason})""")

    json_response = response.json()

    organizations = json_response["features"]
    return organizations


def find_business(ll, spn, request, locale="ru_RU"):
    orgs = find_businesses(ll, spn, request, locale=locale)
    if len(orgs):
        return orgs[0]


def main():
    toponym_to_find = ' '.join(sys.argv[1:])

    lat, lon = get_coordinates(toponym_to_find)
    address_ll = f"{lat},{lon}"
    span = "0.005,0.005"

    organization = find_business(address_ll, span, "аптека")
    point = organization["geometry"]["coordinates"]
    org_lat = float(point[0])
    org_lon = float(point[1])
    point_param = f"pt={org_lat},{org_lon},pm2dgl"

    show_map(f"ll={address_ll}&spn={span}", "map", add_params=point_param)

    points_param = point_param + f"~{address_ll},pm2rdl"

    show_map("ll={0}&spn={1}".format(address_ll, span), "map", add_params=points_param)

    show_map(map_type="map", add_params=points_param)

    name = organization["properties"]["CompanyMetaData"]["name"]
    address = organization["properties"]["CompanyMetaData"]["address"]
    time = organization["properties"]["CompanyMetaData"]["Hours"]["text"]
    distance = round(lonlat_distance((lon, lat), (org_lon, org_lat)))

    snippet = f"Название:\t{name}\nАдрес:\t{address}\nВремя работы:\t{time}\n" \
              f"Расстояние:\t{distance}."
    print(snippet)


if __name__ == "__main__":
    main()
