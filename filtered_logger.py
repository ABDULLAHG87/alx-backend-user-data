#!/usr/bin/env python3
"""A Python script to handle personal data
"""

import re
from typing import List
import logging
from os import environ
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """function to remplace sensitive information in a
    message with redacted value"""

    for m in fields:
        message = re.sub(f"{m}=.*?{separator}",
                         f"{m}={redaction}{separator}", message)
    return message

def get_logger() -> logging.Logger:
    """
    Returns a Logger object for handling Personal Data"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)

    return logger

def get_db() -> mysql.connector.connection.MYSQLConnection:
    """A function that return MYSQLConnection object for
    accessing Personal Database"""
    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")

    con = mysql.connector.connection.MYSQLConnection(user=username,
                                                         password=password,
                                                         host=host,
                                                         database=db_name)
    return con


def main():
    """ main function"""
    db = get_db
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    field_names = [n[0] for n in cursor.description]

    logger = get_logger()

    for row in cursor:
        str_row = "".join(f"{m}={str(r)};" for r,
                          m in zip(row, field_names))
        logger.info(str_row.strip())

    cursor.close()
    db.close()


class RedactingFormatter(logging.Formatter):
    """Function for redacting formatter class for filter PII_FIELDS
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """constructor method for redactingFormatter"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Function that format specified log record """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


if __name__ == "__main__":
    main()
