from fastapi import APIRouter, HTTPException, status
from app.database import db
from app.models import Item
from bson import ObjectId
from datetime import datetime, date
from bson.errors import InvalidId
router = APIRouter()

@router.post("/items/")
async def create_item(item: Item):
    """Create a new item.
    
    # Request: JSON body with item details (name, email, item_name quantity, expiry_date)
    # Response: JSON with inserted item ID
    """
    try:
        item_dict = item.dict()
        item_dict["expiry_date"] = item_dict["expiry_date"].isoformat()
        item_dict["insert_date"] = datetime.now().strftime("%Y-%m-%d")
        result = await db["items"].insert_one(item_dict)
        return {"id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/items/{id}")
async def read_item(id: str):
    """Get an item by its ID.
    
    # Request: Item ID as path parameter
    # Response: JSON with item details or 404 error if not found
    """
    try:
        # Attempt to convert the id to ObjectId
        object_id = ObjectId(id)
    except InvalidId:
        # Raise a 400 Bad Request error if the ID is invalid
        raise HTTPException(status_code=400, detail="Invalid ID format")
    result = await db["items"].find_one({"_id": object_id})
    if result:
        result["_id"] = str(result["_id"])
        return result
    raise HTTPException(status_code=404, detail="Item not found")

@router.get("/items/filter/")
async def filter_items(email: str = None, expiry_date: str = None, insert_date: str = None, quantity: int = None):
    """Filter items by optional criteria (email, expiry_date, insert_date, quantity).
    
    # Request: Optional query parameters (email, expiry_date, insert_date, quantity)
    # Response: JSON array of filtered items
    """
    filter = {}
    if email:
        filter["email"] = email
    if expiry_date:
        filter["expiry_date"] = {"$gt": expiry_date}
    if insert_date:
        filter["insert_date"] = {"$gt": insert_date}
    if quantity:
        filter["quantity"] = {"$gte": quantity}

    results = await db["items"].find(filter).to_list(length=100)
    return [{**item, "_id": str(item["_id"])} for item in results]

@router.delete("/items/{id}")
async def delete_item(id: str):
    """Delete an item by its ID.
    
    # Request: Item ID as path parameter
    # Response: JSON with success message or 404 error if not found
    """
    try:
        # Attempt to convert the id to ObjectId
        object_id = ObjectId(id)
    except InvalidId:
        # Raise a 400 Bad Request error if the ID is invalid
        raise HTTPException(status_code=400, detail="Invalid ID format")
    result = await db["items"].delete_one({"_id": object_id})
    if result.deleted_count == 1:
        return {"message": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")

@router.put("/items/{id}")
async def update_item(id: str, item: Item):
    """Update an item by its ID.
    
    # Request: Item ID as path parameter, JSON body with updated item details
    # Response: JSON with success message or 404 error if not found
    """
    try:
        # Attempt to convert the id to ObjectId
        object_id = ObjectId(id)
    except InvalidId:
        # Raise a 400 Bad Request error if the ID is invalid
        raise HTTPException(status_code=400, detail="Invalid ID format")
    item_dict = item.dict()
    if isinstance(item_dict["expiry_date"], date):
        item_dict["expiry_date"] = item_dict["expiry_date"].isoformat()

    result = await db["items"].update_one({"_id": object_id}, {"$set": item_dict})
    if result.modified_count == 1:
        return {"message": "Item updated"}
    raise HTTPException(status_code=404, detail="Item not found")


@router.get("/items/count-by-email/")
async def count_items_by_email():
    """Aggregate items to count the number of items for each email.
    
    # Response: 
    - JSON list of email counts in the format: [{"count": 10,"email": "example@example.com",}...]
    """
    pipeline = [
        {
            "$group": {
                "_id": "$email",  # Group by email field
                "count": {"$sum": 1}  # Count the number of items
            }
        },
        {
            "$project": {
                "email": "$_id",  # Rename the _id field to email
                "count": 1,  # Include the count field
                "_id": 0  # Exclude the original _id field
            }
        }
    ]
    
    results = await db["items"].aggregate(pipeline).to_list(length=None)  # Fetch all results

    return results
