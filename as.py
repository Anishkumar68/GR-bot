import os
from dotenv import load_dotenv

load_dotenv()

print("OpenAI API Key:", os.getenv("OPENAI_API_KEY"))
