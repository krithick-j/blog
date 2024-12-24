# Blog Application

## Project Setup

This document provides detailed instructions to set up, run, and test the Blog application.

### Features
- Role-based access control (RBAC) for creating articles.
- Feature flags for dynamically enabling/disabling application features.
- Integration with OpenAI API for AI-powered features.
- Django Admin interface for managing users and content.

### Prerequisites
- Docker and Docker Compose
- Python 3.9+
- PostgreSQL

### Environment Variables
Create a `.env` file in the root directory with the following variables:
```env
# Application Port
PORT=8000

# Database Variables
POSTGRES_USER=username
POSTGRES_PASSWORD=password
POSTGRES_DB=databasename
DATABASE_URL=postgres://username:password@db:5432/databasename

# OpenAI API Key
OPENAI_API_KEY=

# Application Secret Key
SECRET_KEY=

# Debug Mode
DEBUG=True

# Allowed Hosts
ALLOWED_HOSTS=localhost,127.0.0.1

# Database URL
DATABASE_URL=postgres://postgres:password@db:5432/postgres
```

### Setup Instructions

#### Using Docker
1. Build and start the application:
   ```bash
   docker-compose up --build
   ```

2. Create a super admin user:
   ```bash
   docker exec -it blog_app python manage.py createsuperuser
   ```

3. Access the application at `http://localhost:8000`.
4. Log in as the super admin at `http://localhost:8000/admin` to create additional admin users.
5. Create members with roles by POST /users/ using admin account.
6. If authentication is not provided, then role will be set to default as member.
7. First member who creates the account will be become the owner.

#### Local Development
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Apply migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. Run the development server:
   ```bash
   python manage.py runserver
   ```

4. For debugging:
   - Install the Python Debugger (pdb):
     ```bash
     pip install pdbpp
     ```
   - Run the application without Docker Compose.

### Running Tests
Run the tests using Docker:
```bash
docker exec -it blog_app python manage.py test api
```

### Import Postman Collection
Use the provided `Blog.postman_collection.json` file to test API endpoints:
1. Open Postman.
2. Import the `Blog.postman_collection.json` file.
3. Use the Collection's environment variables for easy access.
4. Run the requests to test the API.

### Debugging
- To debug locally without Docker Compose, use `pdb` or any IDE with debugging capabilities.
- To disable SQL debugging, comment out the `LOGGING` configuration in `settings.py`:
```python
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django.db.backends': {
#             'level': 'DEBUG',
#             'handlers': ['console'],
#         },
#     },
# }
```
