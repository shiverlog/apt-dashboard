import mysql.connector

# # MySQL 데이터베이스 연결 설정 (로컬용)
# db_config_local = {
#     'host': 'localhost',
#     'user': 'apt',
#     'password': 'apt!1111',
#     'database': 'apt'
# }

# MySQL 데이터베이스 연결 설정 (Azure용)
db_config_azure = {
    'user': 'apt',
    'password': 'apt!1111',
    'host': 'apt-server.mysql.database.azure.com',
    'port': 3306,
    'database': 'apt-database'
}

# MySQL 데이터베이스 연결 함수 (환경에 맞게 설정 변경)
def get_db_connection(use_azure=True):
    if use_azure:
        connection = mysql.connector.connect(**db_config_azure)
    # else:
    #     connection = mysql.connector.connect(**db_config_local)
    return connection