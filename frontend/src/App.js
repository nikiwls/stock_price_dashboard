import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { TrendingUp, TrendingDown, Search, MessageCircle, X, Send, Plus, Trash2, BarChart3 } from 'lucide-react';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  // State management
  const [watchlist, setWatchlist] = useState([]);
  const [selectedStock, setSelectedStock] = useState(null);
  const [stockHistory, setStockHistory] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  
  // Chat state
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [chatMessages, setChatMessages] = useState([]);
  const [chatInput, setChatInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [addingStock, setAddingStock] = useState(null); // Track which stock is being added
  const chatEndRef = useRef(null);
  
  // Session ID for chat
  const [sessionId] = useState(`session_${Date.now()}`);

  // Polling interval ref for real-time updates
  const pollingIntervalRef = useRef(null);

  // Load watchlist on mount
  useEffect(() => {
    loadWatchlist();
    startPolling();
    
    return () => {
      // Clear polling interval on unmount
      if (pollingIntervalRef.current) {
        clearInterval(pollingIntervalRef.current);
      }
    };
  }, []);

  // Auto-scroll chat to bottom
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatMessages]);

  // Ref to store current watchlist for polling (avoids closure issues)
  const watchlistRef = useRef(watchlist);
  
  // Keep ref in sync with state
  useEffect(() => {
    watchlistRef.current = watchlist;
  }, [watchlist]);

  // Fetch stock updates via HTTP polling (more reliable than WebSocket)
  const fetchStockUpdates = async () => {
    try {
      const currentWatchlist = watchlistRef.current;
      const symbols = currentWatchlist.map(s => s.symbol).join(',');
      if (!symbols) return; // No stocks to fetch
      
      const response = await axios.get(`${API_URL}/api/stocks/batch?symbols=${symbols}`);
      if (response.data.type === 'stock_update') {
        updateWatchlistPrices(response.data.data);
      }
    } catch (error) {
      console.error('Error fetching stock updates:', error.message);
      // Polling will automatically retry on next interval
    }
  };

  // Start polling for real-time updates
  const startPolling = () => {
    // Clear any existing interval
    if (pollingIntervalRef.current) {
      clearInterval(pollingIntervalRef.current);
    }
    
    // Initial fetch
    fetchStockUpdates();
    
    // Poll every 30 seconds
    pollingIntervalRef.current = setInterval(fetchStockUpdates, 30000);
    console.log('Stock polling started (30s interval)');
  };

  // Update watchlist with real-time prices
  const updateWatchlistPrices = (newData) => {
    setWatchlist(prevWatchlist => {
      const updatedList = [...prevWatchlist];
      newData.forEach(newStock => {
        const index = updatedList.findIndex(s => s.symbol === newStock.symbol);
        if (index !== -1) {
          updatedList[index] = { ...updatedList[index], ...newStock };
        }
      });
      return updatedList;
    });
  };

  // Load watchlist from API
  const loadWatchlist = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/watchlist`);
      setWatchlist(response.data.stocks);
    } catch (error) {
      console.error('Error loading watchlist:', error);
    }
  };

  // Restart polling when watchlist changes (to fetch correct symbols)
  useEffect(() => {
    if (watchlist.length > 0) {
      startPolling();
    }
  }, [watchlist.length]); // Only restart when watchlist size changes

  // Select a stock to view details
  const selectStock = async (symbol) => {
    try {
      const response = await axios.get(`${API_URL}/api/stocks/${symbol}`);
      setSelectedStock(response.data);
      
      // Load historical data
      const historyResponse = await axios.get(`${API_URL}/api/stocks/${symbol}/history?period=1d&interval=5m`);
      setStockHistory(historyResponse.data.data);
    } catch (error) {
      console.error('Error selecting stock:', error);
    }
  };

  // Debounced search ref
  const searchTimeoutRef = useRef(null);

  // Search stocks with debouncing
  const handleSearch = (query) => {
    setSearchQuery(query);
    
    // Clear previous timeout
    if (searchTimeoutRef.current) {
      clearTimeout(searchTimeoutRef.current);
    }
    
    if (query.length >= 2) {  // Only search if 2+ characters
      // Debounce: wait 300ms before searching
      searchTimeoutRef.current = setTimeout(async () => {
        try {
          const response = await axios.get(`${API_URL}/api/stocks/search/${query}`);
          setSearchResults(response.data.results);
        } catch (error) {
          console.error('Error searching stocks:', error);
        }
      }, 300);
    } else {
      setSearchResults([]);
    }
  };

  // Add stock to watchlist with optimistic UI update
  const addToWatchlist = async (symbol) => {
    // Check if already in local watchlist state first (faster)
    if (watchlist.some(s => s.symbol.toUpperCase() === symbol.toUpperCase())) {
      alert(`${symbol} is already in your watchlist!`);
      setSearchQuery('');
      setSearchResults([]);
      return;
    }
    
    // Set loading state
    setAddingStock(symbol);
    
    // Optimistic UI: Clear search immediately for faster feel
    setSearchQuery('');
    setSearchResults([]);
    
    try {
      await axios.post(`${API_URL}/api/watchlist`, { symbol });
      // Reload to get full stock data
      await loadWatchlist();
    } catch (error) {
      console.error('Error adding to watchlist:', error);
      
      // Handle "already exists" error from server
      if (error.response && error.response.status === 400) {
        alert(`${symbol} is already in your watchlist!`);
      } else {
        alert(`Failed to add ${symbol}. Please try again.`);
      }
    } finally {
      setAddingStock(null);
    }
  };

  // Remove stock from watchlist
  const removeFromWatchlist = async (symbol) => {
    try {
      await axios.delete(`${API_URL}/api/watchlist/${symbol}`);
      loadWatchlist();
      if (selectedStock?.symbol === symbol) {
        setSelectedStock(null);
      }
    } catch (error) {
      console.error('Error removing from watchlist:', error);
    }
  };

  // Send chat message
  const sendChatMessage = async () => {
    if (!chatInput.trim()) return;

    const userMessage = chatInput;
    setChatInput('');
    setIsLoading(true);

    // Add user message to chat
    setChatMessages(prev => [...prev, { role: 'user', content: userMessage }]);

    try {
      const response = await axios.post(`${API_URL}/api/chat`, {
        message: userMessage,
        session_id: sessionId,
        stock_symbol: selectedStock?.symbol
      });

      // Add AI response to chat
      setChatMessages(prev => [...prev, { 
        role: 'assistant', 
        content: response.data.response 
      }]);
    } catch (error) {
      console.error('Error sending chat message:', error);
      setChatMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'Sorry, I encountered an error. Please try again.' 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <BarChart3 size={32} />
            <h1>AI StockPulse</h1>
          </div>
          <div className="search-bar">
            <Search size={20} />
            <input
              type="text"
              placeholder="Search stocks (e.g., AAPL, GOOGL)..."
              value={searchQuery}
              onChange={(e) => handleSearch(e.target.value)}
            />
          </div>
        </div>
        
        {/* Search Results */}
        {searchResults.length > 0 && (
          <div className="search-results">
            {searchResults.map(stock => (
              <div 
                key={stock.symbol} 
                className={`search-result-item ${addingStock === stock.symbol ? 'adding' : ''}`}
              >
                <div className="stock-info-text">
                  <strong>{stock.symbol}</strong>
                  <span>{stock.name}</span>
                </div>
                <button 
                  className="add-stock-btn"
                  onClick={(e) => {
                    e.stopPropagation();
                    addToWatchlist(stock.symbol);
                  }}
                  disabled={addingStock === stock.symbol}
                >
                  {addingStock === stock.symbol ? (
                    <span className="loading-spinner"></span>
                  ) : (
                    <>
                      <Plus size={16} />
                      <span>Add</span>
                    </>
                  )}
                </button>
              </div>
            ))}
          </div>
        )}
      </header>

      {/* Main Content */}
      <div className="main-content">
        {/* Watchlist Sidebar */}
        <aside className="watchlist">
          <h2>Your Watchlist</h2>
          <div className="watchlist-items">
            {watchlist.map(stock => (
              <div 
                key={stock.symbol}
                className={`watchlist-item ${selectedStock?.symbol === stock.symbol ? 'active' : ''}`}
                onClick={() => selectStock(stock.symbol)}
              >
                <div className="stock-info">
                  <div className="stock-header">
                    <strong>{stock.symbol}</strong>
                    <button 
                      className="remove-btn"
                      onClick={(e) => {
                        e.stopPropagation();
                        removeFromWatchlist(stock.symbol);
                      }}
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                  <span className="company-name">{stock.company_name}</span>
                </div>
                <div className="stock-price">
                  <strong>${stock.price?.toFixed(2)}</strong>
                  <span className={stock.change_percent >= 0 ? 'positive' : 'negative'}>
                    {stock.change_percent >= 0 ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
                    {stock.change_percent?.toFixed(2)}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        </aside>

        {/* Stock Details */}
        <main className="stock-details">
          {selectedStock ? (
            <>
              <div className="stock-header-section">
                <div>
                  <h1>{selectedStock.company_name}</h1>
                  <p className="symbol">{selectedStock.symbol}</p>
                </div>
                <div className="price-section">
                  <h2>${selectedStock.price?.toFixed(2)}</h2>
                  <span className={selectedStock.change_percent >= 0 ? 'change positive' : 'change negative'}>
                    {selectedStock.change_percent >= 0 ? '+' : ''}
                    {selectedStock.change_percent?.toFixed(2)}%
                  </span>
                </div>
              </div>

              {/* Chart */}
              {stockHistory.length > 0 && (
                <div className="chart-container">
                  <h3>Price History (Today)</h3>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={stockHistory}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                      <XAxis 
                        dataKey="timestamp" 
                        tickFormatter={(time) => new Date(time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                        stroke="#888"
                      />
                      <YAxis stroke="#888" domain={['auto', 'auto']} />
                      <Tooltip 
                        contentStyle={{ backgroundColor: '#1a1a2e', border: '1px solid #333' }}
                        labelFormatter={(time) => new Date(time).toLocaleString()}
                      />
                      <Line 
                        type="monotone" 
                        dataKey="close" 
                        stroke="#00d4ff" 
                        strokeWidth={2}
                        dot={false}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              )}

              {/* Stock Stats */}
              <div className="stock-stats">
                <div className="stat-item">
                  <span className="stat-label">Volume</span>
                  <span className="stat-value">{selectedStock.volume?.toLocaleString()}</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">Market Cap</span>
                  <span className="stat-value">
                    ${(selectedStock.market_cap / 1e9).toFixed(2)}B
                  </span>
                </div>
              </div>
            </>
          ) : (
            <div className="empty-state">
              <BarChart3 size={64} />
              <h2>Select a stock from your watchlist</h2>
              <p>Or search for a new stock to add</p>
            </div>
          )}
        </main>
      </div>

      {/* AI Chat Button */}
      <button 
        className="chat-button"
        onClick={() => setIsChatOpen(!isChatOpen)}
      >
        {isChatOpen ? <X size={24} /> : <MessageCircle size={24} />}
      </button>

      {/* AI Chat Panel */}
      {isChatOpen && (
        <div className="chat-panel">
          <div className="chat-header">
            <h3>AI Stock Assistant</h3>
            <button onClick={() => setIsChatOpen(false)}>
              <X size={20} />
            </button>
          </div>
          
          <div className="chat-messages">
            {chatMessages.length === 0 && (
              <div className="chat-welcome">
                <MessageCircle size={48} />
                <p>Ask me anything about stocks!</p>
                <div className="example-questions">
                  <button onClick={() => setChatInput("What's a good P/E ratio?")}>
                    What's a good P/E ratio?
                  </button>
                  <button onClick={() => setChatInput("Should I invest in tech stocks?")}>
                    Should I invest in tech?
                  </button>
                </div>
              </div>
            )}
            
            {chatMessages.map((msg, index) => (
              <div key={index} className={`chat-message ${msg.role}`}>
                <div className="message-content">
                  {msg.content}
                </div>
              </div>
            ))}
            
            {isLoading && (
              <div className="chat-message assistant">
                <div className="message-content loading">
                  <span></span><span></span><span></span>
                </div>
              </div>
            )}
            
            <div ref={chatEndRef} />
          </div>
          
          <div className="chat-input">
            <input
              type="text"
              placeholder="Ask about stocks..."
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && sendChatMessage()}
              disabled={isLoading}
            />
            <button onClick={sendChatMessage} disabled={isLoading}>
              <Send size={20} />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;