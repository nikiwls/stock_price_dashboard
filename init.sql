-- Stock Dashboard Database Schema
-- This script runs automatically when the MySQL container starts

-- Create database (already done by docker-compose, but good practice)
CREATE DATABASE IF NOT EXISTS stockdb;
USE stockdb;

-- =======================
-- Table 1: Stock Prices
-- =======================
-- Stores historical and real-time stock price data

CREATE TABLE IF NOT EXISTS stock_prices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    company_name VARCHAR(100),
    price DECIMAL(10, 2) NOT NULL,
    change_percent DECIMAL(5, 2),
    volume BIGINT,
    market_cap BIGINT,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes for faster queries
    INDEX idx_symbol (symbol),
    INDEX idx_timestamp (timestamp),
    INDEX idx_symbol_timestamp (symbol, timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =======================
-- Table 2: Chat History
-- =======================
-- Stores AI chatbot conversation history

CREATE TABLE IF NOT EXISTS chat_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(50) NOT NULL,
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    stock_symbol VARCHAR(10),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_session (session_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =======================
-- Table 3: Watchlist
-- =======================
-- Stores user's favorite stocks to watch

CREATE TABLE IF NOT EXISTS watchlist (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL DEFAULT 'default_user',
    symbol VARCHAR(10) NOT NULL,
    added_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Prevent duplicate entries
    UNIQUE KEY unique_user_symbol (user_id, symbol),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =======================
-- Insert Sample Data
-- =======================

-- Sample stock price data (for fallback when API is rate limited)
-- Watchlist is empty by default - users add their own stocks
INSERT INTO stock_prices (symbol, company_name, price, change_percent, volume) VALUES
    ('AAPL', 'Apple Inc.', 178.50, 1.25, 50000000),
    ('GOOGL', 'Alphabet Inc.', 142.30, -0.80, 25000000),
    ('MSFT', 'Microsoft Corporation', 385.00, 2.10, 30000000),
    ('TSLA', 'Tesla Inc.', 248.75, -1.50, 100000000),
    ('AMZN', 'Amazon.com Inc.', 158.20, 0.95, 40000000);

-- =======================
-- Useful SQL Queries (for learning)
-- =======================

-- Query 1: Get latest price for a stock
-- SELECT * FROM stock_prices WHERE symbol = 'AAPL' ORDER BY timestamp DESC LIMIT 1;

-- Query 2: Get price history for last 24 hours
-- SELECT * FROM stock_prices 
-- WHERE symbol = 'AAPL' AND timestamp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
-- ORDER BY timestamp DESC;

-- Query 3: Get all stocks in watchlist with latest prices
-- SELECT w.symbol, sp.price, sp.change_percent, sp.timestamp
-- FROM watchlist w
-- LEFT JOIN stock_prices sp ON w.symbol = sp.symbol
-- WHERE w.user_id = 'default_user'
-- GROUP BY w.symbol
-- HAVING sp.timestamp = MAX(sp.timestamp);

-- Query 4: Get chat history for a session
-- SELECT * FROM chat_history 
-- WHERE session_id = 'session123' 
-- ORDER BY created_at ASC;

-- Query 5: Calculate average price for a stock
-- SELECT symbol, AVG(price) as avg_price, COUNT(*) as data_points
-- FROM stock_prices
-- WHERE symbol = 'AAPL' AND timestamp >= DATE_SUB(NOW(), INTERVAL 7 DAY)
-- GROUP BY symbol;