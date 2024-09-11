from datetime import datetime, timezone


def data_time_to_timestamp(datetime_str):
    local_dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    utc_dt = local_dt.replace(tzinfo=timezone.utc)
    timestamp = int(utc_dt.timestamp())
    return timestamp
