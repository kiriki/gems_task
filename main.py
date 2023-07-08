from __future__ import annotations

import multiprocessing
import os
from typing import TYPE_CHECKING

from gunicorn.app.base import BaseApplication

from django.core.wsgi import get_wsgi_application

if TYPE_CHECKING:
    from collections.abc import Callable

    from django.core.handlers.wsgi import WSGIHandler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gems_task.settings')
django_app = get_wsgi_application()


def number_of_workers() -> int:
    return (multiprocessing.cpu_count() * 2) + 1


class PyApplication(BaseApplication):
    def __init__(self, app: WSGIHandler, options: dict | None = None) -> None:
        self.application = app
        self.options = options or {}
        super().__init__()

    def load_config(self) -> None:
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self) -> Callable:
        return self.application


if __name__ == '__main__':
    port = int(os.environ.get('APP_API_PORT', '8000'))
    options = {
        'bind': f'0.0.0.0:{port}',
        'workers': os.environ.get('APP_API_WORKERS_COUNT', 2),
        'accesslog': os.environ.get('APP_API_ACCESS_LOG', '-'),
        'errorlog': os.environ.get('APP_API_ERROR_LOG', '-'),
        'timeout': 120,
    }
    application = PyApplication(django_app, options)
    application.run()
