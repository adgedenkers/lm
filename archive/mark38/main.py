from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from models import Shoe, Gender, ListingStatus, PaymentStatus, ShippingStatus

# Initialize FastAPI app
app = FastAPI(
    title="Shoe Inventory API",
    description="API for managing a shoe inventory",
    version="1.0.0",
)

# Pydantic models for Shoe
Shoe_Pydantic = pydantic_model_creator(Shoe, name="Shoe")
ShoeIn_Pydantic = pydantic_model_creator(Shoe, name="ShoeIn", exclude_readonly=True)

# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Shoe Inventory API"}

# Endpoint to get all shoes
@app.get("/shoes/", response_model=list[Shoe_Pydantic])
async def get_shoes():
    return await Shoe_Pydantic.from_queryset(Shoe.all())

# Endpoint to get a single shoe by ID
@app.get("/shoes/{shoe_id}", response_model=Shoe_Pydantic)
async def get_shoe(shoe_id: int):
    shoe = await Shoe.get_or_none(id=shoe_id)
    if not shoe:
        raise HTTPException(status_code=404, detail="Shoe not found")
    return await Shoe_Pydantic.from_tortoise_orm(shoe)

# Endpoint to create a new shoe
@app.post("/shoes/", response_model=Shoe_Pydantic)
async def create_shoe(shoe: ShoeIn_Pydantic):
    obj = await Shoe.create(**shoe.dict(exclude_unset=True))
    return await Shoe_Pydantic.from_tortoise_orm(obj)

# Endpoint to update an existing shoe
@app.put("/shoes/{shoe_id}", response_model=Shoe_Pydantic)
async def update_shoe(shoe_id: int, shoe: ShoeIn_Pydantic):
    db_shoe = await Shoe.get_or_none(id=shoe_id)
    if not db_shoe:
        raise HTTPException(status_code=404, detail="Shoe not found")
    await db_shoe.update_from_dict(shoe.dict(exclude_unset=True))
    await db_shoe.save()
    return await Shoe_Pydantic.from_tortoise_orm(db_shoe)

# Endpoint to delete a shoe
@app.delete("/shoes/{shoe_id}")
async def delete_shoe(shoe_id: int):
    deleted = await Shoe.filter(id=shoe_id).delete()
    if not deleted:
        raise HTTPException(status_code=404, detail="Shoe not found")
    return {"message": "Shoe deleted successfully"}

# Tortoise ORM configuration
register_tortoise(
    app,
    db_url="postgres://user:password@localhost:5432/shoedb",
    modules={"models": ["models"]},
    generate_schemas=True,  # Automatically generate tables
    add_exception_handlers=True,
)

# Run the app with: uvicorn main:app --reload
