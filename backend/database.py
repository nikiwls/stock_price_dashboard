"""
Database Configuration and Models
This file demonstrates:
1. Connecting Python to MySQL
2. Defining database models (ORM)
3. Creating database sessions
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, BigInteger, DateTime, Text, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# =======================
# Database Connection
# =======================

# Get database URL from environment variable
# Format: mysql+pymysql://username:password@host:port/database
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "mysql+pymysql://stockuser:stockpass@db:3306/stockdb"
)

# Create database engine
# echo=True shows SQL queries in console (great for learning!)
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=3600,   # Recycle connections every hour
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()

# =======================
# Database Models (ORM)
# =======================

class StockPrice(Base):
    """
    ORM Model for stock_prices table
    Each class attribute maps to a database column
    """
    __tablename__ = "stock_prices"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    symbol = Column(String(10), nullable=False, index=True)
    company_name = Column(String(100))
    price = Column(DECIMAL(10, 2), nullable=False)
    change_percent = Column(DECIMAL(5, 2))
    volume = Column(BigInteger)
    market_cap = Column(BigInteger)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "symbol": self.symbol,
            "company_name": self.company_name,
            "price": float(self.price) if self.price else None,
            "change_percent": float(self.change_percent) if self.change_percent else None,
            "volume": self.volume,
            "market_cap": self.market_cap,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }


class ChatHistory(Base):
    """
    ORM Model for chat_history table
    Stores AI chatbot conversations
    """
    __tablename__ = "chat_history"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(String(50), nullable=False, index=True)
    user_message = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    stock_symbol = Column(String(10))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "user_message": self.user_message,
            "ai_response": self.ai_response,
            "stock_symbol": self.stock_symbol,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class Watchlist(Base):
    """
    ORM Model for watchlist table
    Stores user's favorite stocks
    """
    __tablename__ = "watchlist"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(50), nullable=False, default="default_user")
    symbol = Column(String(10), nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "symbol": self.symbol,
            "added_at": self.added_at.isoformat() if self.added_at else None
        }


# =======================
# Database Helper Functions
# =======================

def get_db():
    """
    Dependency function for FastAPI
    Creates a new database session for each request
    Automatically closes the session when done
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database tables
    Call this when starting the application
    """
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")


# =======================
# Example SQL Operations
# =======================

def example_sql_operations():
    """
    Demonstrates common SQL operations using SQLAlchemy
    This is for educational purposes
    """
    db = SessionLocal()
    
    try:
        # 1. INSERT - Add new stock price
        new_price = StockPrice(
            symbol="AAPL",
            company_name="Apple Inc.",
            price=175.50,
            change_percent=1.25,
            volume=50000000
        )
        db.add(new_price)
        db.commit()
        print("✅ INSERT: Added new stock price")
        
        # 2. SELECT - Query stock prices
        stock = db.query(StockPrice).filter(
            StockPrice.symbol == "AAPL"
        ).order_by(
            StockPrice.timestamp.desc()
        ).first()
        print(f"✅ SELECT: Latest AAPL price: ${stock.price}")
        
        # 3. UPDATE - Modify existing record
        stock.price = 176.00
        db.commit()
        print("✅ UPDATE: Updated stock price")
        
        # 4. DELETE - Remove old records (older than 30 days)
        # from datetime import timedelta
        # cutoff_date = datetime.utcnow() - timedelta(days=30)
        # db.query(StockPrice).filter(StockPrice.timestamp < cutoff_date).delete()
        # db.commit()
        
        # 5. JOIN - Get watchlist with latest prices
        # This is more advanced SQL
        from sqlalchemy import func
        results = db.query(
            Watchlist.symbol,
            StockPrice.price,
            StockPrice.change_percent
        ).join(
            StockPrice,
            Watchlist.symbol == StockPrice.symbol
        ).filter(
            Watchlist.user_id == "default_user"
        ).all()
        print("✅ JOIN: Watchlist with prices")
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        db.rollback()
    finally:
        db.close()