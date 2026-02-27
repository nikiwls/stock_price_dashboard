# 📋 Stock Dashboard - Quick Reference

## 🚀 Start & Stop

```bash
# Start all services
docker-compose up --build

# Start in background
docker-compose up -d

# Stop all services
docker-compose down

# Restart specific service
docker-compose restart backend
docker-compose restart frontend
```

## 📡 API Testing

### Stock Data

```bash
# Get stock details
curl http://localhost:8000/api/stocks/AAPL

# Get price history (periods: 1d, 5d, 1mo, 3mo, 1y, 5y)
curl "http://localhost:8000/api/stocks/AAPL/history?period=1d"

# Search stocks
curl http://localhost:8000/api/stocks/search/apple

# Get market indices
curl http://localhost:8000/api/market/indices

# Get trending stocks
curl http://localhost:8000/api/market/trending
```

### Watchlist

```bash
# Get watchlist
curl http://localhost:8000/api/watchlist

# Add to watchlist
curl -X POST http://localhost:8000/api/watchlist \
  -H "Content-Type: application/json" \
  -d '{"symbol": "TSLA"}'

# Remove from watchlist
curl -X DELETE http://localhost:8000/api/watchlist/TSLA
```

### AI Chat

```bash
# Send chat message
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is AAPL?", "session_id": "test123"}'

# Chat with stock context
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How is this stock performing?", "session_id": "test123", "stock_symbol": "NVDA"}'
```

## 🗄️ Database

### Connect to MySQL

```bash
docker exec -it stock_db mysql -u stockuser -pstockpass stockdb
```

### Common Queries

```sql
-- Show all tables
SHOW TABLES;

-- View recent stock prices
SELECT * FROM stock_prices ORDER BY timestamp DESC LIMIT 10;

-- View watchlist
SELECT * FROM watchlist;

-- View chat history
SELECT * FROM chat_history ORDER BY created_at DESC LIMIT 10;

-- Count records per symbol
SELECT symbol, COUNT(*) FROM stock_prices GROUP BY symbol;
```

## 🤖 Ollama (AI)

```bash
# Start Ollama service
brew services start ollama

# Stop Ollama service
brew services stop ollama

# List installed models
ollama list

# Download model
ollama pull qwen2.5:0.5b

# Test model
ollama run qwen2.5:0.5b "Hello"

# Delete model
ollama rm qwen2.5:0.5b
```

## 🐳 Docker

### Container Management

```bash
# List running containers
docker ps

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db

# Execute command in container
docker exec -it stock_backend bash
docker exec -it stock_frontend sh

# View resource usage
docker stats
```

### Cleanup

```bash
# Remove all containers and volumes
docker-compose down -v

# Remove unused images
docker image prune -a

# Full cleanup
docker system prune -a
```

## 🔧 Troubleshooting

### Port in Use

```bash
# Find process using port
lsof -i :3000
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Reset Everything

```bash
# Stop and remove all data
docker-compose down -v

# Rebuild from scratch
docker-compose up --build
```

### Check Service Health

```bash
# Backend health
curl http://localhost:8000/health

# Database ping
docker exec stock_db mysqladmin ping -h localhost
```

## 🌐 Access URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| API Docs (ReDoc) | http://localhost:8000/redoc |
