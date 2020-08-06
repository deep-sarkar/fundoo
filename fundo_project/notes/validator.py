from datetime import datetime
from .exceptions import PassedTimeException

def validate_time(time_data):
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    if time_data < current_time:
        raise PassedTimeException