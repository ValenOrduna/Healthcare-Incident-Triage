import logging
import sys
import structlog

def renaming_renderer(logger, name, event_dict):
    # Transformamos las propiedades a español
    event_dict["evento"] = event_dict.pop("event", None)
    event_dict["nivel"] = event_dict.pop("level", None)
    event_dict["fecha"] = event_dict.pop("timestamp", None)
    return event_dict

def setup_logging():
    logging.basicConfig(
        format="%(message)s",
        filename="app.log",
        level=logging.INFO,
        filemode='a'
    )

    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            renaming_renderer,
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )