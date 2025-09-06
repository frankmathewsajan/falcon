#!/bin/bash

# Django Team Tracker - AWS Elastic Beanstalk Deployment Script
# Run this script to deploy your application to AWS Elastic Beanstalk

echo "🚀 Django Team Tracker - AWS Deployment Script"
echo "=============================================="

# Check if EB CLI is installed
if ! command -v eb &> /dev/null; then
    echo "❌ EB CLI is not installed. Installing..."
    pip install awsebcli
fi

# Check if git repo is initialized
if [ ! -d ".git" ]; then
    echo "📝 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit for deployment"
fi

# Initialize EB if not already done
if [ ! -d ".elasticbeanstalk" ]; then
    echo "🔧 Initializing Elastic Beanstalk..."
    eb init --platform python-3.11 --region us-east-1
fi

# Create environment if it doesn't exist
echo "🌍 Creating/deploying to production environment..."
eb create team-tracker-prod --single-instance --timeout 20 || eb deploy

# Set environment variables
echo "⚙️ Setting environment variables..."
eb setenv SECRET_KEY="$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
eb setenv DEBUG=False

# Get the application URL
echo "🌐 Getting application URL..."
APP_URL=$(eb status | grep "CNAME" | awk '{print $2}')
eb setenv ALLOWED_HOSTS="$APP_URL,localhost,127.0.0.1"

echo "✅ Deployment completed!"
echo "🔗 Your application is available at: http://$APP_URL"
echo "🔐 Admin panel: http://$APP_URL/admin/"
echo "👤 Default admin credentials:"
echo "   Username: admin"
echo "   Password: TempPass123!"
echo ""
echo "⚠️  IMPORTANT: Change the admin password after first login!"
echo ""
echo "📋 Next steps:"
echo "1. Visit your application URL"
echo "2. Login to admin panel and change password"
echo "3. Add your team members and tasks"
echo "4. Configure custom domain (optional)"
echo "5. Set up database backup (recommended)"
