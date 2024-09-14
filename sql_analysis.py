from db import get_db_connection

def get_sql_analysis():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # 1. 총 주문 수
    cursor.execute("SELECT COUNT(*) AS total_orders FROM Orders;")
    total_orders = cursor.fetchone()['total_orders']

    # 2. 평균 주문 금액
    cursor.execute("""
    SELECT AVG(total_amount) AS avg_order_value
    FROM (
        SELECT SUM(UnitPrice * Quantity * (1 - Discount)) AS total_amount
        FROM OrderDetail
        GROUP BY OrderId
    ) AS order_totals;
    """)
    avg_order_value = cursor.fetchone()
    avg_order_value = round(float(avg_order_value['avg_order_value']), 2) if avg_order_value else 0.00

    # 3. 최고 주문 금액
    cursor.execute("""
    SELECT MAX(total_amount) AS highest_order_value
    FROM (
        SELECT SUM(UnitPrice * Quantity * (1 - Discount)) AS total_amount
        FROM OrderDetail
        GROUP BY OrderId
    ) AS order_totals;
    """)
    highest_order_value = cursor.fetchone()
    highest_order_value = round(float(highest_order_value['highest_order_value']), 2) if highest_order_value else 0.00

    # 4. 최소 주문 금액
    cursor.execute("""
        SELECT MIN(total_amount) AS lowest_order_value
        FROM (
            SELECT SUM(UnitPrice * Quantity * (1 - Discount)) AS total_amount
            FROM OrderDetail
            GROUP BY OrderId
        ) AS order_totals;
        """)
    lowest_order_value = cursor.fetchone()
    lowest_order_value = round(float(lowest_order_value['lowest_order_value']), 2) if lowest_order_value else 0.00

    # 5. 가장 많은 금액을 주문한 고객
    cursor.execute("""
        SELECT C.ContactName AS customer_name, SUM(OD.UnitPrice * OD.Quantity * (1 - OD.Discount)) AS total_amount
        FROM OrderDetail OD
        JOIN Orders O ON OD.OrderId = O.Id
        JOIN Customer C ON O.CustomerId = C.Id
        GROUP BY C.ContactName
        ORDER BY total_amount DESC
        LIMIT 1;
    """)
    highest_order_customer = cursor.fetchone()
    highest_order_customer = {
        'customer_name': highest_order_customer['customer_name'],
        'total_amount': highest_order_customer['total_amount']
    } if highest_order_customer else {'customer_name': 'N/A', 'total_amount': 0.00}

    # 6. 가장 많이 주문한 고객
    cursor.execute("""
        SELECT C.ContactName AS customer_name, COUNT(O.Id) AS order_count
        FROM Orders O
        JOIN Customer C ON O.CustomerId = C.Id
        GROUP BY C.ContactName
        ORDER BY order_count DESC
        LIMIT 1;
    """)
    most_orders_customer = cursor.fetchone()
    most_orders_customer = {
        'customer_name': most_orders_customer['customer_name'],
        'order_count': most_orders_customer['order_count']
    } if most_orders_customer else {'customer_name': 'N/A', 'order_count': 0}

    # 7. 직원 수
    cursor.execute("""SELECT COUNT(*) AS total_employees FROM Employee;""")
    total_employees = cursor.fetchone()['total_employees']

    # 8. 가장 많이 팔린 제품 상위 5개
    cursor.execute("""
        SELECT P.ProductName, SUM(OD.Quantity) AS total_sold
        FROM OrderDetail OD
        JOIN Product P ON OD.ProductId = P.Id
        GROUP BY P.ProductName
        ORDER BY total_sold DESC
        LIMIT 5;
        """)
    top_products = cursor.fetchall()

    # 9. 최고 매출을 기록한 상위 5개 카테고리
    cursor.execute("""
        SELECT C.CategoryName, SUM(OD.UnitPrice * OD.Quantity * (1 - OD.Discount)) AS total_sales
        FROM OrderDetail OD
        JOIN Product P ON OD.ProductId = P.Id
        JOIN Category C ON P.CategoryId = C.Id
        GROUP BY C.CategoryName
        ORDER BY total_sales DESC
        LIMIT 5;
        """)
    top_categories = cursor.fetchall()

    # 10. 주문 금액이 가장 많은 5개 제품
    cursor.execute("""
        SELECT P.ProductName, SUM(OD.UnitPrice * OD.Quantity * (1 - OD.Discount)) AS total_sales
        FROM OrderDetail OD
        JOIN Product P ON OD.ProductId = P.Id
        GROUP BY P.ProductName
        ORDER BY total_sales DESC
        LIMIT 5;
        """)
    top_sales_products = cursor.fetchall()

    # 11. 각 국가별 총 매출
    cursor.execute("""
        SELECT O.ShipCountry, SUM(OD.UnitPrice * OD.Quantity * (1 - OD.Discount)) AS total_sales
        FROM Orders O
        JOIN OrderDetail OD ON O.Id = OD.OrderId
        GROUP BY O.ShipCountry
        ORDER BY total_sales DESC;
    """)
    country_sales = cursor.fetchall()

    for country in country_sales:
        country['total_sales'] = float(country['total_sales'])

    # 12. 연도별 매출
    cursor.execute("""
        SELECT YEAR(O.OrderDate) AS order_year, 
        SUM(OD.UnitPrice * OD.Quantity * (1 - OD.Discount)) AS total_sales,
        COUNT(O.Id) AS order_count
        FROM Orders O
        JOIN OrderDetail OD ON O.Id = OD.OrderId
        GROUP BY order_year
        ORDER BY order_year;
    """)
    yearly_sales = cursor.fetchall()

    # 13. 월별 총 주문
    cursor.execute("""
        SELECT DATE_FORMAT(O.OrderDate, '%Y-%m') AS order_month, 
        MONTHNAME(O.OrderDate) AS month_name, 
        COUNT(O.Id) AS total_orders
        FROM Orders O
        WHERE YEAR(O.OrderDate) = 2021
        GROUP BY DATE_FORMAT(O.OrderDate, '%Y-%m'), MONTHNAME(O.OrderDate)
        ORDER BY order_month;
    """)
    monthly_orders = cursor.fetchall()

    # 14. 지연된 배송 건수
    cursor.execute("""
        SELECT COUNT(*) AS late_shipment_count
        FROM Orders O
        WHERE O.ShippedDate > O.RequiredDate;
    """)
    late_shipment_count = cursor.fetchone()
    late_shipment_count_value = late_shipment_count['late_shipment_count']

    # 15. 배송 중인 주문 건수
    cursor.execute("""
        SELECT COUNT(*) AS in_transit_orders
        FROM Orders O
        WHERE O.ShippedDate IS NULL;
    """)
    in_transit_orders = cursor.fetchone()  # fetchone() 사용
    in_transit_orders_value = in_transit_orders['in_transit_orders'] if in_transit_orders else 0

    connection.close()

    return {
        'total_orders': total_orders,
        'avg_order_value': avg_order_value,
        'highest_order_value': highest_order_value,
        'lowest_order_value': lowest_order_value,
        'highest_order_customer': highest_order_customer,
        'most_orders_customer': most_orders_customer,
        'total_employees': total_employees,
        'top_products': top_products,
        'top_sales_categories': top_categories,
        'top_sales_products': top_sales_products,
        'country_sales': country_sales,
        'yearly_sales': yearly_sales,
        'monthly_orders': monthly_orders,
        'late_shipment_count': late_shipment_count_value,
        'in_transit_orders': in_transit_orders_value,
    }