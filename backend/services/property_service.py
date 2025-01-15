import threading

from datetime import datetime
from collections import defaultdict
from fastapi.responses import JSONResponse
from sortedcontainers import SortedDict # type: ignore

from utils.utils import generate_unique_id

class Property:
    def __init__(self, property_id: str, user_id: str, details: dict):
        """
        Initialize property with:
        - Basic details (location, price, type)
        - Status (available/sold)
        - Timestamp
        """
        self.property_id = property_id
        self.user_id = user_id
        self.details = details
        self.status = "available"
        self.timestamp = datetime.now()

class PropertyManager:
    def __init__(self):
        """
        Initialize data structures for:
        - Property storage
        - User portfolios
        - Search indices
        """
        self.property_listings = {}
        self.user_property_listing = defaultdict(set)
        self.user_shortlist = defaultdict(set)
        self.price_index = SortedDict()
        self.location_index = defaultdict(list)
        self.status_index = defaultdict(list)
        
        self.lock = threading.Lock()

    def add_property(self, user_id: str, property_details: dict) -> str:
        """
        Add new property listing:
        - Validate details
        - Generate unique ID
        - Update indices
        Returns:
            property_id: str
        """
        # Check if Property details are provided.
        if not property_details:
            raise ValueError("Property details must be provided.")
        
        # Check if price and location are mentioned
        print(property_details)
        if not property_details.price or not property_details.location:
            raise ValueError("Property details must include 'price' and 'location' fields.")
        
        #Generate UniqueID for property, create Property Object and add to db
        property_id = generate_unique_id()
        new_property_data = Property(property_id, user_id, property_details)

        self.property_listings[property_id] = new_property_data
        self.user_property_listing[user_id].add(new_property_data.property_id)

        try:
            # Update indices
            self.price_index.setdefault(property_details.price, []).append(property_id)
            self.location_index[property_details.location].append(property_id)
            self.status_index["available"].append(property_id)
        except Exception as e:
            # Rollback in case any error occured
            del self.property_listings[property_id]
            self.user_property_listing[user_id].remove(property_id)
            raise RuntimeError(f"Failed to update indices: {str(e)}")
        return property_id

    def update_property_status(self, property_id: str, status: str, user_id: str) -> bool:
        """
        Update property status:
        - Verify ownership
        - Update status
        - Handle search index updates
        """
        # Check if Property Exists
        if not property_id in self.property_listings:
            raise KeyError(f"Property with ID '{property_id}' does not exist.")
        
        # Verify Ownership
        property_data = self.property_listings[property_id]
        if user_id != property_data.user_id:
            raise PermissionError("User does not have permission to update this property.")
        with self.lock:
            try:
                # Update the status and indices
                self.status_index[property_data.status].remove(property_id)
                property_data.status = status
                self.status_index[property_data.status].append(property_id)
            except KeyError as e:
                raise RuntimeError(f"Failed to update status index: {str(e)}")
            return JSONResponse(content="The status of property has been updated successfully")

    def get_user_properties(self, user_id: str, status:str) -> list[Property]:
        """
        Retrieve all properties for a user:
        - Filter by status
        - Sort by date
        """
        # Check if User Exists
        if user_id not in self.user_property_listing:
            raise KeyError(f"No properties found for user ID '{user_id}'.")
        try:
            # FInd user properties and filter based on status if status is provided and return sorted by time
            user_properties = [self.property_listings[prop_id] for prop_id in self.user_property_listing[user_id]]
            if status:
                user_properties = [prop for prop in user_properties if prop.status == status]

            return sorted(user_properties, key=lambda x: x.timestamp, reverse=True)
        except KeyError as e:
            raise RuntimeError(f"Failed to retrieve properties: {str(e)}")