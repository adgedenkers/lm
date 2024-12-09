import os
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Body, Request
from fastapi.responses import HTMLResponse
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise
from models import Base, Queue, Image
from typing import List, Optional
from dotenv import load_dotenv
from contextlib import asynccontextmanager

# Load environment variables from .env file
load_dotenv()

# Get the database connection string from the environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Configure the Tortoise ORM
TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["models"],
            "default_connection": "default",
        }
    },
}

# Define a lifespan context for startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    await Tortoise.init(config=TORTOISE_ORM)
    # Optional: Uncomment this line if you need to auto-create schemas
    # await Tortoise.generate_schemas()

    yield

    # Shutdown logic
    await Tortoise.close_connections()

# Initialize FastAPI app with the new lifespan context
app = FastAPI(lifespan=lifespan)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Home page for the application.
    """
    return """
    <html>
        <head>
            <title>FastAPI with Tortoise ORM</title>
        </head>
        <body>
            <h1>FastAPI with Tortoise ORM</h1>
            <p>Welcome to the FastAPI application with Tortoise ORM.</p>
            <p>Visit the <a href="/docs">API documentation</a> for more information.</p>
        </body>
    </html>
    """

@app.get("/api_status")
async def api_status():
    """
    Endpoint to return the current status of the API.
    """
    return {"message": "system is fully operational"}


@app.post("/queue/")
async def add_text(
    raw_text: Optional[str] = Form(None),
    user_id: Optional[int] = Form(None),
    body: Optional[dict] = Body(None)
):
    """
    Endpoint to add a piece of text to the queue.
    Accepts JSON input or form data.
    """
    if body:
        raw_text = body.get("raw_text")
        user_id = body.get("user_id")
    
    if not raw_text or not user_id:
        raise HTTPException(status_code=400, detail="Missing required fields: raw_text or user_id")

    try:
        queue_item = await Queue.create(raw_text=raw_text, user_id=user_id)
        return {"id": queue_item.id, "status": "Text successfully added to queue."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error adding text: {str(e)}")


@app.post("/upload-images/")
async def upload_images(
    queue_id: int = Form(...), 
    files: List[UploadFile] = File(...)
):
    """
    Endpoint to upload images associated with a particular queue item.
    """
    try:
        for file in files:
            content = await file.read()
            # Save the image to disk or cloud storage (this is an example to store locally)
            with open(f"uploads/{file.filename}", "wb") as f:
                f.write(content)
            
            # Create a record in the Images table
            await Image.create(
                queue_id=queue_id,
                filename=file.filename,
                filepath=f"uploads/{file.filename}",
                filetype=file.content_type,
                filesize=len(content)
            )
        return {"status": "Images successfully uploaded."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error uploading images: {str(e)}")

# Run the application using uvicorn (if running as main script)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
