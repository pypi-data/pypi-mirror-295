import json
from flask import Flask, Blueprint, request
from celery import Celery, Task, shared_task, states
from celery.result import AsyncResult
from loguru import logger
from .celery_events import Monitor

@shared_task
def hello():
    return "Hello, World!"


def init_app(app: Flask, config=None) -> Celery:
    # Check if the provided config is valid
    if not (config is None or isinstance(config, dict)):
        raise ValueError("`config` must be an instance of dict or None")

    # Merge the default config with the provided config
    base_config = app.config.get("CELERY_CONFIG", {})
    if config:
        base_config.update(config)
    config = base_config

    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(config)
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    logger.info("Initialized the Celery app")

    # 监听事件
    if config.get("enable_events", True):
        monitor = Monitor(celery_app)
        monitor.start()

    if config.get("blueprint", True):
        # Register the blueprint
        bp = Blueprint("celery", __name__, url_prefix="/celery", template_folder="templates")

        def safe_result(result):
            "returns json encodable result"
            try:
                json.dumps(result)
            except TypeError:
                return repr(result)
            return result

        @bp.route("/tasks")
        def tasks():
            return {"tasks": [task.name for task in celery_app.tasks.values()]}

        @bp.route("/send", methods=["POST"])
        def send():
            data = request.json
            if not data:
                return {"error": "No data provided"}, 400

            taskname = data.get("task")
            args = data.get("args", [])
            kwargs = data.get("kwargs", {})
            result = celery_app.send_task(taskname, args=args, kwargs=kwargs)

            return {"task_id": result.task_id, "task_name": taskname, "state": result.state}

        @bp.route("/result/<task_id>")
        def result(task_id):
            result: AsyncResult = celery_app.AsyncResult(task_id)
            logger.info(f"Task {task_id} is in state {result.state} result.result={result.result}")
            response = {"task_id": task_id, "state": result.state}

            if result.state == states.FAILURE:
                response.update({'result': safe_result(result.result),
                                'traceback': result.traceback})
            else:
                response.update({'result': safe_result(result.result)})

            return response

        @bp.route("/config")
        def config():
            return {
                "broker": celery_app.conf.broker_url,
                "result_backend": celery_app.conf.result_backend,
            }

        app.register_blueprint(bp)
        logger.info("Registered the Celery blueprint")

    return celery_app
