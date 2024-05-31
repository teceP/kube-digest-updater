import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', 1, 't']
    TASK_INTERVAL_SECONDS = int(os.getenv('TASK_INTERVAL_SECONDS', 600))
    SCHEDULER_API_ENABLED = True


