from fastapi import FastAPI, HTTPException, Depends
from models.property_models import PropertyCreate
from utils.utils import get_current_user
from services.property_service import PropertyManager
from services.search_service import PropertySearch

app = FastAPI()

property_manager = PropertyManager()
property_search = PropertySearch(property_manager)

@app.post("/api/v1/properties")
async def create_property(
    property_data: PropertyCreate,
    current_user: str = Depends(get_current_user)
):
    """
    Create new property listing:
    1. Validate input
    2. Create property
    3. Update indices
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    property_id = property_manager.add_property(current_user,property_data)
    return {"message": "Property created successfully", "property_id": property_id}

@app.get("/api/v1/properties")
async def get_property(
    status: str,
    current_user: str = Depends(get_current_user)
):
    """
    Create new property listing:
    1. Validate input
    2. Create property
    3. Update indices
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    response = property_manager.get_user_properties(current_user, status)
    if not response:
        raise HTTPException(status_code=400, detail="Unable to get properties.")
    return {"properties": response}


@app.get("/api/v1/properties/search")
async def search_properties(
    min_price: float = None,
    max_price: float = None,
    location: str = None,
    property_type: str = None,
    page: int = 1,
    limit: int = 10
):
    """
    Search properties with:
    - Price range filter
    - Location filter
    - Type filter
    - Pagination
    """
    criteria = {
        "min_price": min_price,
        "max_price": max_price,
        "location": location,
        "property_type": property_type,
        "page": page,
        "limit": limit,
    }
    results = property_search.search_properties(criteria)
    return {"results": results, "page": page, "limit": limit}


@app.put("/api/v1/properties/shortlist")
async def shortlist_property(
    property_id: str,
    current_user: str = Depends(get_current_user)
):
    """
    Create new property listing:
    1. Validate input
    2. Update Property
    3. Update indices
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    response = property_search.shortlist_property(current_user, property_id)
    if not response:
        raise HTTPException(status_code=400, detail="Unable to shortlist property.")
    return {"message": "Property shortlisted successfully", "property_id": property_id}


@app.get("/api/v1/properties/shortlist")
async def get_shortlisted_properties(
    current_user: str = Depends(get_current_user)
):
    """
    Create new property listing:
    1. Validate input
    2. Update Property
    3. Update indices
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    shortlisted_properties = property_search.get_shortlisted(current_user)
    if not shortlisted_properties:
        raise HTTPException(status_code=404, detail="No shortlisted properties found.")
    return shortlisted_properties