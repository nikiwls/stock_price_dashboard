# 📚 Full-Stack Development Teaching Guide

## Course Overview: Building a Real-Time Stock Dashboard

**Duration:** 4-6 hours of hands-on learning  
**Skill Level:** Beginner to Intermediate  
**Prerequisites:** Basic programming knowledge (any language)

---

## 🎯 Learning Path

### Module 1: Introduction to Full-Stack Architecture (30 min)

**Concepts:**
- What is full-stack development?
- Client-Server architecture
- Request-Response cycle
- RESTful API design

**Practical Exercise:**
1. Draw the architecture diagram on a whiteboard
2. Explain data flow: User clicks → Frontend → Backend → Database → Response
3. Discuss why we separate frontend and backend

**Key Takeaways:**
- Frontend = What users see (React)
- Backend = Business logic (FastAPI)
- Database = Data storage (MySQL)
- Each layer has a specific responsibility

---

### Module 2: SQL & Database Design (60 min)

**Topics:**
1. Database fundamentals
2. SQL syntax and operations
3. Table relationships
4. Indexing for performance

**Hands-On Lab:**

```sql
-- Exercise 1: Create a simple table
CREATE TABLE students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    grade DECIMAL(4,2)
);

-- Exercise 2: Insert data
INSERT INTO students (name, grade) VALUES ('Alice', 95.5);

-- Exercise 3: Query data
SELECT * FROM students WHERE grade > 90;

-- Exercise 4: Update data
UPDATE students SET grade = 96.0 WHERE name = 'Alice';

-- Exercise 5: Join tables
SELECT s.name, c.course_name
FROM students s
JOIN enrollments e ON s.id = e.student_id
JOIN courses c ON e.course_id = c.id;
```

**Common Mistakes to Avoid:**
- ❌ Not using PRIMARY KEY
- ❌ Missing indexes on frequently queried columns
- ❌ Using SELECT * in production
- ❌ Not sanitizing user input (SQL injection)

**Best Practices:**
- ✅ Use meaningful table and column names
- ✅ Define proper data types
- ✅ Add indexes for performance
- ✅ Use foreign keys for relationships
- ✅ Always use prepared statements

---

### Module 3: Python Backend with FastAPI (90 min)

**Part A: SQLAlchemy ORM (30 min)**

**Why use ORM?**
- Write Python instead of SQL
- Type safety
- Easier to maintain
- Prevents SQL injection

**Example Comparison:**

```python
# Without ORM - Raw SQL (dangerous!)
cursor.execute(f"SELECT * FROM users WHERE name = '{user_input}'")
# ☠️ SQL Injection vulnerability!

# With ORM - Safe and clean
user = db.query(User).filter(User.name == user_input).first()
# ✅ Safe, readable, maintainable
```

**Part B: FastAPI Fundamentals (30 min)**

**Key Concepts:**
1. **Path Parameters:** `/api/stocks/{symbol}`
2. **Query Parameters:** `/api/stocks?limit=10`
3. **Request Body:** POST data
4. **Response Models:** Type-safe responses

**Interactive Demo:**

```python
# Simple endpoint
@app.get("/hello")
async def hello():
    return {"message": "Hello World"}

# Path parameter
@app.get("/user/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}

# Request body
@app.post("/create")
async def create_item(item: Item):
    return {"created": item.name}
```

**Part C: Database Integration (30 min)**

**Teaching Flow:**
1. Show how to define models
2. Demonstrate CRUD operations
3. Explain dependency injection
4. Practice error handling

```python
# Dependency Injection Pattern
@app.get("/items")
def get_items(db: Session = Depends(get_db)):
    # db is automatically provided by FastAPI
    items = db.query(Item).all()
    return items
```

---

### Module 4: Docker & Containerization (45 min)

**Metaphor:** "Docker is like a moving box"
- Everything you need in one package
- Works the same everywhere
- Easy to transport and deploy

**Key Commands Students Must Know:**

```bash
# Build and start
docker-compose up --build

# Stop services
docker-compose down

# View logs
docker-compose logs -f [service-name]

# Execute command in container
docker exec -it [container-name] bash

# List running containers
docker ps

# Remove all containers
docker-compose down -v
```

**Common Issues & Solutions:**

| Problem | Solution |
|---------|----------|
| Port already in use | Stop other services or change port |
| Container won't start | Check logs: `docker-compose logs` |
| Database connection failed | Wait for healthcheck to pass |
| Changes not reflected | Rebuild: `docker-compose up --build` |

---

### Module 5: React Frontend Development (90 min)

**Part A: React Basics (30 min)**

**Core Concepts:**
1. Components - Building blocks
2. Props - Passing data down
3. State - Component memory
4. Effects - Side effects

**Simple Example:**

```javascript
// Component
function StockCard({ symbol, price }) {
    const [favorite, setFavorite] = useState(false);
    
    return (
        <div>
            <h3>{symbol}: ${price}</h3>
            <button onClick={() => setFavorite(!favorite)}>
                {favorite ? '❤️' : '🤍'}
            </button>
        </div>
    );
}
```

**Part B: API Integration (30 min)**

**Teaching Points:**
- Async/await for API calls
- Loading states
- Error handling
- Data transformation

```javascript
const [data, setData] = useState(null);
const [loading, setLoading] = useState(true);
const [error, setError] = useState(null);

useEffect(() => {
    async function fetchData() {
        try {
            const response = await fetch('/api/stocks/AAPL');
            const data = await response.json();
            setData(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }
    fetchData();
}, []);
```

**Part C: Real-Time Updates (30 min)**

**WebSocket Explanation:**
- Regular HTTP: Request → Response (one-way)
- WebSocket: Persistent connection (two-way)

```javascript
// WebSocket connection
const ws = new WebSocket('ws://localhost:8000/ws/stocks');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    updateStockPrices(data);
};
```

---

## 🎓 Teaching Methodology

### 1. Explain → Demonstrate → Practice

**For each topic:**
1. **Explain** the concept (5 min)
2. **Demonstrate** with live coding (10 min)
3. **Practice** with guided exercises (15 min)
4. **Review** common mistakes (5 min)

### 2. Build Incrementally

**Week 1:** Database & SQL
- Design schema
- Write queries
- Understand relationships

**Week 2:** Backend API
- Setup FastAPI
- Create endpoints
- Connect to database

**Week 3:** Frontend
- Build React components
- Connect to API
- Add styling

**Week 4:** Integration
- Docker setup
- WebSocket
- Deployment

### 3. Common Student Questions

**Q: "Why do we need three separate containers?"**  
A: Separation of concerns. Database can be upgraded independently, backend can scale, frontend can be deployed to CDN.

**Q: "Can't we just use raw SQL instead of ORM?"**  
A: You can, but ORM provides type safety, prevents SQL injection, and makes code more maintainable.

**Q: "Why FastAPI instead of Flask/Django?"**  
A: FastAPI is modern, fast, has automatic API docs, and built-in async support. Perfect for APIs.

**Q: "Do I need to learn both class components and hooks?"**  
A: Focus on hooks (modern React). Class components are legacy.

**Q: "How do I deploy this?"**  
A: Docker makes deployment easy. Can use AWS ECS, Google Cloud Run, or any platform that supports Docker.

---

## 🔍 Debugging Tips for Students

### Backend Issues

```bash
# Check if backend is running
curl http://localhost:8000/health

# View backend logs
docker-compose logs -f backend

# Connect to database
docker exec -it stock_db mysql -u stockuser -pstockpass stockdb

# Test database connection
docker exec -it stock_backend python -c "from database import engine; print(engine)"
```

### Frontend Issues

```bash
# Check React errors
docker-compose logs -f frontend

# Rebuild node_modules
docker-compose exec frontend rm -rf node_modules
docker-compose exec frontend npm install

# Check API connection
curl http://localhost:3000
```

### Network Issues

```bash
# Check container network
docker network ls
docker network inspect stock-dashboard_default

# Test connectivity between containers
docker exec -it stock_backend ping db
```

---

## 📊 Assessment & Exercises

### Beginner Level

**Exercise 1: Modify Database Schema**
- Add a "sector" field to stock_prices table
- Update the ORM model
- Modify the API to return sector info

**Exercise 2: Create New Endpoint**
- Add `/api/stocks/{symbol}/statistics` endpoint
- Return average price, volume, etc.

**Exercise 3: Frontend Enhancement**
- Add a "favorite" button to each stock
- Store favorites in localStorage

### Intermediate Level

**Exercise 4: Implement Stock Comparison**
- Compare two stocks side by side
- Create a comparison API endpoint
- Build UI for comparison view

**Exercise 5: Add Email Alerts**
- When stock price crosses threshold
- Use background tasks in FastAPI
- Store alert preferences in database

**Exercise 6: Portfolio Tracker**
- Track bought stocks and quantities
- Calculate profit/loss
- Show portfolio performance chart

### Advanced Level

**Exercise 7: User Authentication**
- Implement JWT authentication
- Create user registration/login
- Protect API endpoints

**Exercise 8: Real-Time Notifications**
- Push notifications for price changes
- Use WebSocket for alerts
- Add browser notification API

**Exercise 9: Technical Analysis**
- Calculate moving averages (MA, EMA)
- Add RSI, MACD indicators
- Display on advanced charts

---

## 🎯 Project Extensions

After completing the basic project, students can:

1. **Add More Data Sources**
   - News articles (NewsAPI)
   - Social sentiment (Twitter API)
   - Crypto prices (CoinGecko)

2. **Advanced Features**
   - Stock screener
   - Portfolio optimization
   - Backtesting strategies

3. **Improve UI/UX**
   - Mobile responsive design
   - Dark/light theme toggle
   - Accessibility (ARIA labels)

4. **Performance Optimization**
   - Redis caching
   - Database query optimization
   - Frontend lazy loading

5. **Production Deployment**
   - AWS/GCP deployment
   - CI/CD pipeline
   - Monitoring & logging

---

## 📚 Additional Resources

### Books
- "Learning SQL" by Alan Beaulieu
- "FastAPI" by Bill Lubanovic
- "Learning React" by Alex Banks & Eve Porcello

### Online Courses
- freeCodeCamp SQL Course
- FastAPI Tutorial on YouTube
- React Official Tutorial

### Practice Platforms
- LeetCode (SQL problems)
- HackerRank (Database challenges)
- Frontend Mentor (React projects)

---

## 🎉 Conclusion

By completing this project, students will have:
- ✅ Built a real-world full-stack application
- ✅ Mastered SQL and database design
- ✅ Learned modern backend development
- ✅ Created responsive frontends
- ✅ Understood containerization with Docker
- ✅ Integrated AI capabilities
- ✅ Practiced industry best practices

**Next Steps:**
1. Deploy the application
2. Add it to your portfolio
3. Share on GitHub
4. Build similar projects
5. Apply for full-stack positions!

---

**Remember:** The best way to learn is by building. Make mistakes, debug, and iterate!

Good luck! 🚀