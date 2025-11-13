from dotenv import load_dotenv
import os   
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if  not OPENAI_API_KEY:
    raise ValueError("API keys are not set in the environment variables.")

