from flask import render_template

from db import get_db_connection

# 카테고리 별 월별 매출
# 카테고리 목록을 가져오는 함수
def get_categories():
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            # 카테고리 목록 쿼리
            cursor.execute("SELECT DISTINCT CategoryName FROM MonthlyCategorySales;")
            categories = [row[0] for row in cursor.fetchall()]

    return categories

# SQL 쿼리 실행 후 데이터를 반환하는 함수
def execute_query_for_chart(category):
    with get_db_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            try:
                if category == 'all':
                    # 모든 카테고리의 총 매출 데이터를 가져옴
                    cursor.execute("""
                        SELECT mon AS Month, SUM(total_sales) AS TotalSales
                        FROM MonthlyCategorySales
                        GROUP BY mon
                        ORDER BY mon;
                    """)
                    rows = cursor.fetchall()

                    if rows:
                        labels = [row['Month'] for row in rows]
                        values = [row['TotalSales'] for row in rows]
                        return {'labels': labels, 'values': values}

                elif category == 'outlook':
                    # 전체 카테고리를 한 번에 가져옴
                    cursor.execute("""
                        SELECT mon AS Month, CategoryName, SUM(total_sales) AS TotalSales
                        FROM MonthlyCategorySales
                        GROUP BY mon, CategoryName
                        ORDER BY mon;
                    """)
                    rows = cursor.fetchall()

                    # 카테고리별로 데이터를 정리
                    categories = {}
                    for row in rows:
                        cat = row['CategoryName']
                        if cat not in categories:
                            categories[cat] = {'labels': [], 'values': []}
                        categories[cat]['labels'].append(row['Month'])
                        categories[cat]['values'].append(row['TotalSales'])

                    return categories

                else:
                    # 특정 카테고리의 총 매출 데이터를 가져옴
                    cursor.execute("""
                        SELECT mon AS Month, SUM(total_sales) AS TotalSales
                        FROM MonthlyCategorySales
                        WHERE CategoryName = %s
                        GROUP BY mon
                        ORDER BY mon;
                    """, (category,))

                    rows = cursor.fetchall()

                    if rows:
                        labels = [row['Month'] for row in rows]
                        values = [row['TotalSales'] for row in rows]
                        return {'labels': labels, 'values': values}
            except Exception as e:
                return {'error': str(e)}
    return None

# 직원별 처리한 주문 건수
def get_employee_orders():
    connection = get_db_connection()
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute("""
            SELECT CONCAT(e.FirstName, ' ', e.LastName) AS Employee, COUNT(o.Id) AS OrderCount
            FROM Orders o
            JOIN Employee e ON o.EmployeeId = e.Id
            GROUP BY e.FirstName, e.LastName;
        """)
        rows = cursor.fetchall()
    connection.close()
    return rows

# 배송사별 발송 건수
def get_shipper_shipments():
    connection = get_db_connection()
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute("""
            SELECT s.CompanyName AS Shipper, COUNT(o.Id) AS ShipmentCount
            FROM Orders o
            JOIN Shipper s ON o.ShipVia = s.Id
            GROUP BY s.CompanyName;
        """)
        rows = cursor.fetchall()
    connection.close()
    return rows

# 지역별 주문 수량
def get_region_orders():
    connection = get_db_connection()
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN c.Region IS NULL OR c.Region = '' THEN 'Other' 
                    ELSE c.Region 
                END AS Region, 
                COUNT(o.Id) AS OrderCount
            FROM Orders o
            JOIN Customer c ON o.CustomerId = c.Id
            GROUP BY Region;
        """)
        rows = cursor.fetchall()
    connection.close()
    return rows

# 고객 도시별 매출 비교
def get_city_sales():
    connection = get_db_connection()
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN c.City IS NULL OR c.City = '' THEN 'Other' 
                    ELSE c.City 
                END AS City, 
                SUM(o.Freight) AS TotalSales
            FROM Orders o
            JOIN Customer c ON o.CustomerId = c.Id
            GROUP BY City;
        """)
        rows = cursor.fetchall()
    connection.close()
    return rows

# 카테고리별 평균 주문 수량과 총 판매량을 가져옴
def get_scatter_plot_data():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT c.CategoryName, SUM(od.Quantity * p.UnitPrice) AS TotalSales
        FROM Category c
        JOIN Product p ON c.Id = p.CategoryId
        JOIN OrderDetail od ON p.Id = od.ProductId
        GROUP BY c.CategoryName;
    """)

    rows = cursor.fetchall()
    connection.close()

    # 데이터 포맷 변환
    scatter_data = [(row['CategoryName'], row['TotalSales']) for row in rows]
    return scatter_data


# 제품별 주문량과 재고 상태의 데이터를 가져오는 함수
def get_product_stock_order_data():
    connection = get_db_connection()
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute("""
            SELECT 
                p.ProductName, 
                p.UnitsInStock, 
                SUM(od.Quantity) AS TotalOrderQuantity,
                CASE 
                    WHEN p.UnitsInStock < SUM(od.Quantity) THEN 'Stock Out' 
                    ELSE 'In Stock' 
                END AS StockStatus
            FROM Product p
            JOIN OrderDetail od ON p.Id = od.ProductId
            GROUP BY p.ProductName, p.UnitsInStock;
        """)
        rows = cursor.fetchall()
    connection.close()

    # 필요한 데이터로 변환
    product_stock_order_data = [
        {
            'ProductName': row['ProductName'],
            'UnitsInStock': row['UnitsInStock'],
            'TotalOrderQuantity': row['TotalOrderQuantity'],
            'StockStatus': row['StockStatus']
        }
        for row in rows
    ]
    return product_stock_order_data

# 카테고리별 총 매출을 가져오는 함수
def get_category_sales_data():
    connection = get_db_connection()
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute("""
            SELECT CategoryName, SUM(total_sales) AS TotalSales
            FROM MonthlyCategorySales
            GROUP BY CategoryName;
        """)
        category_sales_data = cursor.fetchall()
    connection.close()

    return list(category_sales_data)


def get_monthly_sales_data():
    query = """
        SELECT 
            a.mon, 
            a.CategoryName,
            a.category_sales, 
            b.total_sales
        FROM 
            (
                SELECT 
                    DATE_FORMAT(OrderDate, "%Y-%m") AS mon, 
                    c.CategoryName,
                    SUM(od.UnitPrice * Quantity - od.UnitPrice * Quantity * Discount) AS category_sales
                FROM 
                    OrderDetail od
                LEFT JOIN Orders o ON od.OrderId = o.Id
                LEFT JOIN Product p ON od.ProductId = p.Id
                LEFT JOIN Category c ON p.CategoryId = c.Id
                GROUP BY mon, c.CategoryName
            ) a
        INNER JOIN 
            (
                SELECT 
                    DATE_FORMAT(OrderDate, "%Y-%m") AS mon, 
                    SUM(od.UnitPrice * Quantity - od.UnitPrice * Quantity * Discount) AS total_sales
                FROM 
                    OrderDetail od
                LEFT JOIN Orders o ON od.OrderId = o.Id
                LEFT JOIN Product p ON od.ProductId = p.Id
                LEFT JOIN Category c ON p.CategoryId = c.Id
                GROUP BY mon
            ) b
        ON a.mon = b.mon;
    """

    with get_db_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            result = cursor.fetchall()

    # 데이터를 월별로 그룹화
    sales_data = {}
    for row in result:
        month = row['mon']
        if month not in sales_data:
            sales_data[month] = []
        sales_data[month].append({
            'category': row['CategoryName'],
            'category_sales': row['category_sales'],
            'total_sales': row['total_sales']
        })

    return sales_data