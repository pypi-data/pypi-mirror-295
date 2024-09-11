from flask import Flask, Blueprint
from loguru import logger
from .nocodb import NocodbClient


def init_app(app: Flask, config=None):
    # Check if the provided config is valid
    if not (config is None or isinstance(config, dict)):
        raise ValueError("`config` must be an instance of dict or None")

    # Merge the default config with the provided config
    base_config = app.config.get("NOCODB_CONFIG", {})
    if config:
        base_config.update(config)
    config = base_config

    # Initialize the NocodbClient
    nocodb_client = NocodbClient(
        **config
    )

    # Add the NocodbClient to the app context
    app.extensions["nocodb"] = nocodb_client
    logger.info("Initialized the NocodbClient")

    if config.get("blueprint", True):
        # Register the blueprint
        nocodb_bp = Blueprint("nocodb", __name__, url_prefix="/nocodb")

        @nocodb_bp.route("/projects")
        def projects():
            return nocodb_client.get_projects()

        @nocodb_bp.route("/tables")
        def tables():
            return nocodb_client.get_tables()
        
        @nocodb_bp.route("/tables/<table_id>")
        def get(table_id):
            return nocodb_client.get(table_id)

        app.register_blueprint(nocodb_bp)
        logger.info("Registered the Nocodb blueprint")

