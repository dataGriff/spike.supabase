import os
from supabase import create_client, Client
from dotenv import load_dotenv  # Import the dotenv library

load_dotenv()  # Load environment variables from the .env file  

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
SUPABASE_BUCKET = os.environ["SUPABASE_BUCKET"]
SUPABASE_JWT_SECRET = os.environ.get("SUPABASE_JWT_SECRET")

if not all([SUPABASE_URL, SUPABASE_KEY, SUPABASE_BUCKET, SUPABASE_JWT_SECRET]):
    raise ValueError("Missing environment variables for Supabase configuration.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)