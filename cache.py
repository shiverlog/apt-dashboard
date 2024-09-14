import json
import os
import requests

CACHE_FILE = 'coordinate_cache.json'

# 캐시 불러오기
def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# 캐시 저장하기
def save_cache(cache):
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=4)  # UTF-8로 저장, 이스케이프 방지

coordinate_cache = load_cache()

def get_coordinates_from_openstreetmap(city, country):
    key = f"{city}, {country}"
    if key in coordinate_cache:
        return coordinate_cache[key]  # 캐시에서 반환

    url = f"https://nominatim.openstreetmap.org/search?city={city}&country={country}&format=json"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if len(data) > 0:
                coordinates = {'lat': float(data[0]['lat']), 'lon': float(data[0]['lon'])}
                coordinate_cache[key] = coordinates  # 캐시에 저장
                save_cache(coordinate_cache)  # 캐시를 파일에 저장
                return coordinates
    except requests.exceptions.Timeout:
        print(f"Timeout occurred for {city}, {country}")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")

    return {'lat': 0, 'lon': 0}  # 기본 좌표 반환