# Railway Deployment Guide

This guide will help you deploy the Django application to Railway using the CLI.

## Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **Railway CLI**: Install the Railway CLI
   ```bash
   # Windows (PowerShell)
   iwr https://railway.app/install.ps1 | iex
   
   # macOS/Linux
   curl -fsSL https://railway.app/install.sh | sh
   ```

3. **Git**: Ensure your project is in a Git repository

## Step 1: Login to Railway

```bash
railway login
```

This will open your browser to authenticate with Railway.

## Step 2: Initialize Railway Project

Navigate to the server directory:

```bash
cd server
railway init
```

This will:
- Create a new Railway project (or link to existing one)
- Generate a `railway.toml` configuration file

## Step 3: Add PostgreSQL Database

Railway provides PostgreSQL as a service. Add it to your project:

```bash
railway add postgresql
```

This will automatically:
- Create a PostgreSQL database
- Set the `DATABASE_URL` environment variable
- Link it to your Django service

## Step 4: Set Environment Variables

Set the required environment variables:

```bash
# Set Django secret key (generate a new one for production!)
railway variables set SECRET_KEY="your-secret-key-here"

# Set DEBUG to False for production
railway variables set DEBUG="False"

# Optional: Set CORS allowed origins if you have a frontend
railway variables set CORS_ALLOWED_ORIGINS="https://your-frontend-domain.com"
```

**Important**: Generate a secure SECRET_KEY:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Step 5: Deploy

Deploy your application:

```bash
railway up
```

This will:
- Build your application using the Dockerfile or Nixpacks
- Run database migrations automatically (via entrypoint.sh)
- Start your Django application with Gunicorn

## Step 6: Generate Public Domain (Optional)

Railway provides a default domain, but you can generate a custom one:

```bash
railway domain
```

This will create a public domain like `your-app-name.up.railway.app`

## Step 7: Run Database Migrations

If migrations don't run automatically, run them manually:

```bash
railway run python manage.py migrate
```

## Step 8: Create Superuser (Optional)

Create a Django admin superuser:

```bash
railway run python manage.py createsuperuser
```

## Step 9: View Logs

Monitor your application logs:

```bash
railway logs
```

## Step 10: Open Your Application

Open your deployed application:

```bash
railway open
```

## Project Structure

The deployment expects:
- `server/Procfile` - Defines the web process
- `server/railway.json` - Railway configuration (optional)
- `server/Dockerfile` - Docker configuration (Railway can use this)
- `server/requirements.txt` - Python dependencies
- `server/entrypoint.sh` - Runs migrations and collects static files

## Environment Variables Reference

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Django secret key | Yes |
| `DEBUG` | Debug mode (set to "False" in production) | Yes |
| `DATABASE_URL` | PostgreSQL connection string | Auto-set by Railway |
| `PORT` | Port to bind to | Auto-set by Railway |
| `RAILWAY_PUBLIC_DOMAIN` | Public domain URL | Auto-set by Railway |
| `RAILWAY_ENVIRONMENT` | Environment name | Auto-set by Railway |

## Troubleshooting

### Database Connection Issues

If you see database connection errors:
1. Ensure PostgreSQL service is added: `railway add postgresql`
2. Check DATABASE_URL is set: `railway variables`
3. Verify migrations ran: `railway run python manage.py migrate`

### Static Files Not Loading

If static files aren't loading:
1. Ensure WhiteNoise is in requirements.txt
2. Check static files are collected: `railway run python manage.py collectstatic --noinput`

### Application Won't Start

Check logs for errors:
```bash
railway logs --tail
```

Common issues:
- Missing environment variables
- Database migrations failed
- Port binding issues (ensure using `$PORT` variable)

## Updating Your Application

To update your deployed application:

```bash
# Make your changes locally
git add .
git commit -m "Your changes"

# Deploy to Railway
railway up
```

## Additional Commands

```bash
# View all services
railway status

# View environment variables
railway variables

# Connect to database shell
railway connect postgresql

# Run Django shell
railway run python manage.py shell

# Run Django management commands
railway run python manage.py <command>
```

## Next Steps

1. Set up a custom domain (optional)
2. Configure CI/CD for automatic deployments
3. Set up monitoring and alerts
4. Configure backups for your PostgreSQL database

For more information, visit [Railway Documentation](https://docs.railway.app)

