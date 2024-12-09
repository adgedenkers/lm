from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
import asyncpg
import aiohttp
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create an instance of the FastAPI application
app = FastAPI()

# Function to test database connection asynchronously
async def test_database_connection():
    try:
        # Retrieve the database URL from environment variables
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            return "DATABASE_URL not set in .env file"

        # Connect to the PostgreSQL database using asyncpg
        conn = await asyncpg.connect(database_url)
        await conn.close()  # Close the connection once tested
        return True  # Return True if no exceptions occurred
    except Exception as e:
        # Return the exception message if an error occurred
        return str(e)

# Function to test internet connection asynchronously
async def test_internet_connection():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://www.google.com", timeout=5) as response:
                if response.status == 200:
                    return True
                return f"Error: Received status code {response.status}"
    except Exception as e:
        return str(e)

# Define a model for the POST endpoint
class QueueItem(BaseModel):
    user_id: int
    raw_text: str
    options: dict

# Define a POST endpoint to create a queue item
@app.post("/queue")
async def create_queue_item(item: QueueItem):
    try:
        # Retrieve the database URL from environment variables
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise HTTPException(status_code=500, detail="DATABASE_URL not set in .env file")

        # Connect to the PostgreSQL database using asyncpg
        conn = await asyncpg.connect(database_url)

        # Insert the new queue item into the database and return the ID
        query = """
            INSERT INTO queue (user_id, raw_text, options)
            VALUES ($1, $2, $3)
            RETURNING id;
        """
        queue_id = await conn.fetchval(query, item.user_id, item.raw_text, item.options)
        await conn.close()

        # Return the ID of the newly created queue item
        return {"queue_id": queue_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Define a GET endpoint to check system status
@app.get("/system_status")
async def system_status():
    # Test the database connection
    database_status = await test_database_connection()
    # Test the internet connection
    internet_status = await test_internet_connection()

    # Prepare the status report as a dictionary
    status_report = {
        "database": "Connected" if database_status is True else f"Error: {database_status}",
        "internet": "Connected" if internet_status is True else f"Error: {internet_status}"
    }

    # Return the status report as a JSON response
    return status_report

# Define a GET endpoint to retrieve item details
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    # Return the item ID and optional query parameter as a dictionary
    return {"item_id": item_id, "query": q}
