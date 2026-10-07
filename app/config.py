import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT/'data'/'job_agent.db'
GENERATED_DIR = ROOT/'generated'
MASTER_RESUME = ROOT/'master_resume.docx'
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY','')
OPENAI_MODEL = os.getenv('OPENAI_MODEL','gpt-6.1-sol')
DAILY_JOB_LIMIT = int(os.getenv('DAILY_JOB_LIMIT','5'))
DISCOVERY_LIMIT = int(os.getenv('DISCOVERY_LIMIT','60'))
MIN_MATCH_SCORE = int(os.getenv('MIN_MATCH_SCORE','70'))
ENABLE_OPENAI_WEB_RESEARCH = os.getenv('ENABLE_OPENAI_WEB_RESEARCH','false').lower()=='true'
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY','')
RAPIDAPI_HOST = os.getenv('RAPIDAPI_HOST','jsearch.p.rapidapi.com')
APP_HOST = os.getenv('APP_HOST','0.0.0.0')
APP_PORT = int(os.getenv('APP_PORT','8000'))
