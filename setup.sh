#!/bin/bash

# Best Cars Dealership - Quick Setup Script
echo "==================================================="
echo "  Best Cars Dealership - Setup Script"
echo "==================================================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required. Please install it first."
    exit 1
fi

# Check Node
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required. Please install it first."
    exit 1
fi

echo "✅ Python and Node.js found"

# Setup virtual environment
echo ""
echo "📦 Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null

# Install Python deps
echo "📦 Installing Python dependencies..."
pip install -r server/requirements.txt

# Setup Django
echo ""
echo "🗄️  Setting up Django database..."
cd server
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo ""
echo "👤 Creating admin superuser..."
echo "   (Username: admin, Password: admin123)"
echo "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@bestcars.com', 'admin123')" | python manage.py shell

# Build React frontend
echo ""
echo "⚛️  Building React frontend..."
cd frontend
npm install
npm run build
cd ..

echo ""
echo "==================================================="
echo "  ✅ Setup Complete!"
echo "==================================================="
echo ""
echo "  To start the development server:"
echo "  cd server && python manage.py runserver"
echo ""
echo "  Then open: http://localhost:8000"
echo "  Admin panel: http://localhost:8000/admin"
echo "  Admin login: admin / admin123"
echo ""
echo "  API Endpoints:"
echo "  GET  http://localhost:8000/djangoapp/get_dealers"
echo "  GET  http://localhost:8000/djangoapp/get_dealers/Kansas"
echo "  GET  http://localhost:8000/djangoapp/dealer/1"
echo "  GET  http://localhost:8000/djangoapp/reviews/dealer/1"
echo "  GET  http://localhost:8000/djangoapp/get_cars"
echo "  GET  http://localhost:8000/djangoapp/analyze_review?text=Fantastic+services"
echo "  POST http://localhost:8000/djangoapp/login"
echo "  GET  http://localhost:8000/djangoapp/logout"
echo "  POST http://localhost:8000/djangoapp/register"
echo ""
