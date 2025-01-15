from datetime import datetime

from models.property_models import Property
from .property_service import PropertyManager


class PropertySearch:
    def __init__(self, property_manager: PropertyManager):
        """
        Initialize search system:
        - Price indices
        - Location indices
        - Status tracking
        """
        self.property_manager = property_manager

    def search_properties(self, criteria: dict) -> list[Property]:
        """
        Search properties based on:
        - Price range
        - Location
        - Property type
        - Status (available only)
        
        Handle:
        - Multiple filters
        - Sorting
        - Pagination
        """
        results = []
        min_price = criteria.get('min_price', 0)
        max_price = criteria.get('max_price', float('inf'))

        try:
            for prop_id, prop_data in self.property_manager.property_listings.items():
                # Check for status 'available'
                if prop_data.status != 'available':
                    continue
                # Check for price range
                if min_price:
                    if not (min_price <= prop_data.details.price):
                        continue
                if max_price:
                    if not (prop_data.details.price <= max_price):
                        continue
                # Check for location if provided
                if criteria.get('location') and prop_data.details.location != criteria.get('location'):
                    continue
                # Check for property type if provided
                if criteria.get('property_type') and prop_data.details.property_type != criteria.get('property_type'):
                    continue
                # If all conditions are met, add to results
                results.append({prop_id: prop_data})
            return results
        except KeyError as e:
            raise KeyError(f"Property data is missing required field: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"An error occurred while searching properties: {str(e)}")

    def shortlist_property(self, user_id: str, property_id: str) -> bool:
        """
        Add property to user's shortlist:
        - Verify property exists
        - Check if already shortlisted
        - Update user's shortlist
        """
        try:
            # Check if Property ID exists 
            if property_id not in self.property_manager.property_listings:
                raise ValueError(f"Property with ID '{property_id}' does not exist.")
            
            # Fetch property status
            property_data = self.property_manager.property_listings[property_id]
            property_status = property_data.status

            # Check if Property already shortlisted
            if property_status == 'sold':
                raise ValueError(f"Property with ID '{property_id}' is already sold.")
            
            # Add property to user's shortlist with the current timestamp
            current_datetime = datetime.now()
            self.property_manager.user_shortlist[user_id].add((property_id, current_datetime))
            
            # Update the property status to sold
            response = self.property_manager.update_property_status(property_id,'sold',user_id)
            return response
        except KeyError as e:
            raise KeyError(f"User ID '{user_id}' does not exist in the system: {str(e)}")
        except ValueError as e:
            raise ValueError(f"Error with property '{property_id}': {str(e)}")
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred while shortlisting property '{property_id}': {str(e)}")


    def get_shortlisted(self, user_id: str) -> list[Property]:
        """
        Get user's shortlisted properties:
        - Filter out sold properties
        - Sort by shortlist date
        """
        try:
            # Check if user exists
            if user_id not in self.property_manager.user_shortlist:
                raise ValueError(f"No shortlisted properties found for user ID '{user_id}'.")

            # Retrieve and sort shortlisted properties by timestamp
            shortlisted_properties = [
                self.property_manager.property_listings[prop_id]
                for prop_id,_ in self.property_manager.user_shortlist[user_id]
            ]
            return sorted(shortlisted_properties, key=lambda x: x.timestamp, reverse=True)
        except ValueError as e:
            raise ValueError(f"Error with user '{user_id}': {str(e)}")
        except KeyError as e:
            raise KeyError(f"Error with user or property data: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred while retrieving the shortlisted properties for user '{user_id}': {str(e)}")