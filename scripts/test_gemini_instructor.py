import os
import google.generativeai as genai
import instructor
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

client = instructor.from_gemini(
    client=genai.GenerativeModel(
        model_name="models/gemini-2.0-flash",
    )
)

class UserExtract(BaseModel):
    name: str
    age: int

try:
    resp = client.chat.completions.create(
        messages=[
            {"role": "user", "content": "Extract Jason is 25 years old"},
        ],
        response_model=UserExtract,
    )
    print(resp)
except Exception as e:
    print("Error:", e)
