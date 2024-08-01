#!/usr/bin/env python3
"""
A function that returns the log message obfuscated:
"""
import re
import logging
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    A function that returns the log message that is obsure
    """
    for field in fields:
        message = re.sub(rf"{field}=.+?{separator}",
                         f"{field}={redaction}{separator}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Constructor method
            """
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Redacting Formatter method
            """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)
