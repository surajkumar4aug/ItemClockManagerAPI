
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

mongo_uri = os.getenv("MONGODB_URI")
mongo_db=os.getenv('MONGODB_DATABASE')
# Initialize the MongoDB client
client = AsyncIOMotorClient(mongo_uri)

# Check if the client is connected
if client:
    print("MongoDB client created successfully.")
    try:
        client.admin.command("ping")
        print("Successfully connected to the MongoDB server.")
        db = client[mongo_db]  # Replace with your database name
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
else:
    print("Failed to create MongoDB client.")
