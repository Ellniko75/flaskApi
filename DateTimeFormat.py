from datetime import datetime


def parseDateTime(date: str):
    date_string = date
    date_format = "%a, %d %b %Y %H:%M:%S %z"
    parsed_date = datetime.strptime(date_string, date_format)
    return parsed_date
