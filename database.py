from db import get_db_connection

# 테이블 데이터를 조회하는 함수, 기본적으로 모든 데이터를 가져옴
def get_table_data(table_name, limit=1000):
    connection = get_db_connection()
    cursor = connection.cursor()

    # 테이블의 컬럼 이름을 동적으로 가져옴
    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
    columns = [column[0] for column in cursor.fetchall()]

    # limit 값이 있으면 제한, 없으면 모든 데이터를 조회
    if limit:
        query = f"SELECT * FROM {table_name} LIMIT {limit}"
    else:
        query = f"SELECT * FROM {table_name}"

    cursor.execute(query)
    rows = cursor.fetchall()

    # 컬럼과 데이터를 딕셔너리 형태로 반환
    result = [dict(zip(columns, row)) for row in rows]

    cursor.close()
    connection.close()
    return result