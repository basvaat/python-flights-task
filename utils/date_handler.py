from datetime import datetime

class DateHandler:
    """
    Handles dates, formats datetime and calculates timedelta.
    """
    def __init__(self) -> None:
        pass

    def calculate_date_difference(first_date, next_date):
        return next_date - first_date       

    def convert_datetime(date):
        return datetime.fromisoformat(date)

    def convert_timedelta_to_datetime(timedelta):
        return str(timedelta)
