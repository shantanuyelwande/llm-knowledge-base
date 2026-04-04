#!/bin/bash
# Start the LLM Knowledge Base system

set -e

echo "🚀 Starting LLM Knowledge Base..."

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "Please create .env from .env.example and add your ANTHROPIC_API_KEY"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
echo "📚 Installing dependencies..."
pip install -q -r requirements.txt

# Initialize data directories
echo "📁 Initializing directories..."
mkdir -p data/raw data/wiki data/output

# Start backend
echo "🔧 Starting backend API on port 8000..."
cd backend
python main.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 2

# Display frontend instructions
echo ""
echo "✅ Backend started (PID: $BACKEND_PID)"
echo ""
echo "📖 Frontend available at: frontend/index.html"
echo "   Open it in your browser or serve with:"
echo "   cd frontend && python -m http.server 5000"
echo ""
echo "🎯 API available at: http://localhost:8000"
echo "   API docs at: http://localhost:8000/docs"
echo ""
echo "💻 CLI available at: cd cli && python main.py"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Keep the script running
wait $BACKEND_PID
