import os
from dotenv import load_dotenv

load_dotenv('.env')

# Use variables
#os.environ["OPENAI_API_KEY"] = os.getenv('openai_key')
os.environ["ANTHROPIC_API_KEY"] = os.getenv('anthropic_key')