from flask import render_template
from sqlalchemy.dialects.mysql import pymysql

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

def get_radar_chart_data():
    query = """
        SELECT
            CASE 
                WHEN MONTH(o.OrderDate) IN (3, 4, 5) THEN 'Spring'
                WHEN MONTH(o.OrderDate) IN (6, 7, 8) THEN 'Summer'
                WHEN MONTH(o.OrderDate) IN (9, 10, 11) THEN 'Fall'
                WHEN MONTH(o.OrderDate) IN (12, 1, 2) THEN 'Winter'
            END AS Season,
            c.CategoryName,
            SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS TotalSales
        FROM OrderDetail od
        JOIN Orders o ON od.OrderId = o.Id
        JOIN Product p ON od.ProductId = p.Id
        JOIN Category c ON p.CategoryId = c.Id
        GROUP BY Season, c.CategoryName
        ORDER BY Season, TotalSales DESC
    """

    connection = get_db_connection()
    with connection.cursor(dictionary=True) as cursor:  # dictionary=True 사용
        cursor.execute(query)
        result = cursor.fetchall()

    # 데이터 가공 (차트에 맞게 계절별로 데이터를 분리)
    season_data = {
        'Spring': {},
        'Summer': {},
        'Fall': {},
        'Winter': {}
    }

    for row in result:
        season = row['Season']
        category = row['CategoryName']
        sales = row['TotalSales']
        season_data[season][category] = sales

    return season_data

# 고매출 상위 10위 고객별 구매 카테고리 데이터
def get_top_customers_sales_data():
    query = """
    SELECT
        c.CompanyName AS CustomerName,
        ca.CategoryName,
        SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS TotalSales
    FROM
        Orders o
    JOIN
        OrderDetail od ON o.Id = od.OrderId
    JOIN
        Product p ON od.ProductId = p.Id
    JOIN
        Category ca ON p.CategoryId = ca.Id
    JOIN
        Customer c ON o.CustomerId = c.Id
    GROUP BY
        c.CompanyName, ca.CategoryName
    ORDER BY
        TotalSales DESC
    LIMIT 10;
    """
    connection = get_db_connection()
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result

# 제품별 누적 주문 수량 데이터
def get_product_order_quantity_data():
    query = """
    SELECT
        p.ProductName,
        SUM(od.Quantity) AS TotalOrderQuantity
    FROM
        OrderDetail od
    JOIN
        Product p ON od.ProductId = p.Id
    GROUP BY
        p.ProductName
    ORDER BY
        TotalOrderQuantity DESC
    LIMIT 10;
    """
    connection = get_db_connection()
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result


def get_timeline_data():
    query = """
        SELECT
            CASE 
                WHEN MONTH(o.OrderDate) IN (3, 4, 5) THEN 'Spring'
                WHEN MONTH(o.OrderDate) IN (6, 7, 8) THEN 'Summer'
                WHEN MONTH(o.OrderDate) IN (9, 10, 11) THEN 'Fall'
                WHEN MONTH(o.OrderDate) IN (12, 1, 2) THEN 'Winter'
            END AS Season,
            c.CategoryName,
            SUM(od.Quantity) AS TotalOrders
        FROM OrderDetail od
        JOIN Orders o ON od.OrderId = o.Id
        JOIN Product p ON od.ProductId = p.Id
        JOIN Category c ON p.CategoryId = c.Id
        GROUP BY Season, c.CategoryName
        ORDER BY Season, c.CategoryName;
    """

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()

    # 모든 카테고리 이름 가져오기
    all_categories = set(row['CategoryName'] for row in result)

    timeline_data = {
        'Spring': {category: 0 for category in all_categories},
        'Summer': {category: 0 for category in all_categories},
        'Fall': {category: 0 for category in all_categories},
        'Winter': {category: 0 for category in all_categories}
    }

    # 결과 데이터를 처리하면서 각 카테고리에 값을 넣어줌
    for row in result:
        season = row['Season']
        category = row['CategoryName']
        total_orders = row['TotalOrders']
        timeline_data[season][category] = total_orders

    cursor.close()
    connection.close()

    return timeline_data


def get_monthly_order_data():
    query = """
        SELECT
            DATE_FORMAT(o.OrderDate, '%Y-%m') AS Month,
            c.CategoryName,
            SUM(od.Quantity) AS TotalOrders
        FROM OrderDetail od
        JOIN Orders o ON od.OrderId = o.Id
        JOIN Product p ON od.ProductId = p.Id
        JOIN Category c ON p.CategoryId = c.Id
        GROUP BY Month, c.CategoryName
        ORDER BY Month, c.CategoryName;
    """

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(query)
    result = cursor.fetchall()

    monthly_data = {}
    for row in result:
        month = row['Month']
        category = row['CategoryName']
        total_orders = row['TotalOrders']
        if month not in monthly_data:
            monthly_data[month] = {}
        monthly_data[month][category] = total_orders

    cursor.close()
    connection.close()

    return monthly_data


def get_weekly_order_data():
    query = """
        SELECT
            WEEK(o.OrderDate) AS Week,
            c.CategoryName,
            SUM(od.Quantity) AS TotalOrders
        FROM OrderDetail od
        JOIN Orders o ON od.OrderId = o.Id
        JOIN Product p ON od.ProductId = p.Id
        JOIN Category c ON p.CategoryId = c.Id
        GROUP BY Week, c.CategoryName
        ORDER BY Week, c.CategoryName;
    """

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(query)
    result = cursor.fetchall()

    weekly_data = {}
    for row in result:
        week = row['Week']
        category = row['CategoryName']
        total_orders = row['TotalOrders']
        if week not in weekly_data:
            weekly_data[week] = {}
        weekly_data[week][category] = total_orders

    cursor.close()
    connection.close()

    return weekly_data


# 1. 카테고리별 매출과 재고 히트맵 데이터 가져오기
def get_sales_stock_heatmap_data():
    query = """
        SELECT 
            c.CategoryName,
            SUM(od.Quantity * od.UnitPrice) AS TotalSales,
            SUM(p.UnitsInStock) AS TotalStock
        FROM 
            OrderDetail od
        JOIN 
            Product p ON od.ProductId = p.Id
        JOIN 
            Category c ON p.CategoryId = c.Id
        GROUP BY 
            c.CategoryName
        ORDER BY 
            TotalSales DESC;
    """

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()

    # Decimal 값을 float으로 변환
    categories = [row['CategoryName'] for row in result]
    sales = [float(row['TotalSales']) for row in result]  # Decimal to float
    stock = [float(row['TotalStock']) for row in result]  # Decimal to float

    heatmap_data = {
        'categories': categories,
        'values': [sales, stock]
    }

    # 변환된 데이터를 확인하기 위한 출력
    print("Processed Heatmap Data (with float):", heatmap_data)
    return heatmap_data


# 2. 계절별 주간 매출, 카테고리별 재고 대비 판매량 히트맵 데이터 가져오기
def get_seasonal_weekly_sales_data():
    query = """
        WITH SeasonalSales AS (
            SELECT 
                CASE 
                    WHEN MONTH(o.OrderDate) IN (3, 4, 5) THEN 'Spring'
                    WHEN MONTH(o.OrderDate) IN (6, 7, 8) THEN 'Summer'
                    WHEN MONTH(o.OrderDate) IN (9, 10, 11) THEN 'Fall'
                    ELSE 'Winter'
                END AS Season,
                c.CategoryName,
                WEEK(o.OrderDate) AS WeekNumber,
                SUM(od.Quantity * od.UnitPrice) AS TotalSales,
                SUM(p.UnitsInStock) AS TotalStock,
                SUM(od.Quantity) AS TotalQuantity
            FROM 
                Orders o
            JOIN 
                OrderDetail od ON o.Id = od.OrderId
            JOIN 
                Product p ON od.ProductId = p.Id
            JOIN 
                Category c ON p.CategoryId = c.Id
            GROUP BY 
                Season, WeekNumber, c.CategoryName
        )
        SELECT 
            Season,
            WeekNumber,
            CategoryName,
            TotalSales,
            TotalStock,
            TotalQuantity,
            (TotalQuantity / NULLIF(TotalStock, 0)) AS SalesToStockRatio
        FROM 
            SeasonalSales
        ORDER BY 
            Season, WeekNumber, CategoryName;
    """

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()

    # 히트맵 데이터 구조로 변환
    seasons = ['Spring', 'Summer', 'Fall', 'Winter']
    weeks = sorted(set([row['WeekNumber'] for row in result]))
    categories = set(row['CategoryName'] for row in result)

    # 히트맵에 표시할 실제 데이터 구성 (히트맵에서 사용할 형태로 변환)
    data_matrix = []
    for category in categories:
        row = []
        for week in weeks:
            value = next((r['TotalSales'] for r in result if r['CategoryName'] == category and r['WeekNumber'] == week), 0)
            row.append(value)
        data_matrix.append(row)

    heatmap_data = {
        'seasons': seasons,
        'weeks': weeks,
        'categories': list(categories),
        'data': data_matrix
    }
    return heatmap_data