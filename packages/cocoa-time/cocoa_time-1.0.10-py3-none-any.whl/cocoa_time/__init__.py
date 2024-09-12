# 27/08/2024 - 19:32:47
# v 1.1.0

import math, re
from datetime import datetime, timedelta

def to_datetime(timestamp: int | str):
    """
    Convert cocoa timestamp to datetime
    
    :param int | str timestamp: The given cocoa timestamp int or string that contains only numbers to be converted into datetime
    """
    if not isinstance(timestamp, int | str) or type(timestamp) == bool:
        raise TypeError("timestamp type is not an int or a string that contains numbers only")
    if type(timestamp) == str: 
        if re.match(r"^\d+$", timestamp):
            timestamp = int(timestamp)
        else:
            raise ValueError("timestamp string is not a number")
    digits = int(math.log10(timestamp)) + 1
    if digits > 9:
        timestamp = timestamp / 100
    return datetime(2001, 1, 1) + timedelta(seconds=timestamp)

def to_unix_timestamp(timestamp: int | str):
    """
    Convert cocoa timestamp to unix timestamp
    
    :param int | str timestamp: The given cocoa timestamp int or string that contains only numbers to be converted into unix timestamp
    """
    if not isinstance(timestamp, int | str) or type(timestamp) == bool:
        raise TypeError("timestamp type is not an int or a string that contains numbers only")
    if type(timestamp) == str: 
        if re.match(r"^\d+$", timestamp):
            timestamp = int(timestamp)
        else:
            raise ValueError("timestamp string is not a number")
    digits = int(math.log10(timestamp)) + 1
    if digits > 9:
        timestamp = timestamp / 100
    return math.floor(978307200 + timestamp)

def from_unix_timestamp(timestamp: int | str, centiseconds: bool = False):
    """
    Convert unix timestamp into cocoa timestamp
    
    :param int | str timestamp: The given unix timestamp int or string that contains only numbers to be converted into cocoa timestamp
    :param bool centiseconds: Add 2 additional digits to the timestamp that contain the centiseconds of the time point `(default False)`
    """
    if not isinstance(timestamp, int | str) or type(timestamp) == bool:
        raise TypeError("timestamp type is not an int or a string that contains numbers only")
    if type(timestamp) == str: 
        if re.match(r"^\d+$", timestamp):
            timestamp = int(timestamp)
        else:
            raise ValueError("timestamp string is not a number")
    if timestamp < 978307200:
        raise ValueError("timestamp value is smaller than 978307200")
    if type(centiseconds) != bool:
        raise TypeError("centiseconds is not a bool")
    digits = int(math.log10(timestamp)) + 1
    if digits > 10:
        timestamp = timestamp / 100
    if not centiseconds:
        timestamp = math.floor(timestamp)
    cococa = timestamp - 978307200
    return math.floor(cococa * (100 if centiseconds else 1))

def from_datetime(date: datetime | str, centiseconds: bool = False, format: str | None = None):
    """
    Convert datetime or string to cocoa timestamp
    
    :param datetime | str date: The given datetime or string that contains a datetime to be converted into cocoa timestamp
    :param bool centiseconds: Add 2 additional digits to the timestamp that contain the centiseconds of the time point `(default False)`
    :param str | None format: Format date string as datetime: A `valid format string` that matches the date string has to be provided `or kept as None` if date is datetime `(default None)`
    """
    if not isinstance(date, datetime | str):
        raise TypeError("date is not datetime or a string")
    else:
        if type(date) == str:
            if not isinstance(format, str):
                raise TypeError("format is not a string")
            date = datetime.strptime(date, format)
        elif type(date) == datetime and format != None:
            raise ValueError("datetime is not a string to be formatted format should be set to none")
    if type(centiseconds) != bool:
        raise TypeError("centiseconds is not a bool")
    return math.floor((date - datetime(2001, 1, 1)).total_seconds() * (100 if centiseconds else 1))