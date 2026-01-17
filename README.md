# Microservices Project

A distributed microservices architecture built with Django and Flask, communicating via RabbitMQ message queue.

## Project Structure

```
microservice/
├── admin/                 # Django admin service
│   ├── manage.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── consumer.py       # RabbitMQ consumer
│   ├── products/         # Django app for product management
│   └── admin/            # Django configuration
│
├── main/                 # Flask main service
│   ├── main.py
│   ├── manager.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── consumer.py       # RabbitMQ consumer
│   ├── producer.py       # RabbitMQ producer
│   └── migrations/       # Alembic database migrations
│
└── README.md            # This file
```

## Services

### Admin Service (Django)
- **Port:** 8000
- **Purpose:** Product management and administration
- **Database:** SQLite (configurable to MySQL)
- **Key Components:**
  - Product CRUD operations
  - User management
  - Message queue consumer for product updates

### Main Service (Flask)
- **Port:** 5000
- **Purpose:** Main application with product synchronization
- **Database:** SQLAlchemy with Alembic migrations
- **Key Components:**
  - Product display and synchronization
  - Message queue consumer for product operations
  - Producer for inter-service communication

## Message Queue

Both services communicate via **RabbitMQ (CloudAMQP)**:
- **Queue Names:**
  - `admin` - Messages sent to admin service
  - `main` - Messages sent to main service

## Environment Variables

Create a `.env` file in each service directory:

```
pika_url=amqps://[username]:[password]@[host]/[vhost]
```

This variable is automatically passed to Docker containers via `docker-compose.yml`.

## Setup & Running

### Prerequisites
- Docker & Docker Compose
- Python 3.9+
- RabbitMQ (CloudAMQP for cloud hosting)

### Local Development

1. **Start Admin Service:**
   ```bash
   cd admin
   docker-compose up
   ```

2. **Start Main Service:**
   ```bash
   cd main
   docker-compose up
   ```

### Docker Compose Services

Each service runs:
- **backend** - Django/Flask application server
- **queue** - RabbitMQ message consumer

## API Endpoints

### Admin Service
- Product Management: `/api/products/`
- User Management: `/api/users/`

### Main Service
- Product Synchronization: `/products/`

## Communication Flow

1. **Product Creation (Admin → Main):**
   - Admin creates/updates product
   - Admin sends message to `main` queue
   - Main consumer receives and synchronizes product

2. **Product Engagement (Main → Admin):**
   - Main service tracks product interactions
   - Sends engagement data to `admin` queue
   - Admin updates product likes/engagement metrics

## Technologies

- **Backend:** Django (admin), Flask (main)
- **Database:** SQLite/MySQL (admin), PostgreSQL/SQLite (main)
- **Message Queue:** RabbitMQ via Pika
- **Container:** Docker & Docker Compose
- **ORM:** Django ORM (admin), SQLAlchemy (main)
- **Migrations:** Django migrations (admin), Alembic (main)

## Configuration

### Docker Compose Files
Both services have `docker-compose.yml` defining:
- Service containers (backend + queue)
- Environment variables
- Volume mounts for development
- Port mappings

## Notes

- Both services must have access to the same RabbitMQ instance
- Use environment variables for sensitive data (API keys, database credentials)
- Database credentials are environment-specific and managed separately
- Services are designed to be independently deployable and scalable
