# FAQ Management System

A Django-based multilingual FAQ management system with WYSIWYG editing support and manual translations.

## Features

- WYSIWYG editor for FAQ content using CKEditor
- Multi-language support (English, Hindi, Bengali)
- Manual translation management
- REST API with language selection
- Caching for improved performance
- Admin interface for easy content management
- Comprehensive test coverage
- Production-ready Docker configuration

## Technical Stack

- **Backend Framework**: Django 5.0.1
- **API Framework**: Django REST Framework 3.14.0
- **Database**: SQLite (can be easily switched to PostgreSQL)
- **Caching**: Django's cache framework with Redis support
- **Rich Text Editor**: CKEditor
- **Testing**: pytest with pytest-django
- **Containerization**: Docker and Docker Compose

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/FAQMaster.git
cd FAQMaster
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set a private signing key in the server environment before running any Django command:
```bash
export DJANGO_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(64))')"
```
In PowerShell use `$env:DJANGO_SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(64))"`.
Keep this value private. Settings reject a missing or blank key. For Docker Compose,
copy `.env.example` to `.env` and replace the empty value with your own generated key;
ordinary Django commands do not automatically load `.env`.

4. Apply migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

```
FAQMaster/
├── faq/                    # Main app directory
│   ├── models.py          # FAQ model with translation support
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API views and viewsets
│   └── tests.py           # Unit tests
├── faqmaster/             # Project settings
│   ├── settings.py        # Development settings
│   └── settings_prod.py   # Production settings
├── requirements.txt       # Project dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
└── nginx.conf           # Nginx configuration for production
```

## Implementation Details

### 1. Multi-language Support
- Each FAQ entry stores translations for questions and answers
- Supported languages: English (default), Hindi, Bengali
- Language selection via URL parameter (?lang=hi, ?lang=bn)
- Fallback to English if translation not available

### 2. Caching Strategy
- Cached FAQ lists per language
- Cache invalidation on FAQ updates
- Redis support for production
- Local memory cache for development

### 3. API Design
- RESTful endpoints following best practices
- Proper status codes and error handling
- Comprehensive response formatting
- Built-in documentation

## API Documentation

### Endpoints

#### 1. List FAQs
```bash
# Get all FAQs (English by default)
GET /api/faqs/

# Get FAQs in Hindi
GET /api/faqs/?lang=hi

# Get FAQs in Bengali
GET /api/faqs/?lang=bn
```

Response:
```json
{
    "count": 1,
    "results": [
        {
            "id": 1,
            "question": "What is this FAQ system?",
            "answer": "This is a multilingual FAQ system...",
            "created_at": "2024-02-03T12:00:00Z",
            "updated_at": "2024-02-03T12:00:00Z"
        }
    ]
}
```

#### 2. Create FAQ
```bash
POST /api/faqs/
Content-Type: application/json

{
    "question": "What is this?",
    "answer": "This is a FAQ system",
    "question_hi": "यह क्या है?",
    "answer_hi": "यह एक FAQ सिस्टम है",
    "question_bn": "এটা কি?",
    "answer_bn": "এটি একটি FAQ সিস্টেম"
}
```

#### 3. Update FAQ
```bash
PUT /api/faqs/{id}/
Content-Type: application/json

{
    "question": "Updated question",
    "answer": "Updated answer",
    "question_hi": "अपडेट किया गया प्रश्न",
    "answer_hi": "अपडेट किया गया उत्तर"
}
```

#### 4. Delete FAQ
```bash
DELETE /api/faqs/{id}/
```

## Testing

The project includes comprehensive tests covering:
- Model functionality
- API endpoints
- Caching mechanism
- Translation features

Run tests with:
```bash
python manage.py test
```

## Production Deployment

For production deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## Contributing

1. Fork the repository
2. Create your feature branch:
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Open a Pull Request

### Commit Message Guidelines
- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- test: Adding tests
- refactor: Code refactoring
- style: Code style changes
- chore: Build process or auxiliary tool changes

### Code Style
- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused
- Write unit tests for new features

## License

This project is licensed under the MIT License - see the LICENSE file for details.
