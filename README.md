# IBM Full Stack Developer Capstone – Car Dealership Application

A full-stack web application built as part of the **IBM Full Stack Software Developer Professional Certificate** Capstone Project.

## 📋 Project Overview

This application is a **Car Dealership Review Platform** that allows users to:
- Browse car dealerships across the United States
- Filter dealerships by state
- View individual dealer details and customer reviews
- Submit new reviews for dealerships
- Get AI-powered sentiment analysis on each review

## 🏗️ Architecture

| Layer | Technology | Port |
|-------|------------|------|
| Frontend | React.js | Served via Django |
| Backend API | Django + Python | 8000 |
| Database Microservice | Node.js + Express + MongoDB | 3030 |
| Sentiment Analyzer | Flask + NLTK | 5050 |
| Database | MongoDB | 27017 |
| SQLite | Django ORM | - |

## 🚀 Features

- ✅ User Registration & Authentication
- ✅ Login / Logout
- ✅ Dealer Listing (all states)
- ✅ Dealer Filter by State
- ✅ Dealer Details Page
- ✅ Customer Reviews with Sentiment Icons
- ✅ Add New Review (authenticated users)
- ✅ Car Makes & Models API
- ✅ Sentiment Analysis (Positive / Negative / Neutral)
- ✅ Django Admin Panel

## 🛠️ Local Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- Docker Desktop

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/xrwvm-fullstack_developer_capstone.git
cd xrwvm-fullstack_developer_capstone/server
```

### 2. Start MongoDB with Docker
```bash
docker run -d --name mongo_db -p 27017:27017 mongo:6.0
```

### 3. Start Node.js Microservice
```bash
cd database
npm install
node app.js
```

### 4. Set Up Python Environment
```bash
cd ..
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
```

### 5. Run Migrations & Seed Data
```bash
.\.venv\Scripts\python manage.py makemigrations
.\.venv\Scripts\python manage.py migrate
```

### 6. Start Sentiment Analyzer
```bash
.\.venv\Scripts\python djangoapp/microservices/app.py
```

### 7. Build React Frontend
```bash
cd frontend
npm install
npm run build
cd ..
.\.venv\Scripts\python manage.py collectstatic --noinput
```

### 8. Start Django Server
```bash
.\.venv\Scripts\python manage.py runserver
```

### 9. Access the Application
Open your browser at: **http://localhost:8000**

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/djangoapp/login` | User Login |
| GET | `/djangoapp/logout` | User Logout |
| POST | `/djangoapp/register` | User Registration |
| GET | `/djangoapp/get_dealers` | All Dealers |
| GET | `/djangoapp/get_dealers/<state>` | Dealers by State |
| GET | `/djangoapp/dealer/<id>` | Dealer Details |
| GET | `/djangoapp/reviews/dealer/<id>` | Dealer Reviews |
| POST | `/djangoapp/add_review` | Submit Review |
| GET | `/djangoapp/get_cars` | Car Makes & Models |

## 🐳 Docker Deployment

### Build Django Docker Image
```bash
docker build -t dealership-backend .
docker run -p 8000:8000 dealership-backend
```

## ☁️ IBM Cloud Code Engine Deployment

```bash
ibmcloud login
ibmcloud target -r us-south -g default
ibmcloud ce project create --name capstone-project
ibmcloud ce application create --name dealership-app --image us.icr.io/your-namespace/dealership-backend --port 8000
```

## 👨‍💻 Author

**Dileep M K** – IBM Full Stack Developer Certificate Program

## 📄 License

This project is licensed under the Apache 2.0 License – see the [LICENSE](LICENSE) file for details.