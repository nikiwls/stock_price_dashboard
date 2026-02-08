"""
AI Chatbot Service using OpenRouter API
Handles stock-related questions with context from the database
"""

import os
from openai import OpenAI
from typing import Optional, List, Dict
from datetime import datetime


class AIService:
    """
    AI-powered chatbot for stock inquiries
    Uses OpenRouter API for intelligent responses
    """
    
    def __init__(self):
        """Initialize OpenRouter client (OpenAI-compatible)"""
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            print("⚠️  Warning: OPENROUTER_API_KEY not set. AI features will be limited.")
            self.client = None
        else:
            # OpenRouter uses OpenAI-compatible API
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
            )
            print("✅ OpenRouter AI client initialized")
    
    
    def get_stock_context(self, stock_data: Optional[Dict] = None) -> str:
        """
        Build context string from stock data
        This helps Claude give more accurate answers
        """
        if not stock_data:
            return ""
        
        context = f"""
Current Stock Information:
- Symbol: {stock_data.get('symbol', 'N/A')}
- Company: {stock_data.get('company_name', 'N/A')}
- Current Price: ${stock_data.get('price', 'N/A')}
- Change: {stock_data.get('change_percent', 'N/A')}%
- Volume: {stock_data.get('volume', 'N/A'):,}
- Market Cap: ${stock_data.get('market_cap', 'N/A'):,}
- Day High: ${stock_data.get('day_high', 'N/A')}
- Day Low: ${stock_data.get('day_low', 'N/A')}
"""
        return context
    
    
    async def chat(
        self,
        user_message: str,
        stock_data: Optional[Dict] = None,
        chat_history: Optional[List[Dict]] = None
    ) -> str:
        """
        Generate AI response to user's stock inquiry
        
        Args:
            user_message: User's question
            stock_data: Current stock information
            chat_history: Previous conversation messages
            
        Returns:
            AI-generated response
        """
        if not self.client:
            return "I apologize, but the AI chatbot is currently unavailable. Please set the OPENROUTER_API_KEY environment variable."
        
        try:
            # Build system prompt
            system_prompt = """You are a helpful stock market assistant. You provide:
1. Clear, accurate information about stocks
2. Analysis of stock performance and trends
3. Explanations of stock market concepts
4. Investment insights (but NOT financial advice)

Always remind users that you're providing information, not financial advice, and they should do their own research or consult a financial advisor before making investment decisions.

Be concise but informative. Use the stock data provided to give context-aware answers."""
            
            # Build conversation messages (OpenAI format)
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            # Add chat history if available
            if chat_history:
                for msg in chat_history[-5:]:  # Last 5 messages for context
                    messages.append({
                        "role": "user",
                        "content": msg.get("user_message", "")
                    })
                    messages.append({
                        "role": "assistant",
                        "content": msg.get("ai_response", "")
                    })
            
            # Add current message with stock context
            current_content = user_message
            if stock_data:
                context = self.get_stock_context(stock_data)
                current_content = f"{context}\n\nUser Question: {user_message}"
            
            messages.append({
                "role": "user",
                "content": current_content
            })
            
            # Call OpenRouter API (OpenAI-compatible)
            response = self.client.chat.completions.create(
                model="anthropic/claude-3.5-sonnet",  # Can use other models on OpenRouter
                max_tokens=1000,
                messages=messages,
                extra_headers={
                    "HTTP-Referer": "http://localhost:3000",
                    "X-Title": "Stock Dashboard"
                }
            )
            
            # Extract response text
            ai_response = response.choices[0].message.content
            
            return ai_response
            
        except Exception as e:
            print(f"❌ AI Service Error: {e}")
            return f"I encountered an error processing your request: {str(e)}"
    
    
    def extract_stock_symbol(self, user_message: str) -> Optional[str]:
        """
        Extract stock symbol from user message
        Simple pattern matching (can be improved with NLP)
        """
        # Common stock symbols
        common_symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'META', 'NVDA', 'JPM', 'V', 'WMT']
        
        message_upper = user_message.upper()
        for symbol in common_symbols:
            if symbol in message_upper:
                return symbol
        
        return None
    
    
    def generate_summary(self, stock_data: Dict) -> str:
        """
        Generate a quick summary of stock performance
        This is a simple rule-based summary (not using AI to save API calls)
        """
        symbol = stock_data.get('symbol', '')
        company = stock_data.get('company_name', '')
        price = stock_data.get('price', 0)
        change = stock_data.get('change_percent', 0)
        
        # Determine sentiment
        if change > 2:
            sentiment = "📈 Strong upward momentum"
        elif change > 0:
            sentiment = "📊 Slight positive movement"
        elif change > -2:
            sentiment = "📉 Slight decline"
        else:
            sentiment = "⚠️ Significant drop"
        
        summary = f"""
{company} ({symbol})
Current Price: ${price}
Change: {change}%
{sentiment}

Market Status: {'Open' if datetime.utcnow().hour < 21 else 'Closed'}
"""
        return summary.strip()


# =======================
# Example Usage
# =======================

if __name__ == "__main__":
    import asyncio
    
    async def test_ai_service():
        ai = AIService()
        
        # Test stock data
        stock_data = {
            'symbol': 'AAPL',
            'company_name': 'Apple Inc.',
            'price': 175.50,
            'change_percent': 1.25,
            'volume': 50000000,
            'market_cap': 2700000000000,
            'day_high': 176.00,
            'day_low': 174.50
        }
        
        # Test chat
        response = await ai.chat(
            "What do you think about this stock's performance today?",
            stock_data=stock_data
        )
        print("\n🤖 AI Response:")
        print(response)
        
        # Test summary
        summary = ai.generate_summary(stock_data)
        print("\n📊 Stock Summary:")
        print(summary)
    
    # Run test
    asyncio.run(test_ai_service())