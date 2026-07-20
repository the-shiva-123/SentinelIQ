#!/bin/bash
# SentinelIQ Project Startup Script

echo "🚀 Starting SentinelIQ Project..."
echo "=================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18 or higher."
    exit 1
fi

# Start Backend (FastAPI)
echo -e "${BLUE}Starting FastAPI Backend on port 8000...${NC}"
python3 run.py &
BACKEND_PID=$!
sleep 3
echo -e "${GREEN}✅ Backend started (PID: $BACKEND_PID)${NC}"

# Start Frontend (Vite)
echo -e "${BLUE}Starting React Frontend on port 5173...${NC}"
cd sentineliq-frontend
npm install
npm run dev &
FRONTEND_PID=$!
sleep 3
echo -e "${GREEN}✅ Frontend started (PID: $FRONTEND_PID)${NC}"

echo ""
echo "=================================="
echo -e "${GREEN}🎉 SentinelIQ is now running!${NC}"
echo "=================================="
echo -e "🌐 Frontend: http://localhost:5173"
echo -e "🔌 Backend API: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop both services"

# Wait for both processes
wait
