# Data Hub

A scalable platform for data ingestion, quality assessment, and preparation for machine learning, data science, and AI agent tasks.

## 🚀 Features

- **Multi-format Data Processing**: Support for PDF, Excel, CSV, and Parquet files
- **Data Quality Assessment**: Automatic validation and quality scoring of datasets
- **ML/AI Readiness**: Evaluation of data suitability for different ML/DS tasks
- **Scalable Architecture**: Django + FastAPI backend with Celery for async processing
- **RESTful API**: Comprehensive API for data management and processing
- **Container Ready**: Docker and Docker Compose setup for easy deployment

## 🏗️ Architecture

This project combines Django for data modeling and administration with FastAPI for high-performance API endpoints. Processing-intensive tasks are handled asynchronously using Celery.

### Main Components:

- **Django Core**: Data models, authentication, and administration
- **FastAPI**: High-performance API endpoints
- **Celery**: Asynchronous task processing
- **PostgreSQL**: Primary database
- **Redis**: Message broker for Celery

## 🛠️ Installation

### Prerequisites

- Python 3.10+
- PostgreSQL
- Redis

### Using Docker Compose (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/datahub.git
   cd datahub
   ```

2. Create a `.env` file based on the example:
   ```bash
   cp .env .env
   # Edit .env with your configuration
   ```

3. Build and start the services:
   ```bash
   docker-compose up -d
   ```

4. Create a superuser:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

### Manual Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/datahub.git
   cd datahub
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file and configure your environment variables

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

8. In a separate terminal, start Celery:
   ```bash
   celery -A config worker -l info
   ```

9. In another terminal, start the FastAPI server:
   ```bash
   cd fastapi
   uvicorn main:app --reload --port 8001
   ```

## 💻 API Usage

### Django REST API

The Django REST API is available at `http://localhost:8000/api/`.

### FastAPI

The FastAPI endpoints are available at `http://localhost:8001/api/`.
API documentation is automatically generated at `http://localhost:8001/docs`.

### Authentication

API endpoints are secured using token-based authentication. To obtain a token:

```bash
curl -X POST http://localhost:8000/api/token/ -d "username=admin&password=password"
```

Use the token in subsequent requests:

```bash
curl -H "Authorization: Token YOUR_TOKEN" http://localhost:8000/api/data/datasets/
```

## 📋 Data Flow

1. **Data Upload**: Files are uploaded through the API
2. **Processing**: Celery tasks process and extract metadata from files
3. **Quality Assessment**: Data quality metrics are calculated
4. **Suitability Evaluation**: Data is analyzed for ML/DL/AI suitability
5. **Storage Organization**: Files are stored in structured directories by type

## 🔌 Integration

### Future Components

The platform is designed to integrate with future components:

- **Scrapers**: Automated data collection (separate project)
- **ML Pipelines**: Preprocessing, training, and validation workflows
- **AI Agents**: Smart data analysis and processing
- **Quality Checkers**: In-depth data quality validation and improvement

### Extension Points

- **File Handlers**: Add new handlers in `data_manager/file_handlers/`
- **Quality Validators**: Extend validation in `data_manager/quality_validators/`
- **API Endpoints**: Add new endpoints in FastAPI routers

## 🔄 CI/CD Pipeline

The repository includes GitHub Actions workflows for:

- **Testing**: Automated testing with pytest
- **Linting**: Code quality checks with flake8, black, and isort
- **Building**: Docker image creation and pushing to registry
- **Deployment**: Automatic deployment to production server

## 🧪 Testing

Run tests with pytest:

```bash
pytest
```

For coverage report:

```bash
pytest --cov=.
```

## 📝 Documentation

API documentation is available at:
- Django REST API: `/api/docs/`
- FastAPI: `/docs` or `/redoc`

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.