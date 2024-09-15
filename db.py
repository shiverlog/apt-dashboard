import mysql.connector

# MySQL 데이터베이스 연결 설정
db_config = {
    'user': 'snvtumbceb',
    'password': 'aptda!1111',  # 실제 비밀번호로 변경
    'host': 'apt-server.mysql.database.azure.com',
    'port': 3306,
    'database': 'apt-database',  # 실제 데이터베이스 이름으로 변경
    'ssl_ca': '/path/to/ca-cert.pem',  # SSL 인증서의 경로로 변경
    'ssl_disabled': False
}

# MySQL 데이터베이스 연결 함수
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection