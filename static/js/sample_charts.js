// TAble
window.addEventListener('DOMContentLoaded', event => {
    // Simple-DataTables
    // https://github.com/fiduswriter/Simple-DataTables/wiki

    const datatablesSimple = document.getElementById('datatablesSimple');
    if (datatablesSimple) {
        new simpleDatatables.DataTable(datatablesSimple);
    }
});

// Area Chart (Chart.js)
var ctxArea = document.getElementById("myAreaChart").getContext("2d");
new Chart(ctxArea, {
    type: 'line',
    data: {
        labels: [
            "2018-02", "2018-03", "2018-04", "2018-05", "2018-06", "2018-07", "2018-08", "2018-09", "2018-10", "2018-11", "2018-12",
            "2019-01", "2019-02", "2019-03", "2019-04", "2019-05", "2019-06", "2019-07", "2019-08", "2019-09", "2019-10", "2019-11", "2019-12",
            "2020-01", "2020-02", "2020-03", "2020-04", "2020-05", "2020-06", "2020-07", "2020-08", "2020-09", "2020-10", "2020-11", "2020-12",
            "2021-01", "2021-02", "2021-03", "2021-04", "2021-05", "2021-06", "2021-07", "2021-08", "2021-09"
        ],
        datasets: [{
            label: "Monthly Sales",
            data: [
                8899663.05, 9484312.05, 10169919.00, 10619512.40, 11306837.60, 10842416.00, 10236589.35, 10469387.55, 10350025.80, 9859385.15, 12121546.90,
                10803171.25, 11277316.00, 10225254.60, 9414072.55, 9927234.65, 10793826.10, 10823247.30, 11503328.20, 10408195.30, 10784412.60, 11086825.60, 11630097.27,
                10158699.00, 10068894.00, 11061652.00, 11732330.00, 11477355.00, 9644318.00, 9743043.00, 11604880.00, 9335533.00, 9421726.00, 11211007.00, 9850324.00,
                10740870.00, 9230261.00, 11387107.00, 10014143.00, 9862251.00, 10786727.00, 12399161.00, 10413555.00, 5566290.00
            ],
            fill: true,
            backgroundColor: "rgba(75,192,192,0.4)",
            borderColor: "rgba(75,192,192,1)"
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                labels: {
                    font: {
                        family: 'Arial'  // 폰트 설정
                    }
                }
            }
        },
        scales: {
            y: {
                beginAtZero: false  // Y축 시작을 0으로 설정하지 않음
            }
        }
    }
});


// Bar Chart (Chart.js)
var ctxBar = document.getElementById("myBarChart").getContext("2d");
new Chart(ctxBar, {
    type: 'bar',
    data: {
        labels: ["Janet Leverling", "Nancy Davolio", "Margaret Peacock", "Steven Buchanan", "Michael Suyama", "Laura Callahan", "Robert King", "Anne Dodsworth", "Andrew Fuller"],  // 직원 이름
        datasets: [{
            label: 'Processed Orders',
            data: [1964, 1918, 1907, 1859, 1849, 1842, 1839, 1835, 1805],  // 처리 주문 수
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',  // Janet Leverling
                'rgba(54, 162, 235, 0.2)',  // Nancy Davolio
                'rgba(255, 206, 86, 0.2)',  // Margaret Peacock
                'rgba(75, 192, 192, 0.2)',  // Steven Buchanan
                'rgba(153, 102, 255, 0.2)', // Michael Suyama
                'rgba(255, 159, 64, 0.2)',  // Laura Callahan
                'rgba(199, 199, 199, 0.2)', // Robert King
                'rgba(255, 205, 86, 0.2)',  // Anne Dodsworth
                'rgba(75, 192, 192, 0.2)'   // Andrew Fuller
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)',
                'rgba(199, 199, 199, 1)',
                'rgba(255, 205, 86, 1)',
                'rgba(75, 192, 192, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                labels: {
                    font: {
                        family: 'Arial'  // 폰트 설정
                    }
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,  // y축이 0부터 시작하도록 설정
                ticks: {
                    precision: 0  // y축 값이 정수로 표시되도록 설정
                }
            }
        }
    }
});


// Pie Chart (Chart.js)
var ctxPie = document.getElementById("myPieChart").getContext("2d");
new Chart(ctxPie, {
    type: 'pie',
    data: {
        labels: ["Confections", "Beverages", "Condiments", "Seafood", "Dairy Products", "Grains/Cereals", "Meat/Poultry", "Produce"],
        datasets: [{
            label: 'Category Sales',
            data: [104976, 97048, 96814, 96777, 80753, 56465, 48545, 40505],
            backgroundColor: [
                'rgba(255, 99, 132, 0.8)',  // Confections
                'rgba(54, 162, 235, 0.8)',  // Beverages
                'rgba(255, 206, 86, 0.8)',  // Condiments
                'rgba(75, 192, 192, 0.8)',  // Seafood
                'rgba(153, 102, 255, 0.8)', // Dairy Products
                'rgba(255, 159, 64, 0.8)',  // Grains/Cereals
                'rgba(199, 199, 199, 0.8)', // Meat/Poultry
                'rgba(255, 205, 86, 0.8)'   // Produce
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)',
                'rgba(199, 199, 199, 1)',
                'rgba(255, 205, 86, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        plugins: {
            tooltip: {
                callbacks: {
                    label: function(tooltipItem) {
                        return tooltipItem.label + ': ' + tooltipItem.raw + ' USD';
                    }
                }
            },
            legend: {
                position: 'right',
                labels: {
                    font: {
                        family: 'Arial'
                    }
                }
            }
        }
    }
});

// Line Chart (Chart.js)
var ctxLine = document.getElementById("myLineChart").getContext("2d");
new Chart(ctxLine, {
    type: 'line',
    data: {
        labels: [
            "2018-02", "2018-03", "2018-04", "2018-05", "2018-06", "2018-07", "2018-08",
            "2018-09", "2018-10", "2018-11", "2018-12", "2019-01", "2019-02", "2019-03",
            "2019-04", "2019-05", "2019-06", "2019-07", "2019-08", "2019-09", "2019-10",
            "2019-11", "2019-12", "2020-01", "2020-02", "2020-03", "2020-04", "2020-05",
            "2020-06", "2020-07", "2020-08", "2020-09", "2020-10", "2020-11", "2020-12",
            "2021-01", "2021-02", "2021-03", "2021-04", "2021-05", "2021-06", "2021-07",
            "2021-08", "2021-09"
        ],
        datasets: [{
            label: 'Beverages Monthly Sales',
            data: [
                1751932.50, 1968441.75, 2116172.00, 2087987.00, 2305829.00, 2142627.75,
                2128061.60, 2146246.55, 2087402.55, 2142307.20, 2502346.30, 2212680.50,
                2289295.35, 2086995.60, 1913017.20, 2058319.90, 2149540.00, 2184472.95,
                2333819.65, 1995867.90, 2213906.60, 2115729.55, 2364219.70, 2139186.00,
                2095944.00, 2261632.00, 2393645.00, 2350344.00, 2068606.00, 1972197.00,
                2356532.00, 2011750.00, 1835707.00, 2257889.00, 1995711.00, 2254715.00,
                1886889.00, 2318976.00, 2145539.00, 2072883.00, 2266783.00, 2607610.00,
                2209879.00, 1072199.00
            ],
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                labels: {
                    font: {
                        family: 'Arial'  // 폰트 설정
                    }
                }
            }
        }
    }
});


// Scatter Plot (Chart.js)
var ctxScatter = document.getElementById("myScatterChart").getContext("2d");
new Chart(ctxScatter, {
    type: 'scatter',
    data: {
        datasets: [{
            label: 'Category Sales',
            data: [
                {x: 'Beverages', y: 93890506.00},
                {x: 'Confections', y: 67475750.00},
                {x: 'Meat/Poultry', y: 66914793.00},
                {x: 'Dairy Products', y: 59690859.00},
                {x: 'Condiments', y: 57047074.00},
                {x: 'Seafood', y: 51251548.00},
                {x: 'Produce', y: 33434598.00},
                {x: 'Grains/Cereals', y: 29130381.00}
            ],
            backgroundColor: 'rgba(75, 192, 192, 0.4)',
            borderColor: 'rgba(75, 192, 192, 1)',
            pointRadius: 10
        }]
    },
    options: {
        scales: {
            x: {
                type: 'category',
                title: {
                    display: true,
                    text: 'Category'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Sales'
                }
            }
        },
        responsive: true,
        plugins: {
            legend: {
                labels: {
                    font: {
                        family: 'Arial'  // 폰트 설정
                    }
                }
            }
        }
    }
});


// Radar Chart (Chart.js)
var ctxRadar = document.getElementById("myRadarChart").getContext("2d");
new Chart(ctxRadar, {
    type: 'radar',
    data: {
        labels: ["Beverages", "Confections", "Meat/Poultry", "Dairy Products", "Condiments", "Seafood", "Produce", "Grains/Cereals"],
        datasets: [
            {
                label: 'Fall',
                data: [19884301.00, 14684009.00, 14341400.00, 12825744.00, 12272444.00, 11049636.00, 7210750.00, 6252341.00],
                fill: true,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                pointBackgroundColor: 'rgba(255, 99, 132, 1)',
            },
            {
                label: 'Winter',
                data: [21494529.00, 15371358.00, 15388812.00, 13528483.00, 13065390.00, 11652800.00, 7594383.00, 6699240.00],
                fill: true,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                pointBackgroundColor: 'rgba(54, 162, 235, 1)',
            },
            {
                label: 'Spring',
                data: [25776219.00, 18284274.00, 18283963.00, 16316219.00, 15620194.00, 14071402.00, 9049128.00, 7990188.00],
                fill: true,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                pointBackgroundColor: 'rgba(75, 192, 192, 1)',
            },
            {
                label: 'Summer',
                data: [26735457.00, 19136109.00, 18900618.00, 17020413.00, 16089046.00, 14477710.00, 9580337.00, 8188612.00],
                fill: true,
                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                borderColor: 'rgba(153, 102, 255, 1)',
                pointBackgroundColor: 'rgba(153, 102, 255, 1)',
            }
        ]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'right',
                labels: {
                    font: {
                        family: 'Arial'
                    }
                }
            }
        },
        scales: {
            r: {
                angleLines: {
                    display: true
                },
                suggestedMin: 5000000,
                suggestedMax: 30000000
            }
        }
    }
});


// Stacked Bar Chart
var ctxColumnChart = document.getElementById("myColumnChart").getContext("2d");

var columnChartData = {
    labels: [
        'Ricardo Adocicados', 'La maison d\'Asie', 'Berglunds snabbköp',
        'Lazy K Kountry Store', 'Vins et alcools Chevalier',
        'Drachenblut Delikatessen', 'GROSELLA-Restaurante',
        'Tradição Hipermercados', 'Lehmanns Marktstand',
        'Familia Arquibaldo'
    ], // x축에 고객명 표시
    datasets: [{
        label: 'Beverages Sales',
        data: [
            1289315.40, 1248766.65, 1234177.75, 1226281.00,
            1210100.00, 1203164.00, 1189202.00, 1162199.00,
            1146002.85, 1135282.10
        ], // 각 고객에 대한 매출액
        backgroundColor: (ctx) => {
            var value = ctx.dataset.data[ctx.dataIndex];
            return value > 1200000 ? 'rgba(255, 99, 132, 0.8)' : value > 1150000 ? 'rgba(54, 162, 235, 0.8)' : 'rgba(75, 192, 192, 0.8)';
        }
    }]
};

new Chart(ctxColumnChart, {
    type: 'bar',
    data: columnChartData,
    options: {
        responsive: true,
        plugins: {
            legend: {
                labels: {
                    font: {
                        family: 'Arial'
                    }
                }
            }
        },
        scales: {
            x: {
                stacked: false, // 각 데이터가 누적되지 않고 개별적으로 나타납니다
            },
            y: {
                beginAtZero: true
            }
        }
    }
});

// timeline
var plotlyTimelineData = [{
    x: ['Spring', 'Summer', 'Autumn', 'Winter' ],
    y: [ // 각 계절의 총 주문 수량을 제품별로 더한 값
        14403 + 14503 + 14592 + 14474 + 12988 + 14407 + 13691 + 14310 + 13678 + 14180 + 14795 + 14327, // Spring
        14637 + 15276 + 14736 + 14642 + 14982 + 14814 + 15956 + 15619 + 15065 + 15287 + 15229 + 14017,  // Summer
        2343 + 2121 + 2396 + 2374 + 2631 + 2131 + 2481 + 2468 + 2299 + 2689 + 2298 + 2388, // Autumn
        9279 + 9111 + 9106 + 9077 + 8837 + 9344 + 9265 + 8466 + 9209 + 8593 + 8662 + 8280 // Winter

    ],
    type: 'scatter',
    mode: 'lines+markers',
    marker: {
        color: 'rgb(54, 162, 235)',
        size: 8
    },
    line: {
        color: 'rgb(54, 162, 235)',
        width: 2
    }
}];

// Plotly 레이아웃 설정
var layout = {
    title: 'Seasonal Order Count Timeline for Beverage Products',
    xaxis: {
        title: 'Season'
    },
    yaxis: {
        title: 'Order Count',
        range: true
    }
};

// Plotly로 차트 생성
Plotly.newPlot('myTimeline', plotlyTimelineData, layout);

// SQL
document.addEventListener('DOMContentLoaded', function() {

    // DOM 요소에 통계 데이터 설정
    document.getElementById('totalOrders').innerText = orderStats.totalOrders;
    document.getElementById('avgOrderValue').innerText = `$${orderStats.avgOrderValue.toFixed(2)}`;
    document.getElementById('highestOrderValue').innerText = `$${orderStats.highestOrderValue.toFixed(2)}`;
    document.getElementById('mostOrdersCustomer').innerText = orderStats.mostOrdersCustomer;
    document.getElementById('highestOrderCustomer').innerText = orderStats.highestOrderCustomer;
});

// World Map
// World Map 데이터: 각 나라의 위도(lat)와 경도(lon) 및 주문 수(order_count)
var data = [{
    type: 'scattergeo',
    locationmode: 'country names',
    lat: [37.7749, 51.1657, 46.6034, -14.2350, 55.3781, 23.6345, 6.4238, 40.4637, -34.6037, 41.8719, 56.1304, 60.1282, 47.5162, 50.8503, 61.9241, 46.8182, 56.2639, 39.3999, 53.4129, 60.4720, 51.9194], // 위도
    lon: [-122.4194, 10.4515, 2.2137, -51.9253, -3.4360, -102.5528, -66.5897, -3.7492, -58.3816, 12.5674, -106.3468, 18.6435, 14.5501, 4.3517, 25.7482, 8.2275, 9.5018, -8.2245, -8.2439, 8.4689, 19.1451], // 경도
    text: ['USA', 'Germany', 'France', 'Brazil', 'UK', 'Mexico', 'Venezuela', 'Spain', 'Argentina', 'Italy', 'Canada', 'Sweden', 'Austria', 'Belgium', 'Finland', 'Switzerland', 'Denmark', 'Portugal', 'Ireland', 'Norway', 'Poland'], // 국가
    marker: {
        size: [2409, 2309, 1799, 1678, 1345, 917, 785, 711, 576, 555, 538, 400, 393, 388, 378, 367, 367, 352, 195, 184, 170].map(x => x / 1000 * 30),
        color: [2409, 2309, 1799, 1678, 1345, 917, 785, 711, 576, 555, 538, 400, 393, 388, 378, 367, 367, 352, 195, 184, 170], // 색상에 주문 수량 반영
        colorscale: 'Portland', // 색상 스케일
        cmin: 0,
        cmax: 2500, // 최대 값으로 설정 (주문 수량 기준)
        colorbar: {
            title: '주문 수량'
        },
        line: {
            color: 'black',
            width: 2
        }
    }
}];

// 레이아웃 설정
var layout = {
    title: '해외직구 배송 도시 별 건 수',
    autosize: true, // 자동 크기 조정
    geo: {
        scope: 'world', // 세계 지도
        projection: {
            type: 'natural earth' // 'natural earth' 프로젝션 사용
        },
        showland: true, // 육지 표시
        landcolor: 'rgb(243, 243, 243)', // 육지 색상
        subunitwidth: 1,
        subunitcolor: 'rgb(217, 217, 217)'
    }
};

// Plotly.js로 지도 그리기
Plotly.newPlot('myWorldMap', data, layout);



// heatmap
document.addEventListener('DOMContentLoaded', function() {
    var heatmapData = [{
        z: [
            [93890506.00, 4524586],  // Beverages: 매출, 재고
            [57047074.00, 4086693],  // Condiments: 매출, 재고
            [67475750.00, 3118929],  // Confections: 매출, 재고
            [59690859.00, 3171647],  // Dairy Products: 매출, 재고
            [29130381.00, 2482431],  // Grains/Cereals: 매출, 재고
            [66914793.00, 1331428],  // Meat/Poultry: 매출, 재고
            [33434598.00, 808283],   // Produce: 매출, 재고
            [51251548.00, 5664895]   // Seafood: 매출, 재고
        ], // 히트맵 데이터 (매출, 재고)
        x: ['Sales', 'Stock'], // x축 값
        y: ['Beverages', 'Condiments', 'Confections', 'Dairy Products', 'Grains/Cereals', 'Meat/Poultry', 'Produce', 'Seafood'], // y축 값
        type: 'heatmap', // 히트맵 타입
        colorscale: 'Viridis', // 컬러 스케일 설정
        colorbar: {
            title: 'Value' // 색상바 타이틀
        }
    }];

    var layout = {
        title: 'Category Sales and Stock Heatmap', // 히트맵 제목
        xaxis: { title: 'Metrics' }, // x축 제목 (매출, 재고)
        yaxis: { title: 'Categories' }, // y축 제목 (카테고리)
        autosize: true, // 자동 사이즈 조정
        margin: { t: 50, r: 50, b: 50, l: 50 } // 마진 설정
    };

    // Plotly.js로 히트맵을 생성
    Plotly.newPlot('myHeatmap', heatmapData, layout);
});


