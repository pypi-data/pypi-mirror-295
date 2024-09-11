import logging
from typing import Any, Dict

import orjson


class SLogger:
    def __init__(self, logger: logging.Logger, format: str = "plain"):
        """
        Initialize the logger with the specified format: 'plain' or 'json'.
        'plain' will output logs in a simple text format, and 'json' will output logs in JSON format.
        """
        self.logger = logger
        self.context = {}
        self.format = format

    def with_fields(self, **fields) -> 'SLogger':
        """
        Returns a new SLogger instance with additional fields added to the context.
        If None is passed as fields, it will be ignored.
        """
        # Treat None as an empty dictionary
        if fields is None:
            fields = {}
        
        new_logger = SLogger(self.logger, self.format)
        new_logger.context = {**self.context, **fields}
        return new_logger


    def log(self, level: int, msg: str, **extra_fields):
        """
        Logs a message at the specified level, including any context fields.
        Switches between 'plain' and 'json' format based on the selected logging format.
        """
        log_context = {**self.context, **extra_fields}
        if self.format == "json":
            log_message = self._format_as_json(msg, log_context)
        else:
            log_message = self._format_as_plain(msg, log_context)
        self.logger.log(level, log_message)

    def _format_as_json(self, msg: str, context: Dict[str, Any]) -> str:
        """
        Formats the log message and context as a JSON string.
        """
        log_entry = {
            "message": msg,
            "context": context if context else {}
        }
        return orjson.dumps(log_entry).decode("utf-8")

    def _format_as_plain(self, msg: str, context: Dict[str, Any]) -> str:
        """
        Formats the log message and context as a simple plain text string.
        """
        context_str = f"{context}" if context else "{}"
        return f"{msg} {context_str}".strip() if msg else context_str


    def debug(self, msg: str, **extra_fields):
        self.log(logging.DEBUG, msg, **extra_fields)

    def info(self, msg: str, **extra_fields):
        self.log(logging.INFO, msg, **extra_fields)

    def warning(self, msg: str, **extra_fields):
        self.log(logging.WARNING, msg, **extra_fields)

    def error(self, msg: str, **extra_fields):
        self.log(logging.ERROR, msg, **extra_fields)

    def critical(self, msg: str, **extra_fields):
        self.log(logging.CRITICAL, msg, **extra_fields)

    def __repr__(self) -> str:
        return f"<SLogger context={self.context}>"
