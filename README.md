# Blog Application

This application is a blogging platform built with Django and Django REST Framework (DRF). It includes role-based access control (RBAC) and integrates with a language model (LLM) such as OpenAI's GPT.

## Features
- Role-based access control (RBAC)
- Article management
- LLM integration for text processing

---

## Setup Instructions

### Prerequisites
Ensure you have the following installed:
- Docker
- Docker Compose

### Clone the Repository
```bash
git clone <repository_url>
cd blog
```

### Configure Environment Variables
Create a `.env` file in the root directory and populate it with the required environment variables:

```env
# Application settings
DJANGO_SETTINGS_MODULE=blog.settings

# Application Port
PORT=8000

# Database Variables
POSTGRES_USER=username
POSTGRES_PASSWORD=password
POSTGRES_DB=databasename
DATABASE_URL=postgres://username:password@db:5432/databasename

# LLM integration
OPENAI_API_KEY=<your_openai_api_key>

# Other settings
SECRET_KEY=<your_secret_key>
DEBUG=True
ALLOWED_HOSTS=*
```

### Start the Application with Docker
Build and start the application using Docker Compose:

```bash
docker-compose up --build
```

The application will be accessible at `http://localhost:8000`.

---

## Running Tests

To run the unit tests:

1. Ensure the application is running.
2. Run the following command within the Docker container:

```bash
docker exec -it blog_app python manage.py test api
```

---

## LLM Integration Configuration

The application integrates with an LLM such as OpenAI's GPT for advanced text processing. To configure this:

1. Set the `OPENAI_API_KEY` environment variable in your `.env` file.
2. Ensure the key is valid and has the necessary permissions for the OpenAI API.

Example usage:
- Text generation or processing endpoints in the API will automatically use the `OPENAI_API_KEY` for API calls.

---

## Additional Notes
- Always ensure your `.env` file is not committed to version control.
- For production, set `DEBUG=False` and configure `ALLOWED_HOSTS` appropriately.
- Import Blog.postman_collection.json to test

For further information, refer to the documentation or contact the project maintainer.
