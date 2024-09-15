from db import get_db_connection

def get_employee_data():
    connection = get_db_connection()
    with connection.cursor(dictionary=True) as cursor:
        sql = '''
            SELECT 
                e.Id, 
                CONCAT(e.FirstName, ' ', e.LastName) AS EmployeeName, 
                e.Title, 
                CONCAT(m.FirstName, ' ', m.LastName) AS ManagerName
            FROM Employee e
            LEFT JOIN Employee m ON e.ReportsTo = m.Id;
            '''
        cursor.execute(sql)
        employees = cursor.fetchall()

    connection.close()
    return employees