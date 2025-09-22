"""
Coffee Data Manager - A simple MongoDB-based class for storing and managing coffee data.
"""

from datetime import datetime
from typing import List, Dict, Optional, Any
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson import ObjectId


class CoffeeDataManager:
    """A class to manage coffee data using MongoDB."""
    
    def __init__(self, connection_string: str = "mongodb://localhost:27017/", 
                 database_name: str = "coffee_db", collection_name: str = "coffees"):
        """
        Initialize the CoffeeDataManager.
        
        Args:
            connection_string: MongoDB connection string
            database_name: Name of the database
            collection_name: Name of the collection
        """
        try:
            self.client = MongoClient(connection_string)
            self.client.admin.command('ping')  # Test connection
            self.db = self.client[database_name]
            self.collection = self.db[collection_name]
            print(f"Connected to MongoDB: {database_name}.{collection_name}")
        except ConnectionFailure:
            raise ConnectionError("Could not connect to MongoDB. Make sure MongoDB is running.")
    
    def add_coffee(self, coffee_name: str, roasting_level: str, grinding_level: str, 
                   brewing_ratio: str, tasting_notes: str) -> str:
        """
        Add a new coffee entry.
        
        Args:
            coffee_name: Name of the coffee
            roasting_level: Roasting level (Light, Medium, Dark, etc.)
            grinding_level: Grinding level (Coarse, Medium, Fine, etc.)
            brewing_ratio: Coffee to water ratio (e.g., "1:15")
            tasting_notes: Tasting notes and description
            
        Returns:
            str: The inserted document's ID
        """
        coffee_data = {
            "coffee_name": coffee_name,
            "roasting_level": roasting_level,
            "grinding_level": grinding_level,
            "brewing_ratio": brewing_ratio,
            "tasting_notes": tasting_notes,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        result = self.collection.insert_one(coffee_data)
        print(f"Added coffee: {coffee_name}")
        return str(result.inserted_id)
    
    def get_all_coffees(self) -> List[Dict[str, Any]]:
        """
        Get all coffee entries.
        
        Returns:
            List of coffee dictionaries
        """
        coffees = list(self.collection.find())
        for coffee in coffees:
            coffee["_id"] = str(coffee["_id"])
        return coffees
    
    def get_coffee_by_id(self, coffee_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a coffee by its ID.
        
        Args:
            coffee_id: The coffee's ID
            
        Returns:
            Coffee dictionary or None if not found
        """
        coffee = self.collection.find_one({"_id": ObjectId(coffee_id)})
        if coffee:
            coffee["_id"] = str(coffee["_id"])
        return coffee
    
    def get_coffee_by_name(self, coffee_name: str) -> Optional[Dict[str, Any]]:
        """
        Get a coffee by its name.
        
        Args:
            coffee_name: Name of the coffee
            
        Returns:
            Coffee dictionary or None if not found
        """
        coffee = self.collection.find_one({"coffee_name": coffee_name})
        if coffee:
            coffee["_id"] = str(coffee["_id"])
        return coffee
    
    def get_coffee_with_query(self, query_dict: Dict[str, Any], 
                            case_sensitive: bool = False) -> List[Dict[str, Any]]:
        """
        Get coffees using a flexible query dictionary with multiple key-value filters.
        
        Args:
            query_dict: Dictionary with field names as keys and target values as values
                       Example: {"roasting_level": "Medium", "grinding_level": "Fine"}
            case_sensitive: If False, uses case-insensitive regex matching
            
        Returns:
            List of matching coffee dictionaries
            
        Examples:
            # Find medium roast coffees
            manager.get_coffee_with_query({"roasting_level": "Medium"})
            
            # Find Ethiopian coffees with fine grinding
            manager.get_coffee_with_query({
                "coffee_name": "Ethiopian", 
                "grinding_level": "Fine"
            })
            
            # Find coffees with specific brewing ratio
            manager.get_coffee_with_query({"brewing_ratio": "1:15"})
            
            # Find coffees with high bitterness in tasting notes
            manager.get_coffee_with_query({"tasting_notes": "Bitterness: High"})
        """
        query = {}
        
        for key, value in query_dict.items():
            if value is not None:
                if case_sensitive:
                    # Exact match
                    query[key] = value
                else:
                    # Case-insensitive regex match
                    query[key] = {"$regex": str(value), "$options": "i"}
        
        coffees = list(self.collection.find(query))
        for coffee in coffees:
            coffee["_id"] = str(coffee["_id"])
        return coffees
    
    def search_coffees(self, roasting_level: Optional[str] = None, 
                      grinding_level: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search for coffees by roasting level and/or grinding level.
        
        Args:
            roasting_level: Filter by roasting level
            grinding_level: Filter by grinding level
            
        Returns:
            List of matching coffee dictionaries
        """
        query = {}
        if roasting_level:
            query["roasting_level"] = {"$regex": roasting_level, "$options": "i"}
        if grinding_level:
            query["grinding_level"] = {"$regex": grinding_level, "$options": "i"}
        
        coffees = list(self.collection.find(query))
        for coffee in coffees:
            coffee["_id"] = str(coffee["_id"])
        return coffees
    
    def update_coffee(self, coffee_id: str, **updates) -> bool:
        """
        Update a coffee entry.
        
        Args:
            coffee_id: The coffee's ID
            **updates: Fields to update
            
        Returns:
            True if updated successfully, False otherwise
        """
        updates["updated_at"] = datetime.now()
        result = self.collection.update_one(
            {"_id": ObjectId(coffee_id)},
            {"$set": updates}
        )
        return result.modified_count > 0
    
    def delete_coffee(self, coffee_id: str) -> bool:
        """
        Delete a coffee entry.
        
        Args:
            coffee_id: The coffee's ID
            
        Returns:
            True if deleted successfully, False otherwise
        """
        result = self.collection.delete_one({"_id": ObjectId(coffee_id)})
        return result.deleted_count > 0
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get basic statistics about the coffee collection.
        
        Returns:
            Dictionary with collection statistics
        """
        total = self.collection.count_documents({})
        roasting_levels = self.collection.distinct("roasting_level")
        grinding_levels = self.collection.distinct("grinding_level")
        
        return {
            "total_coffees": total,
            "roasting_levels": roasting_levels,
            "grinding_levels": grinding_levels
        }
    
    def close(self):
        """Close the MongoDB connection."""
        self.client.close()
        print("Connection closed")


# Example usage
if __name__ == "__main__":
    # Initialize the coffee manager
    manager = CoffeeDataManager()
    
    try:
        # Add some sample coffees
        manager.add_coffee(
            "Ethiopian Yirgacheffe",
            "Light",
            "Medium-Fine",
            "1:15",
            "Bright acidity with floral notes and citrus hints"
        )
        
        manager.add_coffee(
            "Colombian Supremo",
            "Medium",
            "Medium",
            "1:16",
            "Balanced body with chocolate and nutty undertones"
        )
        
        manager.add_coffee(
            "Sumatra Mandheling",
            "Dark",
            "Coarse",
            "1:14",
            "Full body with earthy, herbal notes"
        )
        
        # Display all coffees
        print("\nAll coffees:")
        for coffee in manager.get_all_coffees():
            print(f"- {coffee['coffee_name']} ({coffee['roasting_level']} roast)")
        
        # Search for medium roast coffees (old method)
        print("\nMedium roast coffees (old method):")
        medium_coffees = manager.search_coffees(roasting_level="Medium")
        for coffee in medium_coffees:
            print(f"- {coffee['coffee_name']}: {coffee['tasting_notes']}")
        
        # Search using the new get_coffee_with_query method
        print("\nMedium roast coffees (new method):")
        medium_coffees_new = manager.get_coffee_with_query({"roasting_level": "Medium"})
        for coffee in medium_coffees_new:
            print(f"- {coffee['coffee_name']}: {coffee['tasting_notes']}")
        
        # Example: Find Ethiopian coffees with fine grinding
        print("\nEthiopian coffees with fine grinding:")
        ethiopian_fine = manager.get_coffee_with_query({
            "coffee_name": "Ethiopian", 
            "grinding_level": "Fine"
        })
        for coffee in ethiopian_fine:
            print(f"- {coffee['coffee_name']}: {coffee['grinding_level']}")
        
        # Example: Find coffees with specific brewing ratio
        print("\nCoffees with 1:15 brewing ratio:")
        ratio_coffees = manager.get_coffee_with_query({"brewing_ratio": "1:15"})
        for coffee in ratio_coffees:
            print(f"- {coffee['coffee_name']}: {coffee['brewing_ratio']}")
        
        # Show statistics
        print("\nDatabase statistics:")
        stats = manager.get_stats()
        for key, value in stats.items():
            print(f"- {key}: {value}")
    
    finally:
        manager.close()