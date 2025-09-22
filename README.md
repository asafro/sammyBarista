# Coffee Data Manager

A Python class for managing coffee data using MongoDB. This tool allows you to store, retrieve, update, and search coffee information including roasting level, grinding level, brewing ratio, and tasting notes.

## Features

- **Add Coffee**: Store new coffee entries with all required information
- **Retrieve Data**: Get all coffees, find by ID, or search by name
- **Search**: Filter coffees by roasting level and grinding level
- **Update**: Modify existing coffee entries
- **Delete**: Remove coffee entries from the database
- **Statistics**: Get overview of your coffee collection

## Requirements

- Python 3.6+
- MongoDB running locally (default: `mongodb://localhost:27017/`)
- pymongo library

## Installation

1. Install MongoDB on your system
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

```python
from coffee_manager import CoffeeDataManager

# Initialize the manager
manager = CoffeeDataManager()

# Add a coffee
coffee_id = manager.add_coffee(
    coffee_name="Ethiopian Yirgacheffe",
    roasting_level="Light",
    grinding_level="Medium-Fine",
    brewing_ratio="1:15",
    tasting_notes="Bright acidity with floral notes and citrus hints"
)

# Get all coffees
all_coffees = manager.get_all_coffees()

# Search for medium roast coffees
medium_coffees = manager.search_coffees(roasting_level="Medium")

# Update a coffee
manager.update_coffee(coffee_id, tasting_notes="Updated tasting notes")

# Get statistics
stats = manager.get_stats()

# Close connection
manager.close()
```

### Running the Example

```bash
python example_usage.py
```

## Coffee Data Structure

Each coffee entry contains:
- `coffee_name`: Name of the coffee
- `roasting_level`: Light, Medium, Dark, etc.
- `grinding_level`: Coarse, Medium, Fine, etc.
- `brewing_ratio`: Coffee to water ratio (e.g., "1:15")
- `tasting_notes`: Detailed tasting description
- `created_at`: Timestamp when added
- `updated_at`: Timestamp when last modified

## Methods

### Core Methods
- `add_coffee()`: Add a new coffee entry
- `get_all_coffees()`: Retrieve all coffee entries
- `get_coffee_by_id()`: Find coffee by ID
- `get_coffee_by_name()`: Find coffee by name
- `search_coffees()`: Search by roasting/grinding level
- `update_coffee()`: Update existing coffee
- `delete_coffee()`: Remove coffee from database
- `get_stats()`: Get collection statistics
- `close()`: Close MongoDB connection

## Database Configuration

By default, the class connects to:
- **Host**: localhost:27017
- **Database**: coffee_db
- **Collection**: coffees

You can customize these when initializing:

```python
manager = CoffeeDataManager(
    connection_string="mongodb://localhost:27017/",
    database_name="my_coffee_db",
    collection_name="my_coffees"
)
```

## Error Handling

The class includes proper error handling for:
- MongoDB connection issues
- Invalid ObjectIds
- Missing required fields
- Database operation failures
