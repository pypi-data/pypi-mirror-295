from typing import Any

logger: Any = None

def init_logger(logger_: Any) -> None:
    global logger

    logger = logger_