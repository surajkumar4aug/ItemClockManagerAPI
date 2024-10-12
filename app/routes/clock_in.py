from fastapi import APIRouter, HTTPException
from app.database import db
from app.models import ClockInRecord
from bson import ObjectId
from datetime import datetime
from  bson.errors import InvalidId
router = APIRouter()

@router.post("/clock-in/")
async def create_clock_in_record(clock_in_record: ClockInRecord):
    """Create a new clock-in record.
    
    # Request: JSON body with clock-in record details (email, location, etc.)
    # Response: JSON with inserted record ID
    """
    clock_in_records = clock_in_record.dict()
    clock_in_records["insert_date"] = datetime.now().strftime("%Y-%m-%d")
    result = await db["clock_in_records"].insert_one(clock_in_records)
    return {"id": str(result.inserted_id)}

@router.get("/clock-in/{id}")
async def read_clock_in_record(id: str):
    """Get a clock-in record by its ID.
    
    # Request: Clock-in record ID as path parameter
    # Response: JSON with clock-in record details or 404 error if not found
    """
    try:
        # Attempt to convert the id to ObjectId
        object_id = ObjectId(id)
    except InvalidId:
        # Raise a 400 Bad Request error if the ID is invalid
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    result = await db["clock_in_records"].find_one({"_id": object_id})
    if result:
        result["_id"] = str(result["_id"])
        return result
    raise HTTPException(status_code=404, detail="Clock-in record not found")

@router.get("/clock-in/filter/")
async def filter_clock_in_records(email: str = None, location: str = None, insert_date: str = None):
    """Filter clock-in records by optional criteria (email, location, insert_date).
    
    # Request: Optional query parameters (email, location, insert_date)
    # Response: JSON array of filtered clock-in records
    """
    filter = {}
    if email:
        filter["email"] = email
    if location:
        filter["location"] = location
    if insert_date:
        filter["insert_date"] = {"$gt": insert_date}

    results = await db["clock_in_records"].find(filter).to_list(length=100)
    results = [{**item, "_id": str(item["_id"])} for item in results]
    return results

@router.delete("/clock-in/{id}")
async def delete_clock_in_record(id: str):
    """Delete a clock-in record by its ID.
    
    # Request: Clock-in record ID as path parameter
    # Response: JSON with success message or 404 error if not found
    """
    try:
        # Attempt to convert the id to ObjectId
        object_id = ObjectId(id)
    except InvalidId:
        # Raise a 400 Bad Request error if the ID is invalid
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    result = await db["clock_in_records"].delete_one({"_id": object_id})
    if result.deleted_count == 1:
        return {"message": "Clock-in record deleted"}
    raise HTTPException(status_code=404, detail="Clock-in record not found")

@router.put("/clock-in/{id}")
async def update_clock_in_record(id: str, clock_in_record: ClockInRecord):
    """Update a clock-in record by its ID.
    
    # Request: Clock-in record ID as path parameter, JSON body with updated record details
    # Response: JSON with success message or 404 error if not found
    """
    try:
        # Attempt to convert the id to ObjectId
        object_id = ObjectId(id)
    except InvalidId:
        # Raise a 400 Bad Request error if the ID is invalid
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    clock_in_records = clock_in_record.dict()
    clock_in_records["insert_date"] = datetime.now().strftime("%Y-%m-%d")
    
    result = await db["clock_in_records"].update_one({"_id": object_id}, {"$set": clock_in_records})
    if result.modified_count == 1:
        return {"message": "Clock-in record updated"}
    raise HTTPException(status_code=404, detail="Clock-in record not found")
