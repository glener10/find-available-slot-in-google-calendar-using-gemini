import datetime
import tzlocal

def format_datetime(dt_str):
  dt = datetime.datetime.fromisoformat(dt_str)
  return dt.strftime("%Y-%m-%d %H:%M")

def get_local_timezone_offset():
  offset = datetime.datetime.now().astimezone().utcoffset()
  hours = int(offset.total_seconds() // 3600)
  minutes = int((offset.total_seconds() % 3600) // 60)
  return f"{hours:+03d}:{abs(minutes):02d}"

def get_local_timezone_name():
  return tzlocal.get_localzone()