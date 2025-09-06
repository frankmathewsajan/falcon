# AWS Elastic Beanstalk Deployment Guide

This guide will help you deploy the Django Team Tracker application to AWS Elastic Beanstalk.

## 📋 Prerequisites

1. **AWS Account** with appropriate permissions
2. **AWS CLI** installed and configured
3. **EB CLI** installed (`pip install awsebcli`)
4. **Git** repository initialized

## 🚀 Deployment Steps

### 1. Prepare Your Application

The application is already configured with:
- ✅ `requirements.txt` - Python dependencies
- ✅ `Procfile` - Application startup command
- ✅ `.ebextensions/` - EB configuration files
- ✅ Production-ready Django settings

### 2. Initialize Elastic Beanstalk

```bash
# Navigate to your project directory
cd /path/to/your/falcon/project

# Initialize EB application
eb init

# Follow the prompts:
# - Select region (e.g., us-east-1)
# - Choose "Create new application"
# - Application name: team-tracker-falcon
# - Platform: Python
# - Platform version: Python 3.11 (or latest)
# - Setup SSH: No (unless you need it)
```

### 3. Create Environment

```bash
# Create and deploy environment
eb create team-tracker-prod

# This will:
# - Create EC2 instances
# - Set up load balancer
# - Deploy your application
# - Run migrations automatically
```

### 4. Configure Environment Variables

```bash
# Set environment variables for production
eb setenv SECRET_KEY="your-super-secret-key-here"
eb setenv DEBUG=False
eb setenv ALLOWED_HOSTS="your-app-url.elasticbeanstalk.com"

# Optional: Database URL (if using RDS)
# eb setenv DATABASE_URL="postgres://user:pass@host:port/dbname"
```

### 5. Deploy Updates

```bash
# Deploy changes
eb deploy

# Check application status
eb status

# View application logs
eb logs

# Open application in browser
eb open
```

## 🗃️ Database Setup

### Option 1: SQLite (Development/Testing)
- Default configuration
- Data stored on EC2 instance
- ⚠️ Data lost on instance termination

### Option 2: RDS PostgreSQL (Recommended for Production)

```bash
# Add RDS database to your environment
eb console

# In AWS Console:
# 1. Go to Configuration > Database
# 2. Click "Edit"
# 3. Choose "PostgreSQL"
# 4. Set username/password
# 5. Apply changes
```

EB will automatically set the `DATABASE_URL` environment variable.

## 🔧 Configuration Files

### `requirements.txt`
```
Django>=5.2.6
django-jazzmin>=3.0.1
psycopg2-binary>=2.9.10
dj-database-url>=3.0.1
python-dotenv>=1.1.1
gunicorn>=21.2.0
whitenoise>=6.6.0
boto3>=1.35.0
django-storages>=1.14.0
awsebcli>=3.25
```

### `Procfile`
```
web: gunicorn falcon.wsgi:application --bind 0.0.0.0:$PORT
```

### `.ebextensions/01_django.config`
```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: falcon.wsgi:application
  aws:elasticbeanstalk:application:environment:
    DJANGO_SETTINGS_MODULE: falcon.settings
    PYTHONPATH: /var/app/current:$PYTHONPATH
  aws:elasticbeanstalk:container:python:staticfiles:
    /static/: static/
```

### `.ebextensions/02_python.config`
```yaml
container_commands:
  01_migrate:
    command: "django-admin.py migrate"
    leader_only: true
  02_collectstatic:
    command: "django-admin.py collectstatic --noinput"

option_settings:
  aws:elasticbeanstalk:application:environment:
    DJANGO_SETTINGS_MODULE: falcon.settings
```

## 🛡️ Security Features

### Production Settings Automatically Applied:
- ✅ SSL/TLS enforcement
- ✅ Secure cookies
- ✅ XSS protection
- ✅ Content type sniffing protection
- ✅ HSTS headers
- ✅ CSRF protection

### Environment Variables Required:
- `SECRET_KEY` - Django secret key
- `DEBUG` - Set to `False` for production
- `ALLOWED_HOSTS` - Your domain/EB URL

## 📁 Static Files

Static files are handled by **WhiteNoise** middleware:
- ✅ Automatic compression
- ✅ Caching headers
- ✅ No S3 required for basic setup

## 🔍 Monitoring & Logs

```bash
# View real-time logs
eb logs --all

# Check application health
eb health

# View environment information
eb status
```

## 🚨 Troubleshooting

### Common Issues:

1. **502 Bad Gateway**
   ```bash
   eb logs
   # Check for Python/Django errors
   ```

2. **Static Files Not Loading**
   ```bash
   eb ssh
   sudo cat /opt/python/log/collectstatic.log
   ```

3. **Database Connection Errors**
   ```bash
   eb printenv
   # Verify DATABASE_URL is set
   ```

### Useful Commands:

```bash
# Restart application
eb restart

# SSH into instance
eb ssh

# Terminate environment (DANGER!)
eb terminate

# List all environments
eb list
```

## 💰 Cost Optimization

### Free Tier Eligible:
- t3.micro instance
- Single instance (no load balancer)
- 750 hours/month free

### Production Recommendations:
- Use RDS for database
- Enable auto-scaling
- Set up CloudWatch monitoring
- Configure regular backups

## 🎯 Post-Deployment Checklist

- [ ] Application loads successfully
- [ ] Admin panel accessible at `/admin/`
- [ ] Static files loading correctly
- [ ] Database migrations applied
- [ ] SSL certificate configured (optional)
- [ ] Custom domain configured (optional)
- [ ] Monitoring set up
- [ ] Backup strategy implemented

## 📞 Support

For issues:
1. Check EB logs: `eb logs`
2. Review AWS documentation
3. Check Django deployment best practices
4. Monitor AWS health dashboard

---

**Happy Deploying! 🚀**