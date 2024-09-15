from db import get_db_connection

def execute_sql_query(query):
    connection = get_db_connection()
    result = None

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows:
                # cursor.description을 사용하여 열 이름을 가져옴
                columns = [desc[0] for desc in cursor.description]
                result = {'columns': columns, 'rows': [list(row) for row in rows]}  # 튜플 데이터를 리스트로 변환
            else:
                result = {'columns': [], 'rows': []}  # 빈 결과 처리
    except Exception as e:
        result = {'columns': [], 'rows': [[str(e)]]}
    finally:
        connection.close()

    return result
