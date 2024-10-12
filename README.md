
# FastAPI ItemClockManagerAPI

This project is built using **FastAPI** and provides CRUD operations for managing items and clock-in records in a MongoDB database. It includes routes for creating, reading, updating, and deleting items and clock-in records, along with filtering capabilities.

## Setup Instructions

### Prerequisites

- Python 3.8+
- MongoDB
- FastAPI
- Uvicorn (ASGI server)
- Pydantic (for data validation)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the environment variables:**
   Create a `.env` file in the root of the project and add the following variables:
   ```env

   Database configuration
   MONGODB_URI=
   MONGODB_DATABASE=

   ```
4. Start the FastAPI server using Uvicorn:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Access the API docs at `http://127.0.0.1:8000/docs` or the alternative documentation at `/redoc`.

### Configuration

Ensure your MongoDB is running and accessible. Update the MongoDB connection settings in `app/database.py` if necessary.

### Project Structure

```
app/
│__ __init__.py  
├── database.py         # Database connection setup
├── models.py           # Pydantic models for validation
├── main.py             # FastAPI app instance
└── routes/
|   |__ __init__.py             
|   ├── item_routes.py  # CRUD operations for Items
|   └── clock_in_routes.py # CRUD operations for Clock-in Records
|__ .env
└── requirements.txt     
```

## Endpoints Overview

### Item Management
1. **Create Item**  
   **POST** `/items/`  
   Request Body: `{ "name": "Item1", "email": "example@mail.com", "item_name": "ItemName", "quantity": 5, "expiry_date": "2024-10-15" }`  
   Response: `{ "id": "<item-id>" }`

2. **Get Item by ID**  
   **GET** `/items/{id}`  
   Response: `{ "_id": "<id>", "name": "Item1", ... }`

3. **Filter Items**  
   **GET** `/items/filter/`  
   Query Parameters: `email, expiry_date, insert_date, quantity`  
   Response: `[{ "_id": "<id>", "name": "Item1", ... }, ...]`

4. **Update Item**  
   **PUT** `/items/{id}`  
   Request Body: Updated item details.  
   Response: `{ "message": "Item updated" }`

5. **Delete Item**  
   **DELETE** `/items/{id}`  
   Response: `{ "message": "Item deleted" }`

6. **Count Items by Email**  
   **GET** `/items/count-by-email/`  
   Response: `[{ "email": "example@mail.com", "count": 10 }, ...]`

### Clock-in Record Management
1. **Create Clock-in Record**  
   **POST** `/clock-in/`  
   Request Body: `{ "email": "example@mail.com", "location": "Office" }`  
   Response: `{ "id": "<record-id>" }`

2. **Get Clock-in Record by ID**  
   **GET** `/clock-in/{id}`  
   Response: `{ "_id": "<id>", "email": "example@mail.com", ... }`

3. **Filter Clock-in Records**  
   **GET** `/clock-in/filter/`  
   Query Parameters: `email, location, insert_date`  
   Response: `[{ "_id": "<id>", "email": "example@mail.com", ... }, ...]`

4. **Update Clock-in Record**  
   **PUT** `/clock-in/{id}`  
   Request Body: Updated record details.  
   Response: `{ "message": "Clock-in record updated" }`

5. **Delete Clock-in Record**  
   **DELETE** `/clock-in/{id}`  
   Response: `{ "message": "Clock-in record deleted" }`



