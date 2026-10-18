# Deployment Guide for FAQ Master

This guide provides instructions for deploying the FAQ Master application using Docker and various cloud providers.

## Table of Contents
- [Local Docker Deployment](#local-docker-deployment)
- [Cloud Deployment Options](#cloud-deployment-options)
  - [Heroku Deployment](#heroku-deployment)
  - [AWS Elastic Beanstalk Deployment](#aws-elastic-beanstalk-deployment)
  - [DigitalOcean Deployment](#digitalocean-deployment)

## Local Docker Deployment

### Prerequisites
1. Install Docker and Docker Compose on your machine
2. Git clone of the repository
3. Basic understanding of Docker and Django

### Step-by-Step Deployment

1. **Set Environment Variables**
   Copy `.env.example` to the ignored `.env` file in the project root. Generate a
   new private value with `python -c "import secrets; print(secrets.token_urlsafe(64))"`
   and place it in `DJANGO_SECRET_KEY`. Never commit the generated value.
   ```env
   DJANGO_SECRET_KEY=<paste-your-new-random-value-here>
   DJANGO_SETTINGS_MODULE=faqmaster.settings_prod
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

   Docker Compose reads `.env` and injects `DJANGO_SECRET_KEY` into the web
   container. Missing or blank keys stop startup. For direct Django/Gunicorn
   deployments, set `DJANGO_SECRET_KEY` in the process environment or your hosting
   secret manager; Django does not automatically read `.env`. Static files are
   collected at container startup so the build never needs a signing key.

   Rotate every previously committed Django signing key in each deployment,
   including any key from the removed `.env`. Removing files does not remove Git
   history. Do not retain an exposed key in `SECRET_KEY_FALLBACKS`; existing
   sessions and signed links may be invalidated by rotation.

2. **Build and Start Containers**
   ```bash
   # Build the images
   docker-compose build

   # Start the containers
   docker-compose up -d
   ```

3. **Run Database Migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

4. **Create Superuser**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

5. **Collect Static Files**
   ```bash
   docker-compose exec web python manage.py collectstatic --no-input
   ```

6. **Access the Application**
   - Web Interface: http://localhost
   - Admin Interface: http://localhost/admin
   - API: http://localhost/api/faqs/

### Monitoring Containers
```bash
# View container logs
docker-compose logs -f

# Check container status
docker-compose ps

# Monitor container resources
docker stats
```

## Cloud Deployment Options

### Heroku Deployment

1. **Prerequisites**
   - Heroku CLI installed
   - Heroku account
   - Git repository

2. **Setup Heroku**
   ```bash
   # Login to Heroku
   heroku login

   # Create new app
   heroku create faqmaster-app

   # Add PostgreSQL
   heroku addons:create heroku-postgresql:hobby-dev

   # Add Redis
   heroku addons:create heroku-redis:hobby-dev
   ```

3. **Configure Environment Variables**
   ```bash
   heroku config:set DJANGO_SECRET_KEY=your-secure-secret-key
   heroku config:set DJANGO_SETTINGS_MODULE=faqmaster.settings_prod
   heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
   ```

4. **Deploy**
   ```bash
   git push heroku main

   # Run migrations
   heroku run python manage.py migrate

   # Create superuser
   heroku run python manage.py createsuperuser
   ```

### AWS Elastic Beanstalk Deployment

1. **Prerequisites**
   - AWS account
   - AWS CLI installed
   - EB CLI installed

2. **Initialize EB**
   ```bash
   # Initialize EB project
   eb init -p docker faqmaster

   # Create environment
   eb create faqmaster-env
   ```

3. **Configure Environment Variables**
   Set these in the AWS Console under Configuration → Software → Environment properties:
   - DJANGO_SECRET_KEY
   - DJANGO_SETTINGS_MODULE
   - ALLOWED_HOSTS

4. **Deploy**
   ```bash
   eb deploy
   ```

### DigitalOcean Deployment

1. **Prerequisites**
   - DigitalOcean account
   - doctl CLI installed

2. **Create Resources**
   ```bash
   # Create Docker registry
   doctl registry create faqmaster

   # Create cluster
   doctl kubernetes cluster create faqmaster-cluster
   ```

3. **Deploy Using kubectl**
   ```bash
   # Apply Kubernetes configurations
   kubectl apply -f k8s/
   ```

## Post-Deployment Tasks

1. **Security Checklist**
   - [ ] Set strong Django SECRET_KEY
   - [ ] Enable HTTPS
   - [ ] Configure allowed hosts
   - [ ] Set up backups
   - [ ] Enable logging
   - [ ] Configure monitoring

2. **Performance Optimization**
   - [ ] Configure caching
   - [ ] Enable compression
   - [ ] Set up CDN for static files
   - [ ] Optimize database queries

3. **Monitoring Setup**
   - [ ] Set up error tracking (e.g., Sentry)
   - [ ] Configure performance monitoring
   - [ ] Set up uptime monitoring
   - [ ] Enable logging aggregation

## Troubleshooting

### Common Issues

1. **Container Startup Issues**
   ```bash
   # Check container logs
   docker-compose logs web
   ```

2. **Database Migration Issues**
   ```bash
   # Reset migrations
   docker-compose exec web python manage.py migrate --fake-initial
   ```

3. **Static Files Not Loading**
   ```bash
   # Recollect static files
   docker-compose exec web python manage.py collectstatic --no-input --clear
   ```

### Health Checks

Monitor application health:
```bash
# Check web service
curl http://localhost/health/

# Check Redis
docker-compose exec redis redis-cli ping
```

## Backup and Restore

### Database Backup
```bash
# Create backup
docker-compose exec web python manage.py dumpdata > backup.json

# Restore from backup
docker-compose exec web python manage.py loaddata backup.json
```

### Media Files Backup
```bash
# Backup media files
docker cp $(docker-compose ps -q web):/app/mediafiles ./backup/media

# Restore media files
docker cp ./backup/media $(docker-compose ps -q web):/app/mediafiles
```

## Scaling

### Horizontal Scaling
1. Increase number of web containers:
   ```bash
   docker-compose up -d --scale web=3
   ```

2. Configure load balancer in nginx.conf:
   ```nginx
   upstream faqmaster {
       server web:8000;
       server web_2:8000;
       server web_3:8000;
   }
   ```

## Support and Maintenance

### Regular Maintenance Tasks
1. Update dependencies regularly
2. Monitor system resources
3. Review and rotate logs
4. Backup data regularly
5. Check for security updates

### Monitoring Tools
- Application: Sentry
- Server: Prometheus + Grafana
- Logs: ELK Stack or Papertrail

For additional support or questions, please create an issue in the GitHub repository.
