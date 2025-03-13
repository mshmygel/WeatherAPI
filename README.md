# ☁️ Weather Dashboard


This project is a Django-based system for fetching, storing, and displaying weather data for multiple cities. It uses Celery and Redis for asynchronous tasks, PostgreSQL for data storage, and a simple HTML/JS front-end (with Chart.js) for visualizing current and historical weather.

## Key Features
- Periodically fetch weather data from OpenWeatherMap (or similar) via Celery tasks.
- Store all weather records in a PostgreSQL database.
- Display the latest weather for each city and an optional history chart.
- Expose RESTful API endpoints (Django REST Framework).
- Provide automatic API documentation (Swagger/ReDoc).

## Usage & Endpoints
- **Swagger UI**: [http://localhost/swagger/](http://localhost/swagger/)
- **ReDoc**: [http://localhost/redoc/](http://localhost/redoc/)
- **Django Admin**: [http://localhost/admin/](http://localhost/admin/)
- **Dashboard Front-End**: [http://localhost/dashboard/](http://localhost/dashboard/)
- **API Root**: [http://localhost/api/](http://localhost/api/)

## Running with Docker

1. **Clone** this repository and navigate into the project folder.
2. **Copy** `.env.sample` to `.env` in the project root.
3. **Fill in** the `.env` file with your values (database credentials, Redis settings, OpenWeatherMap API key, etc.).
4. **Build and start** the Docker containers:
   ```bash
   docker-compose up -d --build
