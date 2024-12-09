import dotenv
import os

# Load the Environment Variables
dotenv.load_dotenv(dotenv.find_dotenv())

# Set the Directory
if DIR is None:
    DIR = os.path.dirname(os.path.abspath(__file__))

cd $DIR
python -m venv .venv
source .venv/bin/activate

# Install the Python Requirements
# 3.8 install:  pip install tortoise-orm python-multipart fastapi uvicorn pydantic