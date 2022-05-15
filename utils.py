import datetime


def range_date(start_date_str, end_date_str):
    start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")
    delta = datetime.timedelta(days=1)
    while start_date <= end_date:
        yield start_date.strftime('%Y-%m-%d')
        start_date += delta
