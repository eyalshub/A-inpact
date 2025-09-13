import os
from dotenv import load_dotenv
import google.generativeai as genai

# טוען את קובץ .env
load_dotenv()

# קובע את המפתח
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# בוחר מודל – אפשר "gemini-1.5-flash" (מהיר) או "gemini-1.5-pro" (מדויק)
model = genai.GenerativeModel("gemini-1.5-flash")

# שולח בקשה
response = model.generate_content(
    "כתוב לי דוח בעברית על רישוי מסעדות"
)

print(response.text)
