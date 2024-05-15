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
        stream_handler.setFormatter(redactingFormatter(list(PII_FIELDS)))
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
