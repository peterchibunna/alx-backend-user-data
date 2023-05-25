#!/usr/bin/env python3
"""
Module 0x00. Personal data
"""
import logging
import mysql.connector
import os
import re
from typing import List, Iterable

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password',)


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """returns message obfuscated"""
    return separator.join([(re.sub(r'(?<==).*$', redaction, i)) if re.match(
        r'^[^=]*', i)[0] in fields else i for i in message.split(separator)])


def get_logger() -> logging.Logger:
    """create and return a logger instance
    """
    logger = logging.getLogger("get_logger")
    logger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns and instance of a database connection
    """
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "m!s3rv3R")
    connection = mysql.connector.connect(
        host=host, port=3306, user=db_user, password=db_password,
        database=db_name,
    )
    return connection


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


def main() -> None:
    """This is probably the main thing we have been driving towards
    """
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users;")
    formatter = RedactingFormatter(
        fields=("name", "email", "phone", "ssn", "password"))
    logger = get_logger()

    for row in cursor:
        message = ''
        for item in row:
            message += '{}={}{}'.format(item, row[item], formatter.SEPARATOR)
        args = ("user_data", logging.INFO, None, None, message, None, None)
        record = logging.LogRecord(*args)
        logger.handle(record)
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
