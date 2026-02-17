# Best Cars Dealership - Full Stack Web Application

## Project Overview

A full-stack web application built with **Django** (backend) and **React** (frontend) that allows users to browse car dealerships, read reviews, and post their own reviews with sentiment analysis.

## Project Name: Best Cars Dealership Platform

## Tech Stack

- **Backend**: Django 4.x + Django REST Framework
- **Frontend**: React 18 + Vite
- **Database**: SQLite (development) / PostgreSQL (production)
- **Sentiment Analysis**: IBM Watson NLU / Custom NLP service
- **Deployment**: IBM Cloud Code Engine / Railway / Render
- **CI/CD**: GitHub Actions

## Features

- Browse all car dealerships
- Filter dealerships by state
- View dealer details and customer reviews
- Post reviews with sentiment analysis
- User authentication (Register, Login, Logout)
- Admin panel for managing data
- RESTful API endpoints

## Project Structure

```
dealership_project/
├── README.md
├── server/
│   ├── manage.py
│   ├── requirements.txt
│   ├── djangoapp/          # Main Django app
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── ...
│   ├── frontend/           # React frontend
│   │   ├── src/
│   │   │   └── components/
│   │   │       ├── Header/
│   │   │       ├── Login/
│   │   │       ├── Register/
│   │   │       ├── Dealers/
│   │   │       ├── Dealer/
│   │   │       └── PostReview/
│   │   └── static/
│   │       ├── About.html
│   │       └── Contact.html
│   ├── database/           # Cloudant DB functions
│   ├── sentiment_analyzer/ # NLU microservice
│   └── .github/
│       └── workflows/      # CI/CD pipelines
```

## Setup Instructions

### Prerequisites
- Python 3.9+
- Node.js 16+
- npm 8+

### Backend Setup

```bash
cd server
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend Setup

```bash
cd server/frontend
npm install
npm run build
```

### Environment Variables

Create a `.env` file in the `server/` directory:

```
SECRET_KEY=your-django-secret-key
DEBUG=True
IBM_API_KEY=your-ibm-api-key
IBM_NLU_URL=your-ibm-nlu-url
CLOUDANT_URL=your-cloudant-url
CLOUDANT_KEY=your-cloudant-key
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/djangoapp/get_dealers` | Get all dealers |
| GET | `/djangoapp/get_dealers/:state` | Get dealers by state |
| GET | `/djangoapp/dealer/:id` | Get dealer by ID |
| GET | `/djangoapp/reviews/dealer/:id` | Get reviews for a dealer |
| POST | `/djangoapp/add_review` | Add a review |
| GET | `/djangoapp/get_cars` | Get all car makes and models |
| POST | `/djangoapp/login` | User login |
| POST | `/djangoapp/logout` | User logout |
| POST | `/djangoapp/register` | User registration |
| GET | `/djangoapp/analyze_review` | Analyze review sentiment |

## Team Members

- **Alex Johnson** - Full Stack Developer | alex.johnson@bestcars.com
- **Maria Garcia** - Backend Engineer | maria.garcia@bestcars.com
- **James Smith** - Frontend Developer | james.smith@bestcars.com

## License MIT
## Author: Tadagbe Landry MASSOLOKONON
MIT License - Best Cars Dealership 2024
