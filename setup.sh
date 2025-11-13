#!/bin/bash

echo "================================================"
echo "SpeakMate Setup Script"
echo "================================================"

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please edit .env file with your configuration!"
fi

echo "Creating migrations..."
python manage.py makemigrations

echo "Applying migrations..."
python manage.py migrate

echo ""
echo "================================================"
echo "Setup completed!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your database and email settings"
echo "2. Create a superuser: python manage.py createsuperuser"
echo "3. Run the server: python manage.py runserver"
echo "4. Visit http://localhost:8000"
echo ""
echo "For Google OAuth setup, see INSTALLATION.md"
echo "================================================"

