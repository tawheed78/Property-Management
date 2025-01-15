# Property Management API
This project provides a FastAPI-based API for managing property listings, including functionality for property creation, search, shortlisting, and more. It allows users to manage properties, filter them by various criteria (price, location, etc.).

## Features
- Create Property Listings: Users can create new property listings by providing details like price, location, type, and amenities.
- Search Properties: Allows users to search for properties based on price range, location, property type, and status (available).
- Shortlist Properties: Users can shortlist properties.
- View Shortlisted Properties: Users can view their shortlisted properties, which are sorted by the time they were added.

## Technologies Used
- FastAPI: Web framework for building APIs.
- Pydantic: Data validation and settings management.
- Python Threading: For thread-safe operations on property data.
- SortedDict: For efficient sorted data storage and searching.

## Setup and Installation
1. Clone the Repository
```bash
git clone https://github.com/yourusername/property-management-api.git
cd backend
```

2. Create a virtual environment and activate it
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install Dependencies
Ensure you have Python 3.7+ installed. Then, install the necessary Python dependencies:
```bash
pip install -r requirements.txt
```

4. Run the Application
Start the FastAPI server:
```bash
uvicorn main:app --reload
```

The API docs will be available at http://127.0.0.1:8000/docs for testing.

## API Endpoints
1. Create Property
POST /api/v1/properties
Request Body:
```bash
{
  "location": "Panvel",
  "price": 8000000,
  "property_type": "Flat",
  "description": "A beautiful 2-bedroom apartment",
  "amenities": ["Gym", "Pool"]
}

Response:
{
  "message": "Property created successfully",
  "property_id": "17369669778705324"
}
```

2. Get User Properties
GET /api/v1/properties?status=available
```bash
Response:
{
  "properties": [
    {
      "property_id": "17369669778705324",
      "user_id": "DELL",
      "details": {
        "location": "Panvel",
        "price": 8000000,
        "property_type": "Flat",
        "description": "A beautiful 2-bedroom apartment",
        "amenities": [
          "Gym",
          "Pool"
        ]
      },
      "status": "available",
      "timestamp": "2025-01-16T00:19:37.870262"
    }
  ]
}
```

3. Search Properties
GET /api/v1/properties/search?min_price=6000000&max_price=9000000&location=Panvel&property_type=Flat&page=1&limit=10
```bash
Response:

{
  "results": [
    {
      "17369669778705324": {
        "property_id": "17369669778705324",
        "user_id": "DELL",
        "details": {
          "location": "Panvel",
          "price": 8000000,
          "property_type": "Flat",
          "description": "A beautiful 2-bedroom apartment",
          "amenities": [
            "Gym",
            "Pool"
          ]
        },
        "status": "available",
        "timestamp": "2025-01-16T00:19:37.870262"
      }
    }
  ],
  "page": 1,
  "limit": 10
}
```

4. Shortlist Property
PUT /api/v1/properties/shortlist?property_id={property_id}'
```bash
Request Body:
{
  "property_id": "17369669778705324"
}

Response:
{
  "message": "Property shortlisted successfully",
  "property_id": "17369669778705324"
}
```

5. Get Shortlisted Properties
GET /api/v1/properties/shortlist
```bash
Response:

[
  {
    "property_id": "17369669778705324",
    "user_id": "DELL",
    "details": {
      "location": "Panvel",
      "price": 8000000,
      "property_type": "Flat",
      "description": "A beautiful 2-bedroom apartment",
      "amenities": [
        "Gym",
        "Pool"
      ]
    },
    "status": "sold",
    "timestamp": "2025-01-16T00:19:37.870262"
  }
]
```