from db import get_db_connection

def get_table_info():
    connection = get_db_connection()
    cursor = connection.cursor()

    # 테이블 목록 가져오기
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    table_info_list = []

    for table in tables:
        table_name = table[0]

        # 컬럼 이름 가져오기
        cursor.execute(f"SHOW COLUMNS FROM {table_name}")
        columns = [column[0] for column in cursor.fetchall()]

        # 데이터 개수 가져오기
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        data_count = cursor.fetchone()[0]

        # 테이블 정보 추가
        table_info_list.append({
            "table_name": table_name,
            "columns": columns,
            "data_count": data_count
        })

    cursor.close()
    connection.close()

    return table_info_list