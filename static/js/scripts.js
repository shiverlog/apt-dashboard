/*!
    * Start Bootstrap - SB Admin v7.0.7 (https://startbootstrap.com/template/sb-admin)
    * Copyright 2013-2023 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin/blob/master/LICENSE)
    */
    // 
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});

// 부드럽게 상단으로 스크롤하는 함수
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// 화면에서 일정 부분 스크롤 시 버튼을 표시하고 숨김
window.addEventListener("scroll", function () {
    var backToTopButton = document.getElementById("back-to-top");
    if (window.scrollY > 300) {
        backToTopButton.style.display = "block";
    } else {
        backToTopButton.style.display = "none";
    }
});

window.addEventListener('DOMContentLoaded', event => {
        // 테이블 ID 목록
        const tables = ['adminTable', 'customerTable', 'employeeTable', 'productTable', 'categoryTable',
            'regionTable', 'shipperTable', 'supplierTable', 'territoryTable', 'employeeTerritoryTable', 'orderStatusTable',
            'ordersTable', 'orderDetailTable', 'monthlyCategorySalesTable', 'categoryOrderCntTable'];

        // 각 테이블에 대해 DataTable을 초기화
        tables.forEach(id => {
            const datatable = document.getElementById(id);
            if (datatable) {
                new simpleDatatables.DataTable(datatable);
            }
        });
    });

document.addEventListener("DOMContentLoaded", function() {
    const body = document.body;
    const sidenav = document.querySelector('.sb-sidenav');

    // Check saved theme in localStorage
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        body.classList.add(savedTheme);
        updateSidebar(savedTheme);
    }

    // Light Mode Button Click Event
    document.getElementById('toggleLightMode').addEventListener('click', function() {
        body.classList.remove('dark-mode');
        body.classList.add('light-mode');
        updateSidebar('light-mode');
        localStorage.setItem('theme', 'light-mode');
    });

    // Dark Mode Button Click Event
    document.getElementById('toggleDarkMode').addEventListener('click', function() {
        body.classList.remove('light-mode');
        body.classList.add('dark-mode');
        updateSidebar('dark-mode');
        localStorage.setItem('theme', 'dark-mode');
    });

    // Update Sidebar based on theme
    function updateSidebar(theme) {
        if (theme === 'dark-mode') {
            sidenav.classList.remove('sb-sidenav-light');
            sidenav.classList.add('sb-sidenav-dark');
        } else {
            sidenav.classList.remove('sb-sidenav-dark');
            sidenav.classList.add('sb-sidenav-light');
        }
    }
});

function toggleNotebookView() {
    var frame = document.getElementById('jupyterFrame');
    if (frame.style.display === "none") {
        frame.style.display = "block";
    } else {
        frame.style.display = "none";
    }
}