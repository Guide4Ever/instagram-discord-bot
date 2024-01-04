import datetime

# example: 2024-01-01 00:00:00
def get_today_time_midnight():
    return datetime.datetime.combine(datetime.datetime.today(), datetime.time.min)