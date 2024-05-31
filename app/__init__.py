from flask import Flask
from .routes import register_routes
from .extensions import scheduler, init_scheduler
from .config import Config
from .tasks import periodic_fetch_annotated_resources
import nest_asyncio

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_scheduler(app)
    register_routes(app)
    scheduler.add_job(id='periodic_task', func=lambda: periodic_fetch_annotated_resources(app), trigger='interval',
                      seconds=app.config['TASK_INTERVAL_SECONDS'])
    nest_asyncio.apply()
    return app
