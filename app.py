import os
import io
from functools import wraps

from flask import Flask, render_template, request, session, flash, redirect, url_for, send_file
from flask_cors import CORS

from SQLtoCSV import execute_sql_query_to_csv
from charts import get_categories, execute_query_for_chart, get_employee_orders, get_shipper_shipments, \
    get_region_orders, get_city_sales, get_scatter_plot_data, get_product_stock_order_data, \
    get_category_sales_data, get_monthly_sales_data, get_radar_chart_data, get_top_customers_sales_data, \
    get_product_order_quantity_data, get_timeline_data, get_monthly_order_data, \
    get_weekly_order_data, get_sales_stock_heatmap_data, get_seasonal_weekly_sales_data
from database import get_table_data
from execute_query import execute_sql_query
from login import login_page
from map import get_map_data
from sql_analysis import get_sql_analysis
from table_info import get_table_info
from network import get_employee_data
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'aptkey'

# login.py에서 정의된 로그인 관련 라우트를 app에 추가
app.register_blueprint(login_page)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 세션에 'user' 키가 없으면 로그인 페이지로 리다이렉트
        if 'user' not in session:
            flash('로그인이 필요합니다.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
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

        # 쿼리 실행
        result = execute_sql_query(query)

        # CSV 파일 저장 버튼을 눌렀는지 확인
        if 'export_csv' in request.form:
            # 1. 먼저 StringIO로 CSV 데이터를 작성
            csv_output = io.StringIO()
            csv_filename = 'query_results.csv'

            if result['rows']:  # 쿼리 결과가 있을 때만 CSV로 저장
                success = execute_sql_query_to_csv(query, csv_output)
                if success:
                    # 2. StringIO의 데이터를 BytesIO로 변환
                    csv_output.seek(0)
                    byte_output = io.BytesIO(csv_output.getvalue().encode('utf-8'))

                    # 3. 파일을 전송
                    return send_file(
                        byte_output,
                        mimetype='text/csv',
                        download_name=csv_filename,  # attachment_filename 대신 download_name 사용
                        as_attachment=True  # 파일 다운로드 설정
                    )
                else:
                    flash("An error occurred while saving the query results to CSV.", 'danger')
            else:
                flash("No data returned by the query to save to CSV.", 'info')

    return render_template('visualization/query.html', result=result)


@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/activity-log')
def activity_log():

    return render_template('activity_log.html')

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

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('로그아웃 하였습니다.', 'info')
    return redirect(url_for('login'))

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
def radar_chart():
    radar_data = get_radar_chart_data()
    return render_template('visualization/radar_charts.html', radar_data=radar_data)

@app.route('/stacked_bar_charts_detail')
def show_stacked_bar_charts():
    # 데이터 가져오기
    top_customers_sales = get_top_customers_sales_data()
    product_order_quantity = get_product_order_quantity_data()

    # 데이터를 템플릿에 전달
    return render_template('visualization/stacked_bar_charts.html',
                           top_customers_sales=top_customers_sales,
                           product_order_quantity=product_order_quantity)

@app.route('/timeline_detail')
def show_timeline():
    timeline_data = get_timeline_data()
    monthly_data = get_monthly_order_data()
    weekly_data = get_weekly_order_data()
    categories = list(timeline_data['Spring'].keys())  # 카테고리 리스트 생성
    return render_template('visualization/timeline.html', timeline_data=timeline_data, monthly_data=monthly_data, weekly_data=weekly_data, categories=categories)

@app.route('/heatmap_detail')
def show_heatmap():
    # 두 개의 히트맵 데이터를 모두 가져옴
    sales_stock_data = get_sales_stock_heatmap_data()
    seasonal_weekly_sales_data = get_seasonal_weekly_sales_data()

    print("Sales Stock Data:", sales_stock_data)
    print("Seasonal Weekly Sales Data:", seasonal_weekly_sales_data)

    # 두 데이터셋을 템플릿에 전달
    return render_template(
        'visualization/heatmap.html',
        sales_stock_data=sales_stock_data,
        seasonal_weekly_sales_data=seasonal_weekly_sales_data
    )

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

