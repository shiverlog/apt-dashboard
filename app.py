from flask import Flask, render_template, request
from flask_cors import CORS

from charts import get_categories, execute_query_for_chart, get_employee_orders, get_shipper_shipments, \
    get_region_orders, get_city_sales, get_scatter_plot_data, get_product_stock_order_data, \
    get_category_sales_data, get_monthly_sales_data
from database import get_table_data
from execute_query import execute_sql_query
from map import get_map_data
from sql_analysis import get_sql_analysis
from table_info import get_table_info
from network import get_employee_data
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'aptkey'

@app.route('/')
def index():
    # table_info.py의 함수 호출
    table_info = get_table_info()

    # sql_analysis 데이터 호출
    sql_analysis  = get_sql_analysis()

    # index.html 렌더링, 테이블 정보 및 SQL 분석 데이터 전달
    return render_template('index.html', table_info=table_info, sql_analysis=sql_analysis)

@app.route('/jupyter')
def show_jupiter():
    return render_template('visualization/jupyter.html')

@app.route('/execute_query', methods=['GET', 'POST'])
def execute_query():
    result = None
    if request.method == 'POST':
        query = request.form['query']
        result = execute_sql_query(query)

    return render_template('visualization/query.html', result=result)

@app.route('/error/401')
def error_401():
    return render_template('error/401.html')

@app.route('/error/404')
def error_404():
    return render_template('error/404.html')

@app.route('/error/500')
def error_500():
    return render_template('error/500.html')

@app.route('/network')
def show_network():
    employees = get_employee_data()
    return render_template('visualization/network.html', employees=employees)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/password')
def password():
    return render_template('password.html')

@app.route('/message')
def message():
    return render_template('message.html')

@app.route('/area_charts_detail', methods=['GET', 'POST'])
def show_area_charts():
    categories = get_categories()
    selected_category = request.form.get('category', 'all')

    # 선택된 카테고리에 대한 데이터 가져오기
    chart_data = execute_query_for_chart(selected_category)

    return render_template('visualization/area_charts.html', categories=categories, selected_category=selected_category, chart_data=chart_data)

@app.route('/bar_charts_detail')
def show_bar_charts():
    employee_orders = get_employee_orders()
    shipper_shipments = get_shipper_shipments()
    region_orders = get_region_orders()
    city_sales = get_city_sales()

    return render_template(
        'visualization/bar_charts.html',
        employee_orders=employee_orders,
        shipper_shipments=shipper_shipments,
        region_orders=region_orders,
        city_sales=city_sales
    )

@app.route('/line_charts_detail', methods=['GET', 'POST'])
def show_line_charts():
    categories = get_categories()
    selected_category = request.form.get('category', 'all')

    # 선택된 카테고리에 대한 데이터 가져오기
    chart_data = execute_query_for_chart(selected_category)

    return render_template('visualization/line_charts.html', categories=categories, selected_category=selected_category, chart_data=chart_data)


@app.route('/scatter_plot_detail')
def show_scatter_plot():
    # 두 가지 데이터를 모두 가져옴
    scatter_data = get_scatter_plot_data()
    product_stock_order_data = get_product_stock_order_data()

    # 두 데이터를 템플릿에 전달
    return render_template('visualization/scatter_plot.html', scatter_data=scatter_data, product_stock_order_data=product_stock_order_data)

@app.route('/pie_charts_detail')
def show_pie_charts():
    # 카테고리별 총 매출 데이터
    category_sales_data = get_category_sales_data()
    # 월별 카테고리 매출 데이터
    sales_data = get_monthly_sales_data()

    return render_template('visualization/pie_charts.html', sales_data=sales_data, category_sales_data=category_sales_data)

@app.route('/radar_charts_detail')
def show_radar_charts():
    return render_template('visualization/radar_charts.html')

@app.route('/stacked_bar_charts_detail')
def show_stacked_bar_charts():
    return render_template('visualization/stacked_bar_charts.html')

@app.route('/timeline_detail')
def show_timeline():
    return render_template('visualization/timeline.html')

@app.route('/heatmap_detail')
def show_heatmap():
    return render_template('visualization/heatmap.html')

@app.route('/sql_analysis_detail')
def show_sql_analysis():

    sql_analysis = get_sql_analysis()

    return render_template('visualization/sql_analysis.html', sql_analysis=sql_analysis)

@app.route('/maps_detail')
def show_maps():
    map_data = get_map_data()
    return render_template('visualization/maps.html', map_data=map_data)

@app.route('/map_data')
def map_data():
    return get_map_data()

@app.route('/database_detail')
def show_all_tables():
    # 전체 테이블
    admin_data = get_table_data('Admin')
    customer_data = get_table_data('Customer')
    employee_data = get_table_data('Employee')
    product_data = get_table_data('Product')
    category_data = get_table_data('Category')
    region_data = get_table_data('Region')
    shipper_data = get_table_data('Shipper')
    supplier_data = get_table_data('Supplier')
    territory_data = get_table_data('Territory')
    employee_territory_data = get_table_data('EmployeeTerritory')
    order_status_data = get_table_data('OrderStatus')
    orders_data = get_table_data('Orders')
    order_detail_data = get_table_data('OrderDetail')
    monthly_category_sales_data = get_table_data('MonthlyCategorySales')
    category_order_cnt_data = get_table_data('CategoryOrderCnt_View')

    # 모든 데이터를 HTML로 전달
    return render_template(
        'visualization/database.html',
        admin_data=admin_data,
        customer_data=customer_data,
        employee_data=employee_data,
        product_data=product_data,
        category_data=category_data,
        region_data=region_data,
        shipper_data=shipper_data,
        supplier_data=supplier_data,
        territory_data=territory_data,
        employee_territory_data=employee_territory_data,
        order_status_data=order_status_data,
        orders_data=orders_data,
        order_detail_data=order_detail_data,
        monthly_category_sales_data=monthly_category_sales_data,
        category_order_cnt_data=category_order_cnt_data
    )

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

if __name__ == '__main__':
    app.run(port=5000, debug=True)

