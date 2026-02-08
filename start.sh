#!/bin/bash

# Stock Dashboard - Quick Start Script
# This script helps you get the application running quickly

echo "================================================"
echo "🚀 Stock Dashboard - Quick Start Setup"
echo "================================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed!"
    echo "Please install Docker from: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed!"
    echo "Please install Docker Compose from: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker is installed"
echo "✅ Docker Compose is installed"
echo ""

# Check for .env file
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.template .env
    echo "📝 Please edit .env file and add your ANTHROPIC_API_KEY"
    echo "   Get a free API key at: https://console.anthropic.com"
    echo ""
    read -p "Press Enter when you've added your API key to .env (or press Ctrl+C to exit and do it later)..."
fi

echo ""
echo "🏗️  Building and starting Docker containers..."
echo "This may take a few minutes on first run..."
echo ""

# Build and start containers
docker-compose up --build -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if containers are running
if docker ps | grep -q "stock_backend"; then
    echo "✅ Backend is running"
else
    echo "❌ Backend failed to start"
    echo "Check logs with: docker-compose logs backend"
fi

if docker ps | grep -q "stock_frontend"; then
    echo "✅ Frontend is running"
else
    echo "❌ Frontend failed to start"
    echo "Check logs with: docker-compose logs frontend"
fi

if docker ps | grep -q "stock_db"; then
    echo "✅ Database is running"
else
    echo "❌ Database failed to start"
    echo "Check logs with: docker-compose logs db"
fi

echo ""
echo "================================================"
echo "🎉 Setup Complete!"
echo "================================================"
echo ""
echo "📱 Access your application:"
echo "   Frontend:  http://localhost:3000"
echo "   API:       http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo ""
echo "📊 Useful Commands:"
echo "   View logs:        docker-compose logs -f"
echo "   Stop services:    docker-compose down"
echo "   Restart:          docker-compose restart"
echo "   Rebuild:          docker-compose up --build"
echo ""
echo "🐛 Troubleshooting:"
echo "   If something isn't working:"
echo "   1. Check logs: docker-compose logs -f [service-name]"
echo "   2. Restart: docker-compose restart"
echo "   3. Full rebuild: docker-compose down && docker-compose up --build"
echo ""
echo "📚 For more information, see README.md"
echo ""
echo "Happy coding! 🚀"