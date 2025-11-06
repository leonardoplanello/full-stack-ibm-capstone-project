# Car Dealership Review Portal - IBM Full Stack Development Capstone Project

## Overview

This project is the **Capstone Project** for the **IBM Full Stack Development Specialization** on Coursera. It is a comprehensive full-stack web application that allows customers to browse car dealerships across the United States, view dealership reviews, and submit their own reviews. The application demonstrates proficiency in modern web development technologies, microservices architecture, containerization, and cloud deployment.

## Project Description

A national car dealership with local branches across the United States wanted to provide customers with a centralized database of dealership reviews. This application enables:

- **Anonymous users** to browse dealerships, filter by state, view reviews, and access contact information
- **Registered users** to create accounts, log in, and submit reviews for any dealership
- **Admin users** to manage car makes, models, and other attributes through Django admin panel

The application uses sentiment analysis to automatically analyze review sentiments, providing transparency and building customer trust.

## Architecture

The application follows a microservices architecture with the following components:

```
┌─────────────────────────────────────────────────────────────┐
│                    React Frontend (Port 3000)               │
│              - User Interface & Routing                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│          Django Backend (Port 8000)                          │
│  - User Authentication & Management                          │
│  - Car Make/Model Management (SQLite)                       │
│  - Proxy Services for Dealerships & Reviews                  │
└──────┬───────────────────────────────┬──────────────────────┘
       │                               │
┌──────▼──────────┐        ┌──────────▼──────────────┐
│ Express/MongoDB │        │ Sentiment Analyzer       │
│ Service         │        │ (IBM Cloud Code Engine)  │
│ (Port 3030)     │        │                          │
│ - Dealerships   │        │ - NLP Sentiment Analysis │
│ - Reviews       │        │                          │
└─────────────────┘        └──────────────────────────┘
```

### Technology Stack

#### Frontend
- **React 18.2.0** - Modern UI framework
- **React Router DOM 6.19.0** - Client-side routing
- **Bootstrap** - Responsive styling
- **CSS3** - Custom styling

#### Backend
- **Django 3.2.5+** - Python web framework
- **Django REST Framework** - API endpoints
- **SQLite** - Database for car makes/models and user data
- **Gunicorn** - WSGI HTTP server for production

#### Microservices
- **Node.js/Express** - Dealership and review management service
- **MongoDB** - NoSQL database for dealerships and reviews
- **Python Flask** - Sentiment analyzer microservice (deployed on IBM Cloud Code Engine)
- **NLTK/VADER** - Natural Language Processing for sentiment analysis

#### DevOps & Deployment
- **Docker** - Containerization
- **Kubernetes** - Container orchestration
- **GitHub Actions** - CI/CD pipeline with linting
- **IBM Cloud Code Engine** - Cloud deployment platform

## Features

### User Features
- ✅ User registration and authentication
- ✅ Browse all dealerships
- ✅ Filter dealerships by state
- ✅ View detailed dealership information
- ✅ View dealership reviews with sentiment analysis
- ✅ Submit reviews (authenticated users only)
- ✅ Static pages: About Us, Contact Us

### Admin Features
- ✅ Django admin panel access
- ✅ Manage car makes and models
- ✅ User management

### Technical Features
- ✅ RESTful API design
- ✅ Microservices architecture
- ✅ Sentiment analysis integration
- ✅ Docker containerization
- ✅ Kubernetes deployment
- ✅ CI/CD with automated linting
- ✅ Responsive design

## Project Structure

```
capstone-project/
├── server/
│   ├── djangoapp/              # Django application
│   │   ├── models.py          # CarMake, CarModel models
│   │   ├── views.py           # View functions
│   │   ├── restapis.py        # API proxy functions
│   │   ├── urls.py            # URL routing
│   │   └── microservices/     # Sentiment analyzer service
│   ├── djangoproj/            # Django project settings
│   │   ├── settings.py        # Configuration
│   │   └── urls.py            # Main URL configuration
│   ├── frontend/              # React frontend
│   │   ├── src/
│   │   │   ├── App.js         # Main React app
│   │   │   └── components/    # React components
│   │   │       ├── Dealers/   # Dealership components
│   │   │       ├── Login/     # Login component
│   │   │       └── Register/  # Registration component
│   │   └── build/             # Production build
│   ├── database/              # Express/MongoDB service
│   │   ├── app.js             # Express server
│   │   ├── review.js          # Review model
│   │   ├── dealership.js      # Dealership model
│   │   ├── data/              # Seed data
│   │   └── Dockerfile         # Database service container
│   ├── Dockerfile             # Django app container
│   ├── entrypoint.sh          # Container entrypoint script
│   ├── deployment.yaml        # Kubernetes deployment
│   ├── requirements.txt       # Python dependencies
│   └── manage.py              # Django management script
├── workflows/
│   └── main.yml               # GitHub Actions CI/CD
└── README.md                  # This file
```

## Prerequisites

Before running this application, ensure you have the following installed:

- **Python 3.12+**
- **Node.js 14+** and npm
- **MongoDB** (running locally or remotely)
- **Docker** (for containerization)
- **Kubernetes** (for deployment)
- **Git**

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd capstone-project
```

### 2. Set Up Django Backend

```bash
cd server

# Create virtual environment
python -m venv djangoenv

# Activate virtual environment
# On Windows:
djangoenv\Scripts\activate
# On macOS/Linux:
source djangoenv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional, for admin access)
python manage.py createsuperuser
```

### 3. Set Up MongoDB/Express Service

```bash
cd database

# Install dependencies
npm install

# Ensure MongoDB is running
# On Windows: Start MongoDB service
# On macOS: brew services start mongodb-community
# On Linux: sudo systemctl start mongod

# Start the Express server
node app.js
```

The service will run on `http://localhost:3030` and automatically populate the database with sample dealerships and reviews.

### 4. Set Up React Frontend

```bash
cd frontend

# Install dependencies
npm install

# Build the frontend
npm run build
```

### 5. Configure Environment Variables

Create a `.env` file in the `server` directory:

```env
backend_url=http://localhost:3030
sentiment_analyzer_url=<your-sentiment-analyzer-url>
```

### 6. Run the Application

```bash
# From the server directory
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## API Endpoints

### Django Endpoints

- `GET /djangoapp/get_dealers/` - Get all dealerships
- `GET /djangoapp/get_dealers/<state>` - Get dealerships by state
- `GET /djangoapp/dealer/<id>` - Get dealer details
- `GET /djangoapp/reviews/dealer/<id>` - Get reviews for a dealer
- `POST /djangoapp/add_review` - Add a review
- `GET /djangoapp/get_cars` - Get car makes and models
- `POST /djangoapp/login` - User login
- `POST /djangoapp/logout` - User logout
- `POST /djangoapp/register` - User registration

### Express/MongoDB Endpoints

- `GET /fetchDealers` - Fetch all dealers
- `GET /fetchDealer/:id` - Fetch dealer by ID
- `GET /fetchReviews` - Fetch all reviews
- `GET /fetchReview/dealer/:id` - Fetch reviews for a dealer
- `POST /insertReview` - Insert a new review

## Deployment

### Docker Deployment

Build and run the Django application container:

```bash
# Build the image
docker build -t dealership-app .

# Run the container
docker run -p 8000:8000 dealership-app
```

### Kubernetes Deployment

```bash
# Apply the deployment
kubectl apply -f deployment.yaml

# Port forward to access the application
kubectl port-forward deployment/dealership 8000:8000
```

### CI/CD

The project includes GitHub Actions workflows for automated linting:
- Python files are linted using `flake8`
- JavaScript files are linted using `JSHint`

The workflow runs automatically on push to main/master branch and on pull requests.

## Testing

### Manual Testing Checklist

1. ✅ Django server runs successfully
2. ✅ Static pages (About Us, Contact Us) render correctly
3. ✅ User registration works
4. ✅ User login/logout works
5. ✅ Dealerships list displays correctly
6. ✅ State filtering works
7. ✅ Dealer details page shows reviews
8. ✅ Review submission works (authenticated users)
9. ✅ Sentiment analysis displays correctly
10. ✅ Admin panel accessible

## Screenshots

Screenshots demonstrating various features are available in the `extra/screenshots/` directory, including:
- Django server running
- Static pages (About Us, Contact Us)
- Login/Logout functionality
- Dealership listings
- Review submission
- Admin panel
- Sentiment analyzer
- Deployed application

## Grading Criteria

This project was evaluated based on the following modules (50 points total):

- **Module 1**: Static Pages (7 points)
- **Module 2**: User Management (8 points)
- **Module 3**: Backend Services (17 points)
- **Module 4**: Dynamic Pages (9 points)
- **Module 5**: CI/CD & Deployment (9 points)

## Known Issues & Future Improvements

- [ ] Add unit tests for backend services
- [ ] Add integration tests for API endpoints
- [ ] Implement pagination for dealership listings
- [ ] Add search functionality
- [ ] Implement review editing/deletion
- [ ] Add image upload for reviews
- [ ] Improve error handling and user feedback
- [ ] Add rate limiting for API endpoints

## Contributing

This is a capstone project for educational purposes. However, suggestions and improvements are welcome!

## License

This project was created as part of the IBM Full Stack Development Specialization on Coursera.

## Acknowledgments

- **IBM Skills Network** - Course materials and guidance
- **Coursera** - Learning platform
- Course instructors: Upkar Lidder, Lavanya, Yan Luo, and Priya

## Author

Developed as part of the **IBM Full Stack Development Specialization** capstone project.

---

**Note**: This project demonstrates proficiency in full-stack development, including frontend (React), backend (Django), microservices (Express/Node.js), database management (SQLite, MongoDB), containerization (Docker), orchestration (Kubernetes), and CI/CD practices.

