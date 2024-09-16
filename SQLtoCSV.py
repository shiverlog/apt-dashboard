import csv
from db import get_db_connection


def execute_sql_query_to_csv(query, output_stream):
    """
    주어진 SQL 쿼리를 실행하고 그 결과를 CSV 파일로 저장하는 함수.

    Parameters:
    query (str): 실행할 SQL 쿼리
    output_stream (io.BytesIO or file-like object): 결과를 저장할 스트림 또는 파일 객체

    Returns:
    bool: 성공 여부 (True: 성공, False: 실패 또는 데이터 없음)
    """
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

            if rows:
                # 열 이름을 cursor.description에서 가져옴
                columns = [desc[0] for desc in cursor.description]

                # CSV 파일에 결과 저장
                writer = csv.writer(output_stream)

                # 열 이름을 먼저 작성
                writer.writerow(columns)

                # 각 행을 작성
                for row in rows:
                    writer.writerow(row)

                return True  # 성공적으로 저장된 경우 True 반환
            else:
                return False  # 결과가 없을 경우 False 반환
    except Exception as e:
        print(f"An error occurred: {e}")
        return False  # 에러가 발생한 경우 False 반환
    finally:
        connection.close()
