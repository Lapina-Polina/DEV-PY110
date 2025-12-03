import requests
from pprint import pprint

# Словарь перевода значений направления ветра
DIRECTION_TRANSFORM = {
    "n": "северное",
    "nne": "северо-северо-восточное",
    "ne": "северо-восточное",
    "ene": "восточно-северо-восточное",
    "e": "восточное",
    "ese": "восточно-юго-восточное",
    "se": "юго-восточное",
    "sse": "юго-юго-восточное",
    "s": "южное",
    "ssw": "юго-юго-западное",
    "sw": "юго-западное",
    "wsw": "западно-юго-западное",
    "w": "западное",
    "wnw": "западно-северо-западное",
    "nw": "северо-западное",
    "nnw": "северо-северо-западное",
    "c": "штиль",
}


def current_weather(lat: float, lon: float) -> dict:
    token = "c558442f4f364d7a8d9125451250212"
    url = f"https://api.weatherapi.com/v1/current.json?key={token}&q={lat},{lon}"

    response = requests.get(url)
    data = response.json()
    current = data["current"]

    result = {
        "city": data["location"]["name"],
        "time": current["last_updated"].split(" ")[1],  # Берём только часы и минуты
        "temp": current["temp_c"],
        "feels_like_temp": current["feelslike_c"],
        "pressure": round(current["pressure_mb"] * 0.75, 1),  # мбар → мм рт. ст.
        "humidity": current["humidity"],
        "wind_speed": round(current["wind_kph"] / 3.6, 1),  # км/ч → м/с
        "wind_gust": round(current["gust_kph"] / 3.6, 1),  # км/ч → м/с
        "wind_dir": DIRECTION_TRANSFORM.get(
            current["wind_dir"].lower(), current["wind_dir"]
        ),
    }

    return result


if __name__ == "__main__":
    pprint(current_weather(59.93, 30.31))  # Проверка работы для Санкт-Петербурга
