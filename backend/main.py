"""
Main FastAPI Application
This is the heart of our backend - it creates all the API endpoints
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import asyncio
import json

# Import our custom modules
from database import get_db, init_db, StockPrice, ChatHistory, Watchlist
from stock_service import StockService
from ai_service import AIService

# =======================
# Initialize FastAPI App
# =======================

app = FastAPI(
    title="Stock Dashboard API",
    description="Real-time stock prices with AI chatbot",
    version="1.0.0"
)

# Add CORS middleware (allows frontend to communicate with backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
stock_service = StockService()
ai_service = AIService()

# =======================
# Pydantic Models (Request/Response)
# =======================

class StockResponse(BaseModel):
    """Response model for stock data"""
    symbol: str
    company_name: str
    price: float
    change_percent: float
    volume: int
    market_cap: int
    timestamp: str

class ChatRequest(BaseModel):
    """Request model for chat"""
    message: str
    session_id: str
    stock_symbol: Optional[str] = None

class ChatResponse(BaseModel):
    """Response model for chat"""
    response: str
    stock_data: Optional[dict] = None
    timestamp: str

class WatchlistItem(BaseModel):
    """Model for watchlist item"""
    symbol: str
    user_id: str = "default_user"

# =======================
# Startup Event
# =======================

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    print("🚀 Starting Stock Dashboard API...")
    init_db()
    print("✅ Database initialized!")

# =======================
# Stock Endpoints
# =======================

@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "Stock Dashboard API is running!",
        "version": "1.0.0",
        "endpoints": {
            "stocks": "/api/stocks/{symbol}",
            "watchlist": "/api/watchlist",
            "chat": "/api/chat",
            "websocket": "/ws/stocks"
        }
    }

@app.get("/api/stocks/batch")
async def get_batch_stocks(symbols: str = "AAPL,GOOGL,MSFT,TSLA,AMZN"):
    """
    Get current data for multiple stocks at once (for polling)
    symbols: Comma-separated list of stock symbols
    
    This endpoint is designed for polling-based real-time updates.
    Call every 30 seconds to get fresh data without WebSocket complexity.
    """
    import asyncio
    
    symbol_list = [s.strip().upper() for s in symbols.split(",") if s.strip()]
    
    # Run blocking stock fetches in thread pool to not block event loop
    def fetch_stocks():
        return stock_service.get_multiple_stocks(symbol_list)
    
    loop = asyncio.get_event_loop()
    stocks_data = await loop.run_in_executor(None, fetch_stocks)
    
    return {
        "type": "stock_update",
        "data": stocks_data,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/stocks/search/{query}")
async def search_stocks(query: str):
    """Search for stocks by name or symbol"""
    results = stock_service.search_stocks(query)
    return {"results": results}

@app.get("/api/stocks/{symbol}", response_model=StockResponse)
async def get_stock(
    symbol: str,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = None
):
    """
    Get current stock data for a symbol
    Also saves to database in background
    """
    # Fetch from Yahoo Finance
    stock_data = stock_service.get_stock_data(symbol.upper())
    
    if not stock_data:
        raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")
    
    # Save to database in background (non-blocking)
    def save_to_db():
        new_price = StockPrice(
            symbol=stock_data['symbol'],
            company_name=stock_data['company_name'],
            price=stock_data['price'],
            change_percent=stock_data['change_percent'],
            volume=stock_data['volume'],
            market_cap=stock_data['market_cap']
        )
        db.add(new_price)
        db.commit()
    
    if background_tasks:
        background_tasks.add_task(save_to_db)
    
    return StockResponse(
        symbol=stock_data['symbol'],
        company_name=stock_data['company_name'],
        price=stock_data['price'],
        change_percent=stock_data['change_percent'],
        volume=stock_data['volume'],
        market_cap=stock_data['market_cap'],
        timestamp=stock_data['timestamp'].isoformat()
    )

@app.get("/api/stocks/{symbol}/history")
async def get_stock_history(
    symbol: str,
    period: str = "1d",
    interval: str = "5m"
):
    """
    Get historical stock data
    period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max
    interval: 1m, 5m, 15m, 30m, 1h, 1d, 1wk, 1mo
    """
    history = stock_service.get_historical_data(symbol.upper(), period, interval)
    return {
        "symbol": symbol.upper(),
        "period": period,
        "interval": interval,
        "data": history
    }

# =======================
# Watchlist Endpoints
# =======================

@app.get("/api/watchlist")
async def get_watchlist(
    user_id: str = "default_user",
    db: Session = Depends(get_db)
):
    """Get user's watchlist with current prices"""
    import asyncio
    
    # Get watchlist from database
    watchlist_items = db.query(Watchlist).filter(
        Watchlist.user_id == user_id
    ).all()
    
    # Get current prices for each stock (run in thread pool to avoid blocking)
    symbols = [item.symbol for item in watchlist_items]
    
    if not symbols:
        return {"user_id": user_id, "stocks": []}
    
    def fetch_stocks():
        return stock_service.get_multiple_stocks(symbols)
    
    loop = asyncio.get_event_loop()
    stocks_data = await loop.run_in_executor(None, fetch_stocks)
    
    return {
        "user_id": user_id,
        "stocks": stocks_data
    }

@app.post("/api/watchlist")
async def add_to_watchlist(
    item: WatchlistItem,
    db: Session = Depends(get_db)
):
    """Add stock to watchlist"""
    # Check if already exists
    exists = db.query(Watchlist).filter(
        Watchlist.user_id == item.user_id,
        Watchlist.symbol == item.symbol.upper()
    ).first()
    
    if exists:
        raise HTTPException(status_code=400, detail="Stock already in watchlist")
    
    # Add to watchlist
    new_item = Watchlist(
        user_id=item.user_id,
        symbol=item.symbol.upper()
    )
    db.add(new_item)
    db.commit()
    
    return {"message": f"Added {item.symbol} to watchlist"}

@app.delete("/api/watchlist/{symbol}")
async def remove_from_watchlist(
    symbol: str,
    user_id: str = "default_user",
    db: Session = Depends(get_db)
):
    """Remove stock from watchlist"""
    item = db.query(Watchlist).filter(
        Watchlist.user_id == user_id,
        Watchlist.symbol == symbol.upper()
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Stock not in watchlist")
    
    db.delete(item)
    db.commit()
    
    return {"message": f"Removed {symbol} from watchlist"}

# =======================
# Chat Endpoints
# =======================

@app.post("/api/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Chat with AI about stocks
    """
    # Get stock data if symbol provided
    stock_data = None
    if request.stock_symbol:
        stock_data = stock_service.get_stock_data(request.stock_symbol.upper())
    else:
        # Try to extract symbol from message
        extracted_symbol = ai_service.extract_stock_symbol(request.message)
        if extracted_symbol:
            stock_data = stock_service.get_stock_data(extracted_symbol)
    
    # Get chat history for context
    history = db.query(ChatHistory).filter(
        ChatHistory.session_id == request.session_id
    ).order_by(ChatHistory.created_at.desc()).limit(5).all()
    
    history_list = [h.to_dict() for h in reversed(history)]
    
    # Get AI response
    ai_response = await ai_service.chat(
        user_message=request.message,
        stock_data=stock_data,
        chat_history=history_list
    )
    
    # Save to database
    chat_record = ChatHistory(
        session_id=request.session_id,
        user_message=request.message,
        ai_response=ai_response,
        stock_symbol=stock_data['symbol'] if stock_data else None
    )
    db.add(chat_record)
    db.commit()
    
    return ChatResponse(
        response=ai_response,
        stock_data=stock_data,
        timestamp=datetime.utcnow().isoformat()
    )

@app.get("/api/chat/history/{session_id}")
async def get_chat_history(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Get chat history for a session"""
    history = db.query(ChatHistory).filter(
        ChatHistory.session_id == session_id
    ).order_by(ChatHistory.created_at.asc()).all()
    
    return {
        "session_id": session_id,
        "messages": [h.to_dict() for h in history]
    }

# =======================
# WebSocket for Real-Time Updates
# =======================

class ConnectionManager:
    """Manages WebSocket connections"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        """Send message to all connected clients"""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()

@app.websocket("/ws/stocks")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time stock updates
    Clients can subscribe to specific stocks
    Updates every 30 seconds to avoid rate limiting
    """
    await manager.connect(websocket)
    
    # Default stocks to track
    tracked_symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
    
    try:
        while True:
            # Check if connection is still open before sending
            if websocket.client_state.name != "CONNECTED":
                break
            
            # Send updates every 30 seconds (was 5 seconds)
            # This reduces API calls to Yahoo Finance
            try:
                stocks_data = stock_service.get_multiple_stocks(tracked_symbols)
                
                await websocket.send_json({
                    "type": "stock_update",
                    "data": stocks_data,
                    "timestamp": datetime.utcnow().isoformat()
                })
            except Exception as send_error:
                print(f"Error sending stock data: {send_error}")
                break
            
            # Wait 30 seconds before next update
            await asyncio.sleep(30)
            
    except WebSocketDisconnect:
        print("Client disconnected from WebSocket")
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        # Always ensure cleanup happens
        if websocket in manager.active_connections:
            manager.disconnect(websocket)

# =======================
# Health Check
# =======================

@app.get("/health")
async def health_check():
    """Health check endpoint for Docker"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)