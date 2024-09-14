from db import get_db_connection

# 테이블 데이터를 조회하는 함수, 기본적으로 모든 데이터를 가져옴
def get_table_data(table_name, limit=1000):
    connection = get_db_connection()
    cursor = connection.cursor()

    # limit 값이 있으면 제한, 없으면 모든 데이터를 조회
    if limit:
        query = f"SELECT * FROM {table_name} LIMIT {limit}"
    else:
        query = f"SELECT * FROM {table_name}"

    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()
    return rows