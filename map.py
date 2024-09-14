from db import get_db_connection
from cache import get_coordinates_from_openstreetmap

# 도시 및 국가별 주문 데이터를 가져오는 함수
def get_map_data():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT ShipCountry, ShipCity, COUNT(*) AS order_count
        FROM Orders
        GROUP BY ShipCountry, ShipCity
        ORDER BY ShipCountry, ShipCity, order_count DESC;;
    """)
    map_data = cursor.fetchall()

    # 각 도시와 국가에 대한 좌표 추가
    for row in map_data:
        coordinates = get_coordinates_from_openstreetmap(row['ShipCity'], row['ShipCountry'])
        row['lat'] = coordinates['lat']
        row['lon'] = coordinates['lon']

    connection.close()

    return map_data