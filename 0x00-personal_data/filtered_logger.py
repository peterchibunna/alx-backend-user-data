#!/usr/bin/env python3
"""Module 0x00. Personal data
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """returns message obfuscated"""
    return separator.join([(re.sub(r'(?<==).*$', redaction, i)) if re.match(
        r'^[^=]*', i)[0] in fields else i for i in message.split(separator)])
