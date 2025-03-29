from supabase import create_client, Client
import os
from dotenv import load_dotenv  # Import the dotenv library

load_dotenv()  # Load environment variables from the .env file

supabase: Client = create_client(supabase_url=os.environ["SUPABASE_URL"], supabase_key=os.environ["SUPABASE_KEY"])

# database

# # insert a row
# data = {"first_name": "John Doe"}
# response = supabase.table("demo-table").insert(data).execute()
# #print(response)

# # update a row
# data = {"first_name": "Jane Doe"}
# response = supabase.table("demo-table").update(data).eq('id',2).execute()
# #print(response)

# # update a row
# data = {"first_name": "Jane Doe"}
# response = supabase.table("demo-table").delete().gte('id',2).execute()
# #print(response)

# results = supabase.table("demo-table").select("*").execute()
# print(results)

# get image from storage

response = supabase.storage.from_("demo-bucket").get_public_url("image1.jpg")

print(response)