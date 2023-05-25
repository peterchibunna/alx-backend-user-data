#!/usr/bin/env python3
"""Module 0x00. Personal data
"""
import logging
import re
from typing import List, Iterable

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password',)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """returns message obfuscated"""
    return separator.join([(re.sub(r'(?<==).*$', redaction, i)) if re.match(
        r'^[^=]*', i)[0] in fields else i for i in message.split(separator)])


def get_logger() -> logging.Logger:
    logger = logging.getLogger("get_logger")
    logger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: Iterable) -> None:
        """Initialize the Redacter Formatter
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self._fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the message
        """
        m = super(RedactingFormatter, self).format(record)
        txt = filter_datum(self._fields, self.REDACTION, m, self.SEPARATOR)
        return txt
