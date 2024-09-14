
# docker exec -it apt-mysql mysql -u root -p
# ALTER USER 'apt'@'%' IDENTIFIED WITH mysql_native_password BY 'apt!1111';
# GRANT SELECT ON performance_schema.* TO 'apt'@'%';
# FLUSH PRIVILEGES;

CREATE TABLE IF NOT EXISTS Customer (
    Id VARCHAR(50) PRIMARY KEY,
    CompanyName VARCHAR(50),
    ContactName VARCHAR(50),
    ContactTitle VARCHAR(50),
    Address VARCHAR(50),
    City VARCHAR(50),
    Region VARCHAR(50),
    PostalCode VARCHAR(50),
    Country VARCHAR(50),
    Phone VARCHAR(50),
    Fax VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Employee (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    LastName VARCHAR(50),
    FirstName VARCHAR(50),
    Title VARCHAR(50),
    TitleOfCourtesy VARCHAR(50),
    BirthDate DATE,
    HireDate DATE,
    Address VARCHAR(50),
    City VARCHAR(50),
    Region VARCHAR(50),
    PostalCode VARCHAR(50),
    Country VARCHAR(50),
    HomePhone VARCHAR(50),
    Extension VARCHAR(50),
    Photo BLOB,
    Notes TEXT,
    ReportsTo INT DEFAULT NULL,
    PhotoPath VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Product (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    ProductName VARCHAR(50),
    SupplierId INT NOT NULL,
    CategoryId INT NOT NULL,
    QuantityPerUnit VARCHAR(50),
    UnitPrice DECIMAL(10, 2),
    UnitsInStock INT,
    UnitsOnOrder INT DEFAULT 0,
    ReorderLevel INT DEFAULT 0,
    Discontinued BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS Category (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    CategoryName VARCHAR(50),
    Description TEXT
);

CREATE TABLE IF NOT EXISTS Region (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    RegionDescription VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Shipper (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    CompanyName VARCHAR(50),
    Phone VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Supplier (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    CompanyName VARCHAR(50),
    ContactName VARCHAR(50),
    ContactTitle VARCHAR(50),
    Address VARCHAR(50),
    City VARCHAR(50),
    Region VARCHAR(50),
    PostalCode VARCHAR(50),
    Country VARCHAR(50),
    Phone VARCHAR(50),
    Fax VARCHAR(50),
    HomePage VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Territory (
    Id VARCHAR(50) PRIMARY KEY,
    TerritoryDescription VARCHAR(50),
    RegionId INT NOT NULL,
    FOREIGN KEY (RegionId) REFERENCES Region(Id)
);

CREATE TABLE IF NOT EXISTS EmployeeTerritory (
    Id VARCHAR(255) PRIMARY KEY,
    EmployeeId INT NOT NULL,
    TerritoryId VARCHAR(50) NOT NULL,
    FOREIGN KEY (EmployeeId) REFERENCES Employee(Id),
    FOREIGN KEY (TerritoryId) REFERENCES Territory(Id)
);

CREATE TABLE IF NOT EXISTS OrderStatus (
    Id INT PRIMARY KEY,
    StatusName VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Orders (
    Id VARCHAR(255) PRIMARY KEY,
    CustomerId VARCHAR(50) NULL,
    EmployeeId INT NULL,
    OrderDate DATE,
    RequiredDate DATE,
    ShippedDate DATE,
    ShipVia INT,
    Freight DECIMAL(10, 2) DEFAULT 0.00,
    ShipName VARCHAR(50),
    ShipAddress VARCHAR(50),
    ShipCity VARCHAR(50),
    ShipRegion VARCHAR(50),
    ShipPostalCode VARCHAR(50),
    ShipCountry VARCHAR(50),
    StatusId INT NOT NULL,
    FOREIGN KEY (CustomerId) REFERENCES Customer(Id),
    FOREIGN KEY (EmployeeId) REFERENCES Employee(Id),
    FOREIGN KEY (ShipVia) REFERENCES Shipper(Id),
    FOREIGN KEY (StatusId) REFERENCES OrderStatus(Id)
);

CREATE TABLE IF NOT EXISTS OrderDetail (
    Id VARCHAR(255) PRIMARY KEY,
    OrderId VARCHAR(255) NOT NULL,
    ProductId INT NOT NULL,
    UnitPrice DECIMAL(10, 2),
    Quantity INT,
    Discount DECIMAL(4, 2) DEFAULT 0.00,
    FOREIGN KEY (OrderId) REFERENCES Orders(Id),
    FOREIGN KEY (ProductId) REFERENCES Product(Id)
);

CREATE TABLE IF NOT EXISTS MonthlyCategorySales (
    mon VARCHAR(7),
    CategoryName VARCHAR(50),
    total_sales DECIMAL(10, 2)
);

CREATE TABLE IF NOT EXISTS CategoryOrderCnt_View (
    ym VARCHAR(7),
    CategoryId INT,
    OrderCnt INT,
    PRIMARY KEY (ym, CategoryId),
    FOREIGN KEY (CategoryId) REFERENCES Product(Id)
);

CREATE TABLE IF NOT EXISTS Admin (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL,
    email VARCHAR(128) NOT NULL UNIQUE,
    role VARCHAR(20) NOT NULL DEFAULT 'ADMIN',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
