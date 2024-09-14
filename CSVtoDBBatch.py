import os
import mysql.connector
import pandas as pd

def main():
    # DB 연결 정보
    db_config = {
        'host': 'localhost',
        'user': 'apt',
        'password': 'apt!1111',
        'database': 'apt'
    }

    directory_path = 'data'

    # CSV 파일 목록 가져오기
    list_of_files = [f for f in os.listdir(directory_path) if f.lower().endswith('.csv')]

    if not list_of_files:
        print("CSV 파일이 존재하지 않습니다.")
        return

    # 테이블 삽입 순서에 맞춘 리스트
    table_insert_order = [
        "Region",
        "Territory",
        "Customer",
        "Supplier",
        "Category",
        "Product",
        "Shipper",
        "OrderStatus",
        "Employee",
        "EmployeeTerritory",
        "MonthlyCategorySales",
        "CategoryOrderCnt_View",
        "Orders",
        "OrderDetail"
    ]

    # 테이블 순서에 맞춰 파일 정렬
    sorted_files = []
    for table_name in table_insert_order:
        for file in list_of_files:
            if file.replace('.csv', '').lower() == table_name.lower():
                sorted_files.append(file)
                break

    # DB 연결 및 트랜잭션 시작
    try:
        connection = mysql.connector.connect(**db_config)
        connection.autocommit = False
        cursor = connection.cursor()

        for file in sorted_files:
            table_name = file.replace('.csv', '')
            process_csv_file(os.path.join(directory_path, file), table_name, cursor)

        connection.commit()
        print("모든 CSV 파일이 데이터베이스에 삽입되었습니다.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        connection.rollback()

    finally:
        cursor.close()
        connection.close()

def process_csv_file(file_path, table_name, cursor):
    df = pd.read_csv(file_path)

    # 테이블 생성
    create_table(cursor, table_name, df.columns)

    # 데이터 삽입
    insert_sql = generate_insert_sql(table_name, df.columns)
    for _, row in df.iterrows():
        data = [None if pd.isna(x) else str(x) for x in row]
        cursor.execute(insert_sql, data)

def create_table(cursor, table_name, column_names):
    create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ("
    create_sql += ', '.join([f"{col} TEXT" for col in column_names])
    create_sql += ");"
    cursor.execute(create_sql)

def generate_insert_sql(table_name, column_names):
    placeholders = ', '.join(['%s'] * len(column_names))
    insert_sql = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({placeholders});"
    return insert_sql

if __name__ == "__main__":
    main()