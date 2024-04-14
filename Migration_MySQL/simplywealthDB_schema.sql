CREATE TABLE SimplyWealthApp_userprofile (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    profile_picture VARCHAR(255),
    text VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES auth_user (id) ON DELETE CASCADE
);

CREATE TABLE SimplyWealthApp_stocktransanctions (
    transaction_id VARCHAR(100) PRIMARY KEY,
    user_id INT,
    stock_symbol VARCHAR(5),
    transaction_type VARCHAR(4) DEFAULT 'buy',
    stock_price DECIMAL(10, 2),
    stock_units DECIMAL(10, 2),
    stock_price_date DATE,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES SimplyWealthApp_userprofile (user_id) ON DELETE CASCADE
);

CREATE TABLE SimplyWealthApp_userstockportfolio (
    user_id INT,
    stock_symbol VARCHAR(5),
    stock_units DECIMAL(10, 2),
    PRIMARY KEY (user_id, stock_symbol),
    FOREIGN KEY (user_id) REFERENCES SimplyWealthApp_userprofile (user_id) ON DELETE CASCADE
);

CREATE TABLE SimplyWealthApp_transaction (
    transaction_id VARCHAR(100) PRIMARY KEY,
    user_id INT,
    amount DECIMAL(10, 2),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES SimplyWealthApp_userprofile (user_id) ON DELETE CASCADE
);

CREATE TABLE SimplyWealthApp_stockspricehistory (
    unique_key BINARY(16) PRIMARY KEY,
    current_time DATE DEFAULT CURRENT_TIMESTAMP,
    stock_name VARCHAR(50),
    ticker VARCHAR(10),
    price DECIMAL(10, 2)
);

CREATE TABLE SimplyWealthApp_leaderboard (
    unique_key BINARY(16) PRIMARY KEY,
    current_time DATE DEFAULT CURRENT_TIMESTAMP,
    userid VARCHAR(30),
    current_total DECIMAL(10, 2)
);

CREATE TABLE SimplyWealthApp_topdailygainers (
    unique_key BINARY(16) PRIMARY KEY,
    insert_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    date DATE,
    ticker VARCHAR(20),
    price DECIMAL(10, 2),
    change_percentage DECIMAL(5, 2),
    volume DECIMAL(15, 2)
);

CREATE TABLE SimplyWealthApp_mostactivelytraded (
    unique_key BINARY(16) PRIMARY KEY,
    insert_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    date DATE,
    ticker VARCHAR(20),
    price DECIMAL(10, 2),
    change_percentage DECIMAL(5, 2),
    volume DECIMAL(15, 2)
);

CREATE TABLE SimplyWealthApp_topdailylosers (
    unique_key BINARY(16) PRIMARY KEY,
    insert_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    date DATE,
    ticker VARCHAR(20),
    price DECIMAL(10, 2),
    change_percentage DECIMAL(5, 2),
    volume DECIMAL(15, 2)
);
