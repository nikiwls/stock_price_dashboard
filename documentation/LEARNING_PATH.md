# 🎓 Complete Step-by-Step Learning Guide
## From Zero to Full-Stack Developer in 4 Weeks

---

## 📋 Table of Contents
1. [Learning Philosophy](#learning-philosophy)
2. [Week 1: Database & SQL Foundations](#week-1)
3. [Week 2: Python Backend with FastAPI](#week-2)
4. [Week 3: React Frontend Development](#week-3)
5. [Week 4: Integration & Advanced Features](#week-4)
6. [Daily Study Schedule](#daily-schedule)
7. [Hands-On Exercises](#exercises)

---

## 🎯 Learning Philosophy

### The Best Way to Learn Coding:

**Don't just read code → BREAK IT and FIX IT!**

```
Read Code (10%)
  ↓
Run Code (20%)
  ↓
Break Code (30%)
  ↓
Fix Code (40%)
  ↓
Build New Features (100% Understanding!)
```

### Your Learning Cycle:

1. **Read** - Understand what it does
2. **Run** - See it work
3. **Break** - Change something intentionally
4. **Fix** - Debug and make it work again
5. **Modify** - Add your own features

---

## 📅 WEEK 1: Database & SQL Foundations

### 🎯 Goal: Understand how data is stored and queried

---

### Day 1: Setup & First Database Query

#### Morning (2 hours): Get Everything Running

**Step 1: Install Docker**
```bash
# Download and install Docker Desktop
# https://www.docker.com/products/docker-desktop/

# Verify installation
docker --version
# Should show: Docker version 24.x.x
```

**Step 2: Get the Project Running**
```bash
# Clone your repo and add project files
cd stock-dashboard

# Start everything
docker-compose up --build

# Wait 2 minutes...
# Open http://localhost:3000
```

**✅ Checkpoint:** Can you see the stock dashboard in your browser?

#### Afternoon (2 hours): Your First SQL Query

**Step 1: Connect to MySQL Database**
```bash
# Open a new terminal
# Connect to the database container
docker exec -it stock_db mysql -u stockuser -pstockpass stockdb
```

**You'll see:**
```
mysql>
```

**Step 2: Run Your First Queries**
```sql
-- See all tables
SHOW TABLES;

-- Look at the stock_prices table structure
DESCRIBE stock_prices;

-- See all stock data
SELECT * FROM stock_prices;

-- Count how many records
SELECT COUNT(*) FROM stock_prices;

-- Exit MySQL
exit;
```

**📝 Exercise 1.1: Answer These Questions**
```sql
-- How many stocks are in the database?
SELECT COUNT(DISTINCT symbol) FROM stock_prices;

-- What's the highest stock price?
SELECT MAX(price) FROM stock_prices;

-- Which stock has the highest price?
SELECT symbol, price FROM stock_prices 
ORDER BY price DESC LIMIT 1;
```

**🎯 Goal Achieved When:** You can run these queries and understand the results!

---

### Day 2: Understanding Database Tables

#### Morning (2 hours): Table Relationships

**Open the init.sql file in VS Code**
```bash
code init.sql
```

**Read Through the File and Find:**

1. **How many tables are there?** (Answer: 3)
2. **What are their names?**
   - stock_prices
   - watchlist  
   - chat_history

3. **What does each table store?**

**📝 Exercise 2.1: Draw the Tables**

Draw this on paper or in a text file:

```
TABLE: stock_prices
┌────┬────────┬───────┬────────────┬────────┬───────────┐
│ id │ symbol │ price │ change_%   │ volume │ timestamp │
├────┼────────┼───────┼────────────┼────────┼───────────┤
│ 1  │ AAPL   │175.50 │    +1.25   │  50M   │ 2024...   │
│ 2  │ GOOGL  │140.30 │    -0.80   │  25M   │ 2024...   │
└────┴────────┴───────┴────────────┴────────┴───────────┘

TABLE: watchlist
┌────┬──────────┬────────┬───────────┐
│ id │ user_id  │ symbol │ added_at  │
├────┼──────────┼────────┼───────────┤
│ 1  │ default  │ AAPL   │ 2024...   │
│ 2  │ default  │ GOOGL  │ 2024...   │
└────┴──────────┴────────┴───────────┘
```

#### Afternoon (2 hours): SQL CRUD Operations

**CRUD = Create, Read, Update, Delete**

```sql
-- Connect to database first
docker exec -it stock_db mysql -u stockuser -pstockpass stockdb
```

**1️⃣ CREATE (Insert new data)**
```sql
-- Add a new stock to watchlist
INSERT INTO watchlist (user_id, symbol) 
VALUES ('default', 'NVDA');

-- Check it was added
SELECT * FROM watchlist;
```

**2️⃣ READ (Query data)**
```sql
-- Get all Apple stock prices
SELECT * FROM stock_prices 
WHERE symbol = 'AAPL';

-- Get stocks with positive change
SELECT symbol, price, change_percent 
FROM stock_prices 
WHERE change_percent > 0;

-- Get top 3 most expensive stocks
SELECT symbol, price 
FROM stock_prices 
ORDER BY price DESC 
LIMIT 3;
```

**3️⃣ UPDATE (Modify existing data)**
```sql
-- Update a stock price
UPDATE stock_prices 
SET price = 180.00 
WHERE symbol = 'AAPL' AND id = 1;

-- Check the change
SELECT * FROM stock_prices WHERE symbol = 'AAPL';
```

**4️⃣ DELETE (Remove data)**
```sql
-- Remove a stock from watchlist
DELETE FROM watchlist 
WHERE symbol = 'NVDA';

-- Verify it's gone
SELECT * FROM watchlist;
```

**📝 Exercise 2.2: Practice CRUD**
```sql
-- 1. Add TSLA to your watchlist
-- Your code here:

-- 2. Find all stocks worth more than $200
-- Your code here:

-- 3. Update GOOGL price to 145.00
-- Your code here:

-- 4. Delete the oldest stock_prices record
-- Your code here:
```

**🎯 Goal Achieved When:** You can add, read, update, and delete data confidently!

---

### Day 3: SQL Joins & Relationships

#### Morning (2 hours): Understanding Foreign Keys

**Concept: Tables are Connected!**

```
watchlist              stock_prices
┌────────┐            ┌────────┐
│ symbol │────────────│ symbol │
└────────┘            └────────┘
   AAPL       same       AAPL
```

**Run This Join Query:**
```sql
-- Get watchlist WITH current prices
SELECT 
    w.symbol,
    sp.price,
    sp.change_percent
FROM watchlist w
LEFT JOIN stock_prices sp ON w.symbol = sp.symbol
WHERE sp.timestamp = (
    SELECT MAX(timestamp) 
    FROM stock_prices sp2 
    WHERE sp2.symbol = w.symbol
);
```

**Break it down:**
1. `FROM watchlist w` - Start with watchlist
2. `LEFT JOIN stock_prices sp` - Add price data
3. `ON w.symbol = sp.symbol` - Match by stock symbol
4. `WHERE sp.timestamp = (...)` - Get only latest price

#### Afternoon (2 hours): Advanced Queries

**Aggregation Functions:**
```sql
-- Average price per stock
SELECT 
    symbol,
    AVG(price) as avg_price,
    COUNT(*) as num_records
FROM stock_prices
GROUP BY symbol;

-- Total volume traded
SELECT 
    symbol,
    SUM(volume) as total_volume
FROM stock_prices
GROUP BY symbol
ORDER BY total_volume DESC;

-- Price range (high - low)
SELECT 
    symbol,
    MAX(price) - MIN(price) as price_range
FROM stock_prices
GROUP BY symbol;
```

**📝 Exercise 3.1: Write Complex Queries**
```sql
-- 1. Find the stock with the highest average price
-- Hint: Use AVG() and ORDER BY

-- 2. Count how many times each stock appears in stock_prices
-- Hint: Use COUNT() and GROUP BY

-- 3. Get all stocks in watchlist that increased in price
-- Hint: Use JOIN and WHERE change_percent > 0
```

**🎯 Goal Achieved When:** You understand how to combine data from multiple tables!

---

### Day 4: Database Design Principles

#### Morning (2 hours): Why Tables Look This Way

**Good Design Principles:**

**1. Primary Keys (id column)**
```sql
-- Every table has an 'id' column
-- Why? Unique identifier for each row

CREATE TABLE example (
    id INT PRIMARY KEY AUTO_INCREMENT,  -- ← Unique, auto-generated
    name VARCHAR(100)
);
```

**2. Indexes (for speed)**
```sql
-- Indexes make queries MUCH faster
-- Like a book index - jump to the page instead of reading everything

-- Check existing indexes
SHOW INDEX FROM stock_prices;

-- Why we have these indexes:
-- idx_symbol: Fast lookup by stock symbol
-- idx_timestamp: Fast lookup by time
```

**3. Data Types Matter**
```sql
-- Wrong: Using VARCHAR for price
price VARCHAR(10)  -- ❌ Can't do math, wastes space

-- Right: Using DECIMAL for price
price DECIMAL(10, 2)  -- ✅ Precise, can calculate
```

**📝 Exercise 4.1: Design Your Own Table**
```sql
-- Design a table to store user portfolios
-- Should track: user, stock, quantity, purchase_price, purchase_date

CREATE TABLE portfolio (
    -- Add columns here
    -- Think about data types!
);
```

#### Afternoon (2 hours): Practice with Real Data

**Scenario: Build a Stock Performance Report**

```sql
-- Create a view of best performing stocks
CREATE VIEW top_performers AS
SELECT 
    symbol,
    AVG(price) as avg_price,
    AVG(change_percent) as avg_change,
    COUNT(*) as data_points
FROM stock_prices
GROUP BY symbol
HAVING avg_change > 0
ORDER BY avg_change DESC;

-- Use the view
SELECT * FROM top_performers;
```

**📝 Exercise 4.2: Build Reports**
```sql
-- 1. Create a report of stocks with price above $100
-- 2. Find stocks with high volatility (big price swings)
-- 3. Calculate total market cap of watchlist stocks
```

**🎯 Week 1 Complete When:** 
- ✅ You can write SELECT, INSERT, UPDATE, DELETE
- ✅ You understand JOINs
- ✅ You know why indexes exist
- ✅ You can design a simple table

---

## 📅 WEEK 2: Python Backend with FastAPI

### 🎯 Goal: Build APIs that connect database to frontend

---

### Day 5: Understanding the Backend Structure

#### Morning (2 hours): Read backend/database.py

**Open in VS Code:**
```bash
code backend/database.py
```

**Read Through and Answer:**

1. **What is SQLAlchemy?**
   - It's an ORM (Object-Relational Mapping)
   - Lets you use Python objects instead of SQL

2. **Find the DATABASE_URL**
   ```python
   DATABASE_URL = "mysql+pymysql://stockuser:stockpass@db:3306/stockdb"
   ```
   - Break down each part:
   - `mysql+pymysql://` - Database type
   - `stockuser:stockpass` - Username:Password
   - `@db:3306` - Host:Port
   - `/stockdb` - Database name

3. **Find the Three Models (Tables)**
   ```python
   class StockPrice(Base):      # → stock_prices table
   class ChatHistory(Base):     # → chat_history table
   class Watchlist(Base):       # → watchlist table
   ```

**📝 Exercise 5.1: Understand the Model**
```python
# Look at StockPrice model
class StockPrice(Base):
    __tablename__ = "stock_prices"
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    # ... more columns

# Answer these:
# 1. What does __tablename__ do?
# 2. What does nullable=False mean?
# 3. Why use DECIMAL for price instead of Float?
```

#### Afternoon (2 hours): Run Python Code Manually

**Test the Database Connection:**

```bash
# Enter the backend container
docker exec -it stock_backend bash

# Start Python interactive shell
python
```

**Try This Code:**
```python
# Import the database
from database import SessionLocal, StockPrice

# Create a database session
db = SessionLocal()

# Query all stocks
stocks = db.query(StockPrice).all()
for stock in stocks:
    print(f"{stock.symbol}: ${stock.price}")

# Query specific stock
aapl = db.query(StockPrice).filter(
    StockPrice.symbol == "AAPL"
).first()
print(f"Apple price: ${aapl.price}")

# Exit Python
exit()

# Exit container
exit
```

**📝 Exercise 5.2: Write Your Own Queries**
```python
# 1. Get all stocks with price > $150
# 2. Count how many GOOGL entries exist
# 3. Get the most recent stock price for any symbol
```

**🎯 Goal Achieved When:** You understand ORM models and can query with Python!

---

### Day 6: FastAPI Endpoints

#### Morning (2 hours): Read backend/main.py

**Open the file:**
```bash
code backend/main.py
```

**Understand the Structure:**

```python
# 1. Imports
from fastapi import FastAPI
from database import get_db, StockPrice

# 2. Create app
app = FastAPI()

# 3. Define endpoints
@app.get("/api/stocks/{symbol}")
async def get_stock(symbol: str):
    # Handle request
    return data
```

**Find These Endpoints:**
```python
GET    /                           # Home page
GET    /api/stocks/{symbol}        # Get stock data
GET    /api/watchlist              # Get watchlist
POST   /api/watchlist              # Add to watchlist
DELETE /api/watchlist/{symbol}     # Remove from watchlist
POST   /api/chat                   # AI chatbot
```

**Test Them in Your Browser:**
```
http://localhost:8000/docs
```

This opens **Swagger UI** - interactive API documentation!

#### Afternoon (2 hours): Create Your First Endpoint

**📝 Exercise 6.1: Add a New Endpoint**

**Add this to main.py (around line 100):**
```python
@app.get("/api/stocks/{symbol}/stats")
async def get_stock_stats(symbol: str, db: Session = Depends(get_db)):
    """
    Get statistics for a stock (min, max, avg price)
    """
    # Query all prices for this symbol
    prices = db.query(StockPrice).filter(
        StockPrice.symbol == symbol.upper()
    ).all()
    
    if not prices:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    # Calculate stats
    price_values = [float(p.price) for p in prices]
    
    return {
        "symbol": symbol.upper(),
        "min_price": min(price_values),
        "max_price": max(price_values),
        "avg_price": sum(price_values) / len(price_values),
        "data_points": len(prices)
    }
```

**Test It:**
```bash
# Restart backend
docker-compose restart backend

# Go to:
http://localhost:8000/docs

# Try your new endpoint: /api/stocks/AAPL/stats
```

**🎯 Goal Achieved When:** You've created and tested your own API endpoint!

---

### Day 7: Understanding Dependencies & Database Sessions

#### Morning (2 hours): Dependency Injection

**What is `Depends(get_db)`?**

```python
# This pattern:
@app.get("/api/stocks")
async def get_stocks(db: Session = Depends(get_db)):
    # Use db here
    stocks = db.query(StockPrice).all()
    return stocks

# Means:
# 1. FastAPI calls get_db() automatically
# 2. Creates a database session
# 3. Passes it as 'db' parameter
# 4. Closes it when done (in finally block)
```

**Why is this good?**
- ✅ Automatic session management
- ✅ No forgotten connections
- ✅ Clean code
- ✅ Easy testing

**📝 Exercise 7.1: Understand the Flow**

Study this code in `database.py`:
```python
def get_db():
    db = SessionLocal()    # 1. Create session
    try:
        yield db           # 2. Give it to endpoint
    finally:
        db.close()         # 3. Always close (even if error!)
```

#### Afternoon (2 hours): Error Handling

**Add Error Handling to Your Endpoint:**

```python
@app.get("/api/stocks/{symbol}")
async def get_stock(symbol: str, db: Session = Depends(get_db)):
    try:
        # Get stock data from Yahoo Finance
        stock_data = stock_service.get_stock_data(symbol.upper())
        
        if not stock_data:
            raise HTTPException(
                status_code=404,
                detail=f"Stock {symbol} not found"
            )
        
        # Save to database
        new_price = StockPrice(**stock_data)
        db.add(new_price)
        db.commit()
        
        return stock_data
        
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        # Log the error
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
```

**📝 Exercise 7.2: Add Error Handling**
```python
# Add proper error handling to the stats endpoint you created
# Handle these cases:
# 1. Stock not found
# 2. Database connection error
# 3. Invalid symbol (empty string)
```

**🎯 Goal Achieved When:** You understand dependencies and can handle errors!

---

### Day 8: Stock Service & External APIs

#### Morning (2 hours): Read backend/stock_service.py

**Understanding yfinance:**

```python
import yfinance as yf

# Create a ticker object
ticker = yf.Ticker("AAPL")

# Get information
info = ticker.info

# Extract what we need
data = {
    'symbol': 'AAPL',
    'price': info.get('currentPrice'),
    'volume': info.get('volume'),
    'market_cap': info.get('marketCap')
}
```

**Why yfinance is great:**
- ✅ FREE (no API key needed!)
- ✅ Real-time data
- ✅ Historical data
- ✅ Company information

**Test it yourself:**
```bash
# Enter backend container
docker exec -it stock_backend bash

# Start Python
python

# Try yfinance
import yfinance as yf
ticker = yf.Ticker("AAPL")
print(ticker.info['currentPrice'])
print(ticker.info['longName'])
```

#### Afternoon (2 hours): Modify the Stock Service

**📝 Exercise 8.1: Add a New Feature**

**Add this function to stock_service.py:**

```python
@staticmethod
def get_company_info(symbol: str) -> Optional[Dict]:
    """
    Get detailed company information
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        return {
            'symbol': symbol.upper(),
            'company_name': info.get('longName', 'N/A'),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'website': info.get('website', 'N/A'),
            'description': info.get('longBusinessSummary', 'N/A'),
            'employees': info.get('fullTimeEmployees', 0),
            'city': info.get('city', 'N/A'),
            'country': info.get('country', 'N/A')
        }
    except Exception as e:
        print(f"Error getting company info: {e}")
        return None
```

**Now add an endpoint in main.py:**
```python
@app.get("/api/stocks/{symbol}/info")
async def get_company_info(symbol: str):
    """Get detailed company information"""
    info = stock_service.get_company_info(symbol.upper())
    
    if not info:
        raise HTTPException(status_code=404, detail="Company not found")
    
    return info
```

**Test it:**
```
http://localhost:8000/api/stocks/AAPL/info
```

**🎯 Week 2 Complete When:**
- ✅ You understand FastAPI endpoints
- ✅ You can create new API routes
- ✅ You understand database sessions
- ✅ You can integrate external APIs

---

## 📅 WEEK 3: React Frontend Development

### 🎯 Goal: Build beautiful, interactive user interfaces

---

### Day 9: Understanding React Basics

#### Morning (2 hours): Read frontend/src/App.js

**Open the file:**
```bash
code frontend/src/App.js
```

**Core React Concepts:**

**1. State (Component Memory)**
```javascript
const [watchlist, setWatchlist] = useState([]);

// useState creates two things:
// - watchlist: current value
// - setWatchlist: function to update it

// Update state:
setWatchlist([...newStocks]);
```

**2. Effects (Side Effects)**
```javascript
useEffect(() => {
    // This runs when component loads
    loadWatchlist();
}, []);  // ← Empty array = run once on load

useEffect(() => {
    // This runs when selectedStock changes
    console.log("Selected:", selectedStock);
}, [selectedStock]);  // ← Run when this changes
```

**3. Event Handlers**
```javascript
const handleClick = (symbol) => {
    console.log("Clicked:", symbol);
    selectStock(symbol);
};

// In JSX:
<button onClick={() => handleClick('AAPL')}>
    Click me
</button>
```

**📝 Exercise 9.1: Find These in App.js**
```javascript
// 1. How many useState() calls are there?
// 2. How many useEffect() calls?
// 3. What does loadWatchlist() do?
// 4. Find the function that handles search
```

#### Afternoon (2 hours): Component Structure

**Break Down the App Component:**

```javascript
function App() {
    // 1. STATE (data storage)
    const [watchlist, setWatchlist] = useState([]);
    
    // 2. EFFECTS (load data, subscriptions)
    useEffect(() => {
        loadWatchlist();
    }, []);
    
    // 3. FUNCTIONS (event handlers)
    const selectStock = (symbol) => {
        // ...
    };
    
    // 4. RENDER (what user sees)
    return (
        <div className="app">
            {/* Components here */}
        </div>
    );
}
```

**📝 Exercise 9.2: Trace a User Action**

**Follow this flow:**
```javascript
// User clicks on a stock in watchlist
// ↓
onClick={() => selectStock(stock.symbol)}
// ↓
const selectStock = async (symbol) => {
    // Makes API call
    const response = await axios.get(`/api/stocks/${symbol}`);
    // Updates state
    setSelectedStock(response.data);
}
// ↓
// React detects state change
// ↓
// Component re-renders with new data
// ↓
// Chart shows updated data
```

**Trace this yourself with console.log:**
```javascript
const selectStock = async (symbol) => {
    console.log("1. User clicked:", symbol);
    
    const response = await axios.get(`/api/stocks/${symbol}`);
    console.log("2. Got data:", response.data);
    
    setSelectedStock(response.data);
    console.log("3. Updated state");
};
```

**🎯 Goal Achieved When:** You understand state, effects, and event handlers!

---

### Day 10: API Integration

#### Morning (2 hours): Understanding axios

**How Frontend Talks to Backend:**

```javascript
import axios from 'axios';

// GET request
const response = await axios.get('http://localhost:8000/api/stocks/AAPL');
console.log(response.data);  // The JSON data

// POST request
await axios.post('http://localhost:8000/api/watchlist', {
    symbol: 'AAPL',
    user_id: 'default_user'
});

// DELETE request
await axios.delete('http://localhost:8000/api/watchlist/AAPL');
```

**Find These API Calls in App.js:**

```javascript
// Load watchlist (GET)
const loadWatchlist = async () => {
    const response = await axios.get(`${API_URL}/api/watchlist`);
    setWatchlist(response.data.stocks);
};

// Add to watchlist (POST)
const addToWatchlist = async (symbol) => {
    await axios.post(`${API_URL}/api/watchlist`, { symbol });
    loadWatchlist();  // Refresh the list
};

// Remove from watchlist (DELETE)
const removeFromWatchlist = async (symbol) => {
    await axios.delete(`${API_URL}/api/watchlist/${symbol}`);
    loadWatchlist();
};
```

**📝 Exercise 10.1: Add Error Handling**

```javascript
const loadWatchlist = async () => {
    try {
        const response = await axios.get(`${API_URL}/api/watchlist`);
        setWatchlist(response.data.stocks);
    } catch (error) {
        console.error("Failed to load watchlist:", error);
        // Show error message to user
        alert("Could not load watchlist");
    }
};
```

**Add error handling to all API calls!**

#### Afternoon (2 hours): Loading States

**Show User When Data is Loading:**

```javascript
// Add loading state
const [isLoading, setIsLoading] = useState(false);

const selectStock = async (symbol) => {
    setIsLoading(true);  // Start loading
    
    try {
        const response = await axios.get(`/api/stocks/${symbol}`);
        setSelectedStock(response.data);
    } catch (error) {
        console.error(error);
    } finally {
        setIsLoading(false);  // Stop loading
    }
};

// In JSX:
{isLoading ? (
    <div>Loading...</div>
) : (
    <div>Stock Details Here</div>
)}
```

**📝 Exercise 10.2: Add Loading Spinner**

**Add this to your CSS:**
```css
.loading-spinner {
    border: 4px solid #f3f3f3;
    border-top: 4px solid #00d4ff;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
```

**Use it:**
```javascript
{isLoading && (
    <div className="loading-spinner"></div>
)}
```

**🎯 Goal Achieved When:** You can make API calls and handle loading states!

---

### Day 11: WebSocket for Real-Time Updates

#### Morning (2 hours): Understanding WebSockets

**HTTP vs WebSocket:**

```
HTTP (Request-Response):
Client: "Hey, any updates?" ──────────→ Server
Client: ←────────────────────────── "Here's data"
Client: "Any updates now?" ──────────→ Server
Client: ←────────────────────────── "Here's data"
(Repeat every few seconds... inefficient!)

WebSocket (Persistent Connection):
Client: "Connect me!" ───────────────→ Server
Client: ←──────────────────── "Connected!"
        ↕ (Stay connected)
Client: ←──────────────────── "New data!"
Client: ←──────────────────── "New data!"
Client: ←──────────────────── "New data!"
(Server pushes updates instantly!)
```

**Find the WebSocket Code in App.js:**

```javascript
const connectWebSocket = () => {
    // Create WebSocket connection
    wsRef.current = new WebSocket('ws://localhost:8000/ws/stocks');
    
    // When message received
    wsRef.current.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === 'stock_update') {
            updateWatchlistPrices(data.data);
        }
    };
    
    // When connection closes
    wsRef.current.onclose = () => {
        console.log('WebSocket disconnected');
    };
    
    // When error occurs
    wsRef.current.onerror = (error) => {
        console.error('WebSocket error:', error);
    };
};
```

#### Afternoon (2 hours): Implement WebSocket Updates

**📝 Exercise 11.1: Add Connection Status**

```javascript
// Add state
const [wsConnected, setWsConnected] = useState(false);

// Update WebSocket code
const connectWebSocket = () => {
    wsRef.current = new WebSocket('ws://localhost:8000/ws/stocks');
    
    wsRef.current.onopen = () => {
        console.log('Connected!');
        setWsConnected(true);
    };
    
    wsRef.current.onclose = () => {
        console.log('Disconnected');
        setWsConnected(false);
    };
    
    wsRef.current.onmessage = (event) => {
        const data = JSON.parse(event.data);
        updateWatchlistPrices(data.data);
    };
};

// Show status in UI
<div className={`connection-status ${wsConnected ? 'connected' : 'disconnected'}`}>
    {wsConnected ? '● Live' : '○ Disconnected'}
</div>
```

**Add CSS:**
```css
.connection-status {
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 14px;
}

.connected {
    background: rgba(46, 204, 113, 0.2);
    color: #2ecc71;
    border: 1px solid #2ecc71;
}

.disconnected {
    background: rgba(255, 71, 87, 0.2);
    color: #ff4757;
    border: 1px solid #ff4757;
}
```

**🎯 Goal Achieved When:** You see real-time price updates and connection status!

---

### Day 12: Styling & UI Polish

#### Morning (2 hours): Understanding CSS Structure

**Read frontend/src/App.css**

**Key Concepts:**

**1. CSS Variables**
```css
:root {
    --primary: #00d4ff;
    --background: #0f0c29;
    --text: #ffffff;
}

.button {
    color: var(--primary);  /* Use the variable */
}
```

**2. Flexbox Layout**
```css
.container {
    display: flex;
    justify-content: space-between;  /* Horizontal spacing */
    align-items: center;             /* Vertical alignment */
    gap: 1rem;                       /* Space between items */
}
```

**3. Grid Layout**
```css
.grid {
    display: grid;
    grid-template-columns: 1fr 2fr;  /* 2 columns: 1:2 ratio */
    gap: 2rem;
}
```

**📝 Exercise 12.1: Modify the Color Scheme**

**Change to a light theme:**
```css
/* In App.css, find and replace: */

/* Old (dark) */
background: #0f0c29;
color: #ffffff;

/* New (light) */
background: #f5f5f5;
color: #333333;
```

**Or create your own color scheme:**
```css
/* Ocean theme */
--primary: #0077be;
--secondary: #00a8e8;
--background: #f0f8ff;

/* Sunset theme */
--primary: #ff6b6b;
--secondary: #feca57;
--background: #2c2c54;

/* Forest theme */
--primary: #27ae60;
--secondary: #2ecc71;
--background: #1e3a20;
```

#### Afternoon (2 hours): Add New UI Components

**📝 Exercise 12.2: Create a Price Alert Component**

**Add this component:**
```javascript
// Add to App.js
function PriceAlert({ stock, threshold }) {
    const [showAlert, setShowAlert] = useState(false);
    
    useEffect(() => {
        if (stock && stock.price > threshold) {
            setShowAlert(true);
        }
    }, [stock, threshold]);
    
    if (!showAlert) return null;
    
    return (
        <div className="price-alert">
            ⚠️ {stock.symbol} is above ${threshold}!
            <button onClick={() => setShowAlert(false)}>×</button>
        </div>
    );
}

// Use it in your render:
<PriceAlert stock={selectedStock} threshold={200} />
```

**Add CSS:**
```css
.price-alert {
    position: fixed;
    top: 80px;
    right: 20px;
    background: rgba(255, 107, 107, 0.9);
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    animation: slideIn 0.3s ease;
}

@keyframes slideIn {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}
```

**🎯 Week 3 Complete When:**
- ✅ You understand React state and effects
- ✅ You can make API calls
- ✅ You understand WebSockets
- ✅ You can style components

---

## 📅 WEEK 4: Integration & Advanced Features

### 🎯 Goal: Connect everything and build new features

---

### Day 13: Understanding the Full Stack Flow

#### Full Day (4 hours): Trace a Complete User Action

**Scenario: User Searches for "TSLA"**

**Step 1: Frontend (React)**
```javascript
// User types in search box
<input 
    value={searchQuery}
    onChange={(e) => handleSearch(e.target.value)}
/>

// handleSearch function
const handleSearch = async (query) => {
    setSearchQuery(query);
    if (query.length > 0) {
        // Make API call
        const response = await axios.get(`/api/stocks/search/${query}`);
        setSearchResults(response.data.results);
    }
};
```

**Step 2: Backend (FastAPI)**
```python
# main.py
@app.get("/api/stocks/search/{query}")
async def search_stocks(query: str):
    # Call stock service
    results = stock_service.search_stocks(query)
    return {"results": results}
```

**Step 3: Stock Service**
```python
# stock_service.py
@staticmethod
def search_stocks(query: str) -> List[Dict]:
    # Search in predefined list
    common_stocks = [
        {'symbol': 'TSLA', 'name': 'Tesla Inc.'},
        # ...
    ]
    
    # Filter results
    results = [s for s in common_stocks if query.lower() in s['name'].lower()]
    return results
```

**Step 4: Back to Frontend**
```javascript
// Display results
{searchResults.map(stock => (
    <div 
        key={stock.symbol}
        onClick={() => addToWatchlist(stock.symbol)}
    >
        {stock.symbol} - {stock.name}
    </div>
))}
```

**📝 Exercise 13.1: Add Console Logs**

Add `console.log()` at every step to see the data flow:

```javascript
// Frontend
const handleSearch = async (query) => {
    console.log("1. User typed:", query);
    setSearchQuery(query);
    
    const response = await axios.get(`/api/stocks/search/${query}`);
    console.log("2. Got results:", response.data);
    
    setSearchResults(response.data.results);
    console.log("3. Updated state");
};
```

```python
# Backend
@app.get("/api/stocks/search/{query}")
async def search_stocks(query: str):
    print(f"4. Received search query: {query}")
    results = stock_service.search_stocks(query)
    print(f"5. Found {len(results)} results")
    return {"results": results}
```

**Watch the console to see the flow!**

---

### Day 14: Build a New Feature (Portfolio Tracker)

#### Morning (2 hours): Design the Database

**📝 Exercise 14.1: Create Portfolio Table**

**Add to init.sql:**
```sql
CREATE TABLE IF NOT EXISTS portfolio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL DEFAULT 'default_user',
    symbol VARCHAR(10) NOT NULL,
    quantity INT NOT NULL,
    purchase_price DECIMAL(10, 2) NOT NULL,
    purchase_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_user_symbol (user_id, symbol)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Sample data
INSERT INTO portfolio (symbol, quantity, purchase_price) VALUES
    ('AAPL', 10, 150.00),
    ('GOOGL', 5, 120.00),
    ('MSFT', 8, 350.00);
```

**Restart database:**
```bash
docker-compose down
docker-compose up --build
```

#### Afternoon (2 hours): Create Backend API

**📝 Exercise 14.2: Add Portfolio Endpoints**

**Add to database.py:**
```python
class Portfolio(Base):
    __tablename__ = "portfolio"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), nullable=False, default="default_user")
    symbol = Column(String(10), nullable=False)
    quantity = Column(Integer, nullable=False)
    purchase_price = Column(DECIMAL(10, 2), nullable=False)
    purchase_date = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "symbol": self.symbol,
            "quantity": self.quantity,
            "purchase_price": float(self.purchase_price),
            "purchase_date": self.purchase_date.isoformat()
        }
```

**Add to main.py:**
```python
from database import Portfolio

@app.get("/api/portfolio")
async def get_portfolio(
    user_id: str = "default_user",
    db: Session = Depends(get_db)
):
    """Get user's portfolio with current P&L"""
    # Get portfolio holdings
    holdings = db.query(Portfolio).filter(
        Portfolio.user_id == user_id
    ).all()
    
    # Get current prices
    portfolio_data = []
    total_cost = 0
    total_value = 0
    
    for holding in holdings:
        # Get current price
        current_stock = stock_service.get_stock_data(holding.symbol)
        current_price = current_stock['price'] if current_stock else 0
        
        # Calculate P&L
        cost_basis = float(holding.purchase_price) * holding.quantity
        current_value = current_price * holding.quantity
        profit_loss = current_value - cost_basis
        profit_loss_percent = (profit_loss / cost_basis * 100) if cost_basis > 0 else 0
        
        total_cost += cost_basis
        total_value += current_value
        
        portfolio_data.append({
            "symbol": holding.symbol,
            "quantity": holding.quantity,
            "purchase_price": float(holding.purchase_price),
            "current_price": current_price,
            "cost_basis": cost_basis,
            "current_value": current_value,
            "profit_loss": profit_loss,
            "profit_loss_percent": profit_loss_percent
        })
    
    return {
        "holdings": portfolio_data,
        "total_cost": total_cost,
        "total_value": total_value,
        "total_profit_loss": total_value - total_cost,
        "total_return_percent": ((total_value - total_cost) / total_cost * 100) if total_cost > 0 else 0
    }

@app.post("/api/portfolio")
async def add_to_portfolio(
    symbol: str,
    quantity: int,
    purchase_price: float,
    user_id: str = "default_user",
    db: Session = Depends(get_db)
):
    """Add stock to portfolio"""
    new_holding = Portfolio(
        user_id=user_id,
        symbol=symbol.upper(),
        quantity=quantity,
        purchase_price=purchase_price
    )
    db.add(new_holding)
    db.commit()
    
    return {"message": f"Added {quantity} shares of {symbol}"}
```

**Test it:**
```
http://localhost:8000/docs
Try: GET /api/portfolio
```

---

### Day 15: Build Portfolio Frontend

**📝 Exercise 15.1: Create Portfolio Component**

**Add to App.js:**
```javascript
// Add state
const [portfolio, setPortfolio] = useState(null);
const [showPortfolio, setShowPortfolio] = useState(false);

// Load portfolio
const loadPortfolio = async () => {
    try {
        const response = await axios.get(`${API_URL}/api/portfolio`);
        setPortfolio(response.data);
    } catch (error) {
        console.error("Error loading portfolio:", error);
    }
};

// Add to useEffect
useEffect(() => {
    loadWatchlist();
    loadPortfolio();  // Load portfolio on mount
}, []);

// Portfolio component
function PortfolioView({ portfolio, onClose }) {
    if (!portfolio) return null;
    
    return (
        <div className="portfolio-modal">
            <div className="portfolio-content">
                <div className="portfolio-header">
                    <h2>My Portfolio</h2>
                    <button onClick={onClose}>×</button>
                </div>
                
                <div className="portfolio-summary">
                    <div className="summary-item">
                        <span>Total Value</span>
                        <strong>${portfolio.total_value.toFixed(2)}</strong>
                    </div>
                    <div className="summary-item">
                        <span>Total Cost</span>
                        <strong>${portfolio.total_cost.toFixed(2)}</strong>
                    </div>
                    <div className={`summary-item ${portfolio.total_profit_loss >= 0 ? 'positive' : 'negative'}`}>
                        <span>Profit/Loss</span>
                        <strong>
                            ${portfolio.total_profit_loss.toFixed(2)}
                            ({portfolio.total_return_percent.toFixed(2)}%)
                        </strong>
                    </div>
                </div>
                
                <div className="portfolio-holdings">
                    {portfolio.holdings.map((holding, index) => (
                        <div key={index} className="holding-item">
                            <div className="holding-header">
                                <strong>{holding.symbol}</strong>
                                <span>{holding.quantity} shares</span>
                            </div>
                            <div className="holding-details">
                                <div>
                                    <span>Purchase:</span>
                                    <span>${holding.purchase_price.toFixed(2)}</span>
                                </div>
                                <div>
                                    <span>Current:</span>
                                    <span>${holding.current_price.toFixed(2)}</span>
                                </div>
                                <div className={holding.profit_loss >= 0 ? 'positive' : 'negative'}>
                                    <span>P/L:</span>
                                    <span>
                                        ${holding.profit_loss.toFixed(2)}
                                        ({holding.profit_loss_percent.toFixed(2)}%)
                                    </span>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

// Add to render
<button onClick={() => setShowPortfolio(true)}>
    View Portfolio
</button>

{showPortfolio && (
    <PortfolioView 
        portfolio={portfolio}
        onClose={() => setShowPortfolio(false)}
    />
)}
```

**Add CSS:**
```css
.portfolio-modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.portfolio-content {
    background: rgba(26, 26, 46, 0.98);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 2rem;
    max-width: 600px;
    width: 90%;
    max-height: 80vh;
    overflow-y: auto;
}

.portfolio-summary {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin: 1.5rem 0;
}

.summary-item {
    background: rgba(0, 212, 255, 0.05);
    padding: 1rem;
    border-radius: 8px;
    text-align: center;
}

.summary-item span {
    display: block;
    color: #888;
    font-size: 0.875rem;
    margin-bottom: 0.5rem;
}

.summary-item strong {
    font-size: 1.5rem;
}

.holding-item {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 1rem;
}
```

**🎯 Goal Achieved When:** You have a working portfolio tracker showing P&L!

---

### Day 16: Final Polish & Deployment Prep

#### Morning (2 hours): Code Review & Cleanup

**📝 Exercise 16.1: Clean Up Your Code**

**Checklist:**
- [ ] Remove all `console.log()` statements (or comment them out)
- [ ] Add comments to complex functions
- [ ] Check for unused imports
- [ ] Format code consistently
- [ ] Add error handling to all API calls
- [ ] Test all features work

**Example cleanup:**
```javascript
// Before
const loadWatchlist = async () => {
  console.log('loading...')  // Remove this
  const r = await axios.get(url)  // Bad variable name
  setWatchlist(r.data.stocks)
}

// After
/**
 * Load user's watchlist from the API
 * Updates the watchlist state with current stock prices
 */
const loadWatchlist = async () => {
    try {
        const response = await axios.get(`${API_URL}/api/watchlist`);
        setWatchlist(response.data.stocks);
    } catch (error) {
        console.error("Failed to load watchlist:", error);
        // Show user-friendly error
    }
};
```

#### Afternoon (2 hours): Testing Everything

**📝 Exercise 16.2: Manual Testing Checklist**

Test each feature:

- [ ] Can load the app (http://localhost:3000)
- [ ] Can see stock prices
- [ ] Can search for stocks
- [ ] Can add stock to watchlist
- [ ] Can remove stock from watchlist
- [ ] Can select a stock and see chart
- [ ] Can chat with AI (if API key set)
- [ ] WebSocket shows "Live" status
- [ ] Prices update automatically
- [ ] Portfolio shows correct P/L
- [ ] All buttons work
- [ ] No console errors

**Document Bugs:**
```
Bug List:
1. Search doesn't clear after adding stock
   Fix: Add setSearchQuery('') after addToWatchlist()

2. Chart doesn't update when selecting same stock twice
   Fix: Add key prop to chart component

3. Portfolio modal doesn't close with Escape key
   Fix: Add event listener for Escape key
```

**🎯 Week 4 Complete When:**
- ✅ You built a new feature (portfolio)
- ✅ You understand full-stack flow
- ✅ Code is clean and documented
- ✅ All features tested and working

---

## 📊 Daily Study Schedule

### Recommended Daily Routine:

```
Morning Session (2 hours):
├─ 09:00-09:30 → Review previous day's work
├─ 09:30-10:30 → Read new code/concepts
└─ 10:30-11:00 → Run code, experiment

Afternoon Session (2 hours):
├─ 14:00-15:00 → Hands-on exercises
├─ 15:00-15:45 → Build new features
└─ 15:45-16:00 → Document what you learned

Evening (Optional 1 hour):
└─ 20:00-21:00 → Watch tutorials, read docs
```

### Weekly Goals:

```
Week 1: "I can query a database!"
Week 2: "I built my first API!"
Week 3: "My frontend talks to my backend!"
Week 4: "I built a full-stack feature!"
```

---

## 🎯 Key Learning Principles

### 1. **The 80/20 Rule**
Focus on core concepts first:
- 20% of SQL knowledge handles 80% of queries
- 20% of React hooks cover 80% of use cases

### 2. **Build, Break, Fix**
```
1. Make it work (doesn't have to be perfect)
2. Break it (intentionally)
3. Fix it (learn debugging)
4. Make it better (refactor)
```

### 3. **Don't Memorize, Understand**
```
❌ Bad: Memorizing syntax
✅ Good: Understanding concepts

You can always Google syntax.
You can't Google understanding.
```

### 4. **Ask "Why?" Three Times**
```
Why do we use useState?
  → To store component state
    
    Why store component state?
      → So React knows when to re-render
      
      Why does React need to know when to re-render?
        → To update the UI when data changes
```

---

## 📝 Hands-On Exercises Summary

### Week 1 Exercises:
1. Write SQL queries (SELECT, INSERT, UPDATE, DELETE)
2. Use JOIN to combine tables
3. Create indexes for performance
4. Design a new table

### Week 2 Exercises:
5. Create new API endpoints
6. Add error handling
7. Integrate external API (yfinance)
8. Understand dependency injection

### Week 3 Exercises:
9. Build React components
10. Make API calls with axios
11. Handle loading and error states
12. Style components with CSS

### Week 4 Exercises:
13. Build complete features (portfolio tracker)
14. Add real-time updates
15. Clean up and document code
16. Test everything end-to-end

---

## 🎓 After 4 Weeks, You'll Know:

### Technical Skills:
- ✅ SQL (queries, joins, indexes)
- ✅ Python (functions, async, OOP)
- ✅ FastAPI (endpoints, dependencies)
- ✅ React (components, hooks, state)
- ✅ Docker (containers, compose)
- ✅ Git (version control)
- ✅ APIs (REST, WebSocket)

### Soft Skills:
- ✅ Reading documentation
- ✅ Debugging errors
- ✅ Breaking down problems
- ✅ Google-fu (finding answers)
- ✅ Building incrementally
- ✅ Testing systematically

### You Can:
- ✅ Build full-stack applications
- ✅ Deploy with Docker
- ✅ Read and understand code
- ✅ Debug issues systematically
- ✅ Add new features confidently
- ✅ Explain your code to others

---

## 🚀 Next Steps After This Course

### Level Up:
1. **Add Authentication**
   - User login/signup
   - JWT tokens
   - Protected routes

2. **Deploy to Production**
   - AWS, Google Cloud, or Heroku
   - Set up CI/CD
   - Monitor with logs

3. **Advanced Features**
   - Email notifications
   - Mobile app (React Native)
   - Advanced charts (TradingView)
   - Machine learning predictions

4. **Build More Projects**
   - E-commerce site
   - Social media clone
   - Project management tool
   - Your own idea!

---

## 💡 Pro Tips for Success

### 1. **Code Every Day**
Even 30 minutes is better than 0 minutes.

### 2. **Build Projects You Care About**
Modify this project to track something YOU'RE interested in:
- Crypto instead of stocks
- Sports scores
- Weather data
- Anything!

### 3. **Join Communities**
- r/learnprogramming
- Stack Overflow
- Discord coding servers
- Local meetups

### 4. **Don't Give Up!**
```
Feeling stuck is NORMAL.
Feeling confused is NORMAL.
Googling everything is NORMAL.

All developers do this.
Even seniors with 10+ years experience.
```

### 5. **Celebrate Small Wins**
```
✅ First SQL query worked!
✅ First API endpoint created!
✅ Frontend showed data!
✅ WebSocket connected!
✅ Built a complete feature!
```

---

## 📚 Additional Resources

### Documentation:
- **SQL**: https://www.sqltutorial.org/
- **Python**: https://docs.python.org/3/tutorial/
- **FastAPI**: https://fastapi.tiangolo.com/tutorial/
- **React**: https://react.dev/learn
- **Docker**: https://docs.docker.com/get-started/

### Interactive Learning:
- **SQL**: SQLZoo, HackerRank SQL
- **Python**: Codecademy, Python.org
- **React**: React Tutorial (official)
- **Full-Stack**: freeCodeCamp

### YouTube Channels:
- Traversy Media (web development)
- The Net Ninja (React, Node.js)
- Corey Schafer (Python)
- CS Dojo (fundamentals)

---

## 🎉 Final Thoughts

**You're about to learn:**
- How web applications REALLY work
- How to build something from scratch
- How to think like a developer

**Remember:**
- Every expert was once a beginner
- Mistakes are how you learn
- Google is your friend
- You got this! 💪

**Ready to start?**
```bash
cd stock-dashboard
docker-compose up --build
```

**See you on the other side! 🚀**

---

*Good luck on your coding journey!*
*You're going to do amazing things!*
