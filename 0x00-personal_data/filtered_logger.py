#!/usr/bin/env python3
"""
A function that returns the log message obfuscated:
"""
import re


def filter_datum(fields, redaction, message, separator):
    """
    A function that returns the log message that is obsure
    """
    message = re.sub(r"password=.*?;", f"password={redaction};", message)
    message = re.sub(
        r"date_of_birth=.*?;", f"date_of_birth={redaction};", message)
    return message
