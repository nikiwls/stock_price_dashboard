# 📋 Stock Dashboard - Quick Reference Cheat Sheet

## 🚀 Quick Start Commands

```bash
# Start everything
docker-compose up --build

# Start in background
docker-compose up -d

# Stop everything
docker-compose down

# View logs (all services)
docker-compose logs -f

# View logs (specific service)
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

---

## 🗄️ SQL Cheat Sheet

### Common Queries

```sql
-- View all tables
SHOW TABLES;

-- View table structure
DESCRIBE stock_prices;

-- Get latest stock prices
SELECT * FROM stock_prices 
ORDER BY timestamp DESC 
LIMIT 10;

-- Get stock history for specific symbol
SELECT * FROM stock_prices 
WHERE symbol = 'AAPL' 
AND timestamp > DATE_SUB(NOW(), INTERVAL 1 DAY)
ORDER BY timestamp DESC;

-- Get chat history
SELECT * FROM chat_history 
ORDER BY created_at DESC 
LIMIT 20;

-- Get watchlist with latest prices
SELECT w.symbol, sp.price, sp.change_percent
FROM watchlist w
LEFT JOIN (
    SELECT symbol, price, change_percent
    FROM stock_prices
    WHERE (symbol, timestamp) IN (
        SELECT symbol, MAX(timestamp)
        FROM stock_prices
        GROUP BY symbol
    )
) sp ON w.symbol = sp.symbol;

-- Count records by symbol
SELECT symbol, COUNT(*) as count
FROM stock_prices
GROUP BY symbol
ORDER BY count DESC;

-- Average price by symbol
SELECT symbol, 
       AVG(price) as avg_price,
       MIN(price) as min_price,
       MAX(price) as max_price
FROM stock_prices
WHERE timestamp > DATE_SUB(NOW(), INTERVAL 7 DAY)
GROUP BY symbol;
```

### Database Access

```bash
# Connect to MySQL
docker exec -it stock_db mysql -u stockuser -pstockpass stockdb

# Or use connection string
mysql -h localhost -P 3306 -u stockuser -pstockpass stockdb
```

---

## 🐍 FastAPI Cheat Sheet

### Testing Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Get stock data
curl http://localhost:8000/api/stocks/AAPL

# Get stock history
curl "http://localhost:8000/api/stocks/AAPL/history?period=1d&interval=5m"

# Get watchlist
curl http://localhost:8000/api/watchlist

# Add to watchlist
curl -X POST http://localhost:8000/api/watchlist \
  -H "Content-Type: application/json" \
  -d '{"symbol": "TSLA"}'

# Remove from watchlist
curl -X DELETE http://localhost:8000/api/watchlist/TSLA

# Chat with AI
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is Apple stock?",
    "session_id": "test123",
    "stock_symbol": "AAPL"
  }'

# Search stocks
curl http://localhost:8000/api/stocks/search/apple
```

### Interactive API Docs

Access at: http://localhost:8000/docs

---

## ⚛️ React Development

### Useful npm Commands

```bash
# Install dependencies
docker-compose exec frontend npm install

# Add new package
docker-compose exec frontend npm install package-name

# Clear cache
docker-compose exec frontend npm cache clean --force

# Rebuild node_modules
docker-compose exec frontend rm -rf node_modules
docker-compose exec frontend npm install
```

### Component Structure

```javascript
// State
const [data, setData] = useState(initialValue);

// Effect (on mount)
useEffect(() => {
    // code
}, []);

// Effect (on dependency change)
useEffect(() => {
    // code
}, [dependency]);

// API call
const fetchData = async () => {
    const response = await axios.get(url);
    setData(response.data);
};

// Event handler
const handleClick = () => {
    // code
};
```

---

## 🐳 Docker Cheat Sheet

### Container Management

```bash
# List running containers
docker ps

# List all containers
docker ps -a

# Stop a container
docker stop stock_backend

# Start a container
docker start stock_backend

# Restart a container
docker restart stock_backend

# Remove a container
docker rm stock_backend

# View container logs
docker logs -f stock_backend

# Execute command in container
docker exec -it stock_backend bash

# View container resource usage
docker stats
```

### Image Management

```bash
# List images
docker images

# Remove image
docker rmi image_name

# Remove all unused images
docker image prune -a

# Build image
docker build -t my-image .
```

### Network Management

```bash
# List networks
docker network ls

# Inspect network
docker network inspect stock-dashboard_default

# Create network
docker network create my-network
```

### Volume Management

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect stock-dashboard_mysql_data

# Remove volume
docker volume rm volume_name

# Remove all unused volumes
docker volume prune
```

---

## 🔧 Common Issues & Solutions

### Issue: Port already in use

```bash
# Find process using port 3000
lsof -i :3000

# Kill process
kill -9 <PID>

# Or change port in docker-compose.yml
ports:
  - "3001:3000"  # Use 3001 instead
```

### Issue: Database connection failed

```bash
# Wait for database to be ready
docker-compose logs db

# Restart database
docker-compose restart db

# Reset database
docker-compose down -v
docker-compose up --build
```

### Issue: Frontend won't start

```bash
# Check logs
docker-compose logs frontend

# Rebuild frontend
docker-compose up --build frontend

# Clear npm cache
docker-compose exec frontend npm cache clean --force
```

### Issue: Changes not reflecting

```bash
# Rebuild containers
docker-compose up --build

# For frontend hot-reload issues
docker-compose restart frontend
```

---

## 📊 Monitoring & Debugging

### Check Service Health

```bash
# Backend health
curl http://localhost:8000/health

# Database health
docker exec stock_db mysqladmin ping -h localhost

# Container status
docker ps
```

### View Resource Usage

```bash
# All containers
docker stats

# Specific container
docker stats stock_backend
```

### Database Debugging

```bash
# Connect to database
docker exec -it stock_db mysql -u stockuser -pstockpass stockdb

# Show processlist
SHOW PROCESSLIST;

# Show table sizes
SELECT 
    table_name AS 'Table',
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)'
FROM information_schema.TABLES
WHERE table_schema = 'stockdb'
ORDER BY (data_length + index_length) DESC;
```

---

## 🎯 Performance Tips

### Backend Optimization

```python
# Use background tasks for slow operations
@app.post("/data")
async def process(background_tasks: BackgroundTasks):
    background_tasks.add_task(slow_operation)
    return {"status": "processing"}

# Cache expensive operations
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_function(param):
    # expensive operation
    return result

# Use database indexing
CREATE INDEX idx_symbol_timestamp 
ON stock_prices(symbol, timestamp);
```

### Frontend Optimization

```javascript
// Memoize expensive computations
const expensiveValue = useMemo(() => {
    return computeExpensive(data);
}, [data]);

// Memoize components
const MemoizedComponent = React.memo(Component);

// Lazy load components
const LazyComponent = lazy(() => import('./Component'));
```

---

## 📚 Learning Resources

### SQL
- SQLZoo: https://sqlzoo.net/
- MySQL Tutorial: https://dev.mysql.com/doc/

### FastAPI
- Official Docs: https://fastapi.tiangolo.com/
- Tutorial: https://fastapi.tiangolo.com/tutorial/

### React
- Official Docs: https://react.dev/
- Tutorial: https://react.dev/learn

### Docker
- Get Started: https://docs.docker.com/get-started/
- Compose: https://docs.docker.com/compose/

---

## 🎓 Next Steps

1. ✅ Complete the basic project
2. ✅ Add user authentication
3. ✅ Implement portfolio tracking
4. ✅ Add technical indicators
5. ✅ Deploy to production
6. ✅ Add to your portfolio
7. ✅ Share on GitHub

---

**Quick Links:**
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- GitHub: Add your repo link here

**Need Help?**
- Check README.md for detailed instructions
- See TEACHING_GUIDE.md for learning path
- Review code comments for explanations

Happy coding! 🚀