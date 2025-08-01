# Render.com deployment configuration

# Build Command: pip install -r requirements.txt
# Start Command: gunicorn app:app --bind 0.0.0.0:$PORT

# Environment Variables (set in Render dashboard):
# - SECRET_KEY: your-secret-key-here
# - PYTHON_VERSION: 3.12

# Auto-deploy: Yes
# Region: Choose your preferred region
# Instance Type: Free tier is sufficient for basic usage

# Health Check: /
# Port: Uses $PORT environment variable (automatically set by Render)
