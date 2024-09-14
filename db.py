import mysql.connector

# MySQL 데이터베이스 연결 설정
db_config = {
    'host': 'localhost',
    'user': 'apt',
    'password': 'apt!1111',
    'database': 'apt'
}

# MySQL 데이터베이스 연결 함수
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection