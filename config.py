import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    # Use /tmp/site.db for serverless environments (writable)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:////tmp/site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

