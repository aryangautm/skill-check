# Deployment Guide

This guide covers deploying the Skill Check API to production environments.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Docker Deployment](#docker-deployment)
4. [Production Deployment](#production-deployment)
5. [Security Considerations](#security-considerations)

## Prerequisites

- Python 3.9+
- PostgreSQL 12+
- Google Gemini API Key
- Domain name (for production)
- SSL certificate (for production)

## Environment Setup

### 1. Create Production Environment File

```bash
cp .env.example .env
```

Edit `.env` with production values:

```env
DATABASE_URL=postgresql://username:password@db-host:5432/skillcheck_prod
GEMINI_API_KEY=your_production_gemini_api_key
SECRET_KEY=your_secure_secret_key_here
ENVIRONMENT=production
```

### 2. Generate a Secure Secret Key

```python
import secrets
print(secrets.token_urlsafe(32))
```

## Docker Deployment

### 1. Create Dockerfile

Create `Dockerfile` in the project root:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Create docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: skillcheck
      POSTGRES_USER: skillcheck_user
      POSTGRES_PASSWORD: secure_password_here
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U skillcheck_user -d skillcheck"]
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://skillcheck_user:secure_password_here@db:5432/skillcheck
      GEMINI_API_KEY: ${GEMINI_API_KEY}
      SECRET_KEY: ${SECRET_KEY}
      ENVIRONMENT: production
    depends_on:
      db:
        condition: service_healthy
    command: >
      sh -c "
        alembic upgrade head &&
        uvicorn app.main:app --host 0.0.0.0 --port 8000
      "

volumes:
  postgres_data:
```

### 3. Deploy with Docker Compose

```bash
# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

## Production Deployment

### Option 1: Deploy to Cloud Platform (e.g., Heroku, Railway)

#### Railway Deployment

1. Install Railway CLI:
```bash
npm install -g @railway/cli
```

2. Login and deploy:
```bash
railway login
railway init
railway up
```

3. Add PostgreSQL addon:
```bash
railway add postgresql
```

4. Set environment variables:
```bash
railway variables set GEMINI_API_KEY=your_key
railway variables set SECRET_KEY=your_secret
```

### Option 2: Deploy to VPS (Ubuntu/Debian)

#### 1. Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and PostgreSQL
sudo apt install -y python3.11 python3-pip postgresql postgresql-contrib nginx

# Install supervisor for process management
sudo apt install -y supervisor
```

#### 2. Setup PostgreSQL

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE skillcheck;
CREATE USER skillcheck_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE skillcheck TO skillcheck_user;
\q
```

#### 3. Setup Application

```bash
# Clone repository
cd /var/www
sudo git clone https://github.com/yourusername/skill-check.git
cd skill-check

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
sudo nano .env
# Add your configuration

# Run database migrations
alembic upgrade head
```

#### 4. Configure Supervisor

Create `/etc/supervisor/conf.d/skillcheck.conf`:

```ini
[program:skillcheck]
directory=/var/www/skill-check
command=/var/www/skill-check/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 4
user=www-data
autostart=true
autorestart=true
stdout_logfile=/var/log/skillcheck/access.log
stderr_logfile=/var/log/skillcheck/error.log
environment=PATH="/var/www/skill-check/venv/bin"
```

```bash
# Create log directory
sudo mkdir -p /var/log/skillcheck
sudo chown www-data:www-data /var/log/skillcheck

# Reload supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start skillcheck
```

#### 5. Configure Nginx

Create `/etc/nginx/sites-available/skillcheck`:

```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    client_max_body_size 10M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/skillcheck /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 6. Setup SSL with Let's Encrypt

```bash
# Install certbot
sudo apt install -y certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d api.yourdomain.com
```

### Option 3: Deploy to AWS EC2

1. Launch EC2 instance (Ubuntu 22.04)
2. Configure security groups (allow ports 80, 443, 22)
3. Follow VPS deployment steps above
4. Use Amazon RDS for PostgreSQL (recommended)

### Option 4: Deploy to Google Cloud Run

```bash
# Install gcloud CLI
# Build and push container
gcloud builds submit --tag gcr.io/PROJECT_ID/skillcheck

# Deploy to Cloud Run
gcloud run deploy skillcheck \
  --image gcr.io/PROJECT_ID/skillcheck \
  --platform managed \
  --region us-central1 \
  --set-env-vars GEMINI_API_KEY=$GEMINI_API_KEY,SECRET_KEY=$SECRET_KEY
```

## Database Migrations

Always run migrations before deploying:

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one version
alembic downgrade -1
```

## Monitoring and Logging

### 1. Application Logging

Add logging to production settings:

```python
# app/core/config.py
import logging

if settings.environment == "production":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
```

### 2. Health Check Monitoring

Use the `/health` endpoint for monitoring:

```bash
curl http://api.yourdomain.com/health
```

### 3. Error Tracking

Consider integrating:
- Sentry for error tracking
- DataDog for monitoring
- CloudWatch (AWS)
- Stackdriver (GCP)

## Security Considerations

### 1. Update CORS Settings

In production, update `app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific domains only
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### 2. Environment Variables

Never commit `.env` files. Use:
- Docker secrets
- Cloud platform environment variables
- Secret management services (AWS Secrets Manager, GCP Secret Manager)

### 3. Database Security

- Use strong passwords
- Enable SSL for database connections
- Regular backups
- Restrict database access to application servers only

### 4. API Security

Consider adding:
- Rate limiting (e.g., `slowapi`)
- API key authentication
- JWT tokens for user sessions
- Input validation and sanitization

### 5. File Upload Security

- Limit file sizes
- Validate file types
- Scan for malware
- Store files in secure locations

## Backup Strategy

### Database Backups

```bash
# Manual backup
pg_dump -U skillcheck_user skillcheck > backup_$(date +%Y%m%d).sql

# Automated daily backup (cron)
0 2 * * * pg_dump -U skillcheck_user skillcheck > /backups/skillcheck_$(date +\%Y\%m\%d).sql
```

### Application Backups

- Use version control (Git)
- Tag releases
- Keep deployment artifacts

## Scaling Considerations

### Horizontal Scaling

- Use load balancer (Nginx, AWS ALB)
- Deploy multiple API instances
- Share PostgreSQL database

### Vertical Scaling

- Increase server resources
- Optimize database queries
- Add database indexes
- Use connection pooling

### Caching

Consider adding Redis for:
- Session storage
- API response caching
- Rate limiting

## Troubleshooting

### Common Issues

1. **Database connection errors**
   - Check DATABASE_URL
   - Verify PostgreSQL is running
   - Check network connectivity

2. **API key errors**
   - Verify GEMINI_API_KEY is set
   - Check API key validity
   - Review API quota limits

3. **File upload failures**
   - Check file size limits
   - Verify file permissions
   - Review disk space

### Logs Location

- Supervisor logs: `/var/log/skillcheck/`
- Nginx logs: `/var/log/nginx/`
- PostgreSQL logs: `/var/log/postgresql/`

## Performance Optimization

1. **Database Optimization**
   - Add indexes on frequently queried columns
   - Use connection pooling
   - Optimize queries

2. **API Optimization**
   - Enable Gzip compression
   - Use async operations
   - Implement caching

3. **AI Service Optimization**
   - Implement request queuing
   - Add timeout handling
   - Cache common responses
