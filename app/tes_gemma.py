from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMMA_API_KEY")
)

response = client.models.generate_content(
    model="models/gemma-4-26b-a4b-it",
    contents="Hello, introduce yourself briefly."
)

print(response.text)