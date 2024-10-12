from pydantic import BaseModel,EmailStr,Field
from datetime import datetime, date

class Item(BaseModel):
    name: str
    email: EmailStr
    item_name: str
    quantity: int
    expiry_date: date
    
class ClockInRecord(BaseModel):
    email: EmailStr
    location: str