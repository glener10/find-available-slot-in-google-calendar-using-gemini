import os

from dotenv import load_dotenv
from google import genai

from src.utils.date import get_local_timezone_offset

MODEL = "gemini-2.0-flash"

def get_api_key():
  load_dotenv()
  api_key = os.getenv('API_KEY')
  if not api_key:
    raise Exception("❌ missing API_KEY in .env")
  return api_key

def find_next_available_slot(events, attendance_time_start, attendance_time_end, attendance_minutes_duration):
    client = genai.Client(api_key=get_api_key())
    print(events)
    prompt = (
      f"You are an event scheduling agent. Your task is to find the next available time slot to schedule an event. "
      f"Working hours are from {attendance_time_start} to {attendance_time_end}, and you can only find slots within this interval. "
      f"The event must last {attendance_minutes_duration} minutes. "
      f"You cannot return a time when there are already registered events. "
      f"pay attention to the start and end time of each event and timezone, the calendar with the events already occupied are these: {events}. "
      f"Respond ONLY with the date and time of the next available slot in the ISO 8601 format 'YYYY-MM-DDTHH:MM:SS.sss{get_local_timezone_offset()}'. "
      f"I will use your response directly in new Date(), so it must be ONLY that, nothing else. "
      f"If there are no available slots, respond with 'no available slots'. "
    )
    return client.models.generate_content(
      model=MODEL,
      contents=[prompt]).text.strip()