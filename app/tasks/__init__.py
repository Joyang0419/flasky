from celery import Celery
import os
from app import create_app


def make_celery(app):
    celery = Celery(app.import_name, config_source='celeryconfig')

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


flask_app = create_app(os.getenv('FLASK_CONFIG') or 'default', celery=True)
celery = make_celery(flask_app)

# task加進來
from .add_together import add_together
from .send_email import send_email
