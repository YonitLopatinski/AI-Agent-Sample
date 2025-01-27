import os

from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = ''
os.environ["OPENAI_API_BASE"] = 'https://api.groq.com/openai/v1'
