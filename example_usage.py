"""
Example usage of the CoffeeDataManager class with 400 coffee examples.
"""

from coffee_manager import CoffeeDataManager
import random


def generate_coffee_examples(manager):
    """Generate 400 coffee examples using 10 different coffee types."""
    
    # Define 10 coffee types with their characteristics
    coffee_types = [
        {
            "name": "Ethiopian Yirgacheffe",
            "roasting_levels": ["Light", "Medium-Light"],
            "grinding_levels": ["Medium-Fine", "Fine"],
            "brewing_ratios": ["1:15", "1:16", "1:17"],
            "base_notes": "Bright acidity with floral notes, hints of citrus and jasmine",
            "bitterness_level": "Low",
            "sourness_level": "High"
        },
        {
            "name": "Colombian Supremo",
            "roasting_levels": ["Medium", "Medium-Dark"],
            "grinding_levels": ["Medium", "Medium-Fine"],
            "brewing_ratios": ["1:15", "1:16", "1:17"],
            "base_notes": "Balanced body with chocolate and nutty undertones",
            "bitterness_level": "Medium",
            "sourness_level": "Medium"
        },
        {
            "name": "Sumatra Mandheling",
            "roasting_levels": ["Dark", "Medium-Dark"],
            "grinding_levels": ["Coarse", "Medium"],
            "brewing_ratios": ["1:14", "1:15", "1:16"],
            "base_notes": "Full body with earthy, herbal notes and low acidity",
            "bitterness_level": "High",
            "sourness_level": "Low"
        },
        {
            "name": "Guatemala Antigua",
            "roasting_levels": ["Medium", "Medium-Light"],
            "grinding_levels": ["Medium", "Medium-Fine"],
            "brewing_ratios": ["1:15", "1:16", "1:17"],
            "base_notes": "Smooth with notes of caramel and spice",
            "bitterness_level": "Medium-Low",
            "sourness_level": "Medium"
        },
        {
            "name": "Kenya AA",
            "roasting_levels": ["Light", "Medium-Light"],
            "grinding_levels": ["Medium-Fine", "Fine"],
            "brewing_ratios": ["1:15", "1:16", "1:17"],
            "base_notes": "Wine-like acidity with berry and citrus notes",
            "bitterness_level": "Low",
            "sourness_level": "High"
        },
        {
            "name": "Brazilian Santos",
            "roasting_levels": ["Medium", "Medium-Dark"],
            "grinding_levels": ["Medium", "Medium-Fine"],
            "brewing_ratios": ["1:16", "1:17", "1:18"],
            "base_notes": "Mild and smooth with nutty and chocolate flavors",
            "bitterness_level": "Medium",
            "sourness_level": "Low"
        },
        {
            "name": "Jamaican Blue Mountain",
            "roasting_levels": ["Medium", "Medium-Light"],
            "grinding_levels": ["Medium", "Medium-Fine"],
            "brewing_ratios": ["1:16", "1:17", "1:18"],
            "base_notes": "Mild, smooth, and well-balanced with no bitterness",
            "bitterness_level": "Very Low",
            "sourness_level": "Low"
        },
        {
            "name": "Costa Rica Tarrazu",
            "roasting_levels": ["Medium", "Medium-Light"],
            "grinding_levels": ["Medium", "Medium-Fine"],
            "brewing_ratios": ["1:15", "1:16", "1:17"],
            "base_notes": "Bright acidity with citrus and honey notes",
            "bitterness_level": "Low",
            "sourness_level": "Medium-High"
        },
        {
            "name": "Italian Espresso Blend",
            "roasting_levels": ["Dark", "Very Dark"],
            "grinding_levels": ["Fine", "Extra-Fine"],
            "brewing_ratios": ["1:2", "1:3", "1:4"],
            "base_notes": "Strong, bold flavor with rich crema and intense body",
            "bitterness_level": "High",
            "sourness_level": "Low"
        },
        {
            "name": "Hawaiian Kona",
            "roasting_levels": ["Medium", "Medium-Light"],
            "grinding_levels": ["Medium", "Medium-Fine"],
            "brewing_ratios": ["1:16", "1:17", "1:18"],
            "base_notes": "Smooth, mild flavor with hints of nuts and spices",
            "bitterness_level": "Low",
            "sourness_level": "Low"
        }
    ]
    
    # Additional flavor descriptors for variety
    flavor_enhancers = [
        "with a hint of vanilla", "with subtle cinnamon notes", "with a touch of honey",
        "with mild cocoa undertones", "with gentle floral aromas", "with bright lemon zest",
        "with warm caramel finish", "with delicate berry hints", "with smooth chocolate notes",
        "with crisp apple acidity", "with rich toffee flavors", "with fresh herbal tones",
        "with sweet orange peel", "with dark cherry notes", "with creamy milk chocolate",
        "with tangy grapefruit", "with roasted almond finish", "with spicy clove hints",
        "with tropical fruit notes", "with earthy mushroom undertones", "with smoky cedar finish",
        "with bright lime acidity", "with velvety dark chocolate", "with crisp pear notes",
        "with warm brown sugar", "with fresh mint hints", "with rich molasses finish",
        "with tangy passion fruit", "with smooth butterscotch", "with bright mandarin orange",
        "with deep wine-like body", "with creamy vanilla bean", "with fresh garden herbs",
        "with sweet maple syrup", "with bright strawberry notes", "with rich dark cherry",
        "with smooth hazelnut cream", "with crisp green apple", "with warm ginger spice",
        "with tropical mango hints", "with earthy forest floor", "with bright bergamot",
        "with creamy coconut milk", "with fresh peach notes", "with rich dark chocolate cake"
    ]
    
    print("=== Adding 400 Coffee Examples ===")
    
    for i in range(400):
        # Select random coffee type
        coffee_type = random.choice(coffee_types)
        
        # Generate variant name
        variant_num = (i // 40) + 1
        coffee_name = f"{coffee_type['name']} - Batch {variant_num:03d}"
        
        # Select random attributes
        roasting_level = random.choice(coffee_type['roasting_levels'])
        grinding_level = random.choice(coffee_type['grinding_levels'])
        brewing_ratio = random.choice(coffee_type['brewing_ratios'])
        
        # Create tasting notes with bitterness and sourness
        flavor_enhancer = random.choice(flavor_enhancers)
        tasting_notes = f"{coffee_type['base_notes']}, {flavor_enhancer}. "
        tasting_notes += f"Bitterness: {coffee_type['bitterness_level']}. "
        tasting_notes += f"Sourness: {coffee_type['sourness_level']}."
        
        # Add the coffee
        try:
            manager.add_coffee(
                coffee_name=coffee_name,
                roasting_level=roasting_level,
                grinding_level=grinding_level,
                brewing_ratio=brewing_ratio,
                tasting_notes=tasting_notes
            )
            
            if (i + 1) % 50 == 0:
                print(f"Added {i + 1} coffees...")
                
        except Exception as e:
            print(f"Error adding coffee {i + 1}: {e}")
    
    print(f"Successfully added 400 coffee examples!")


def main():
    """Demonstrate the CoffeeDataManager functionality."""
    
    # Initialize the coffee manager
    print("Initializing Coffee Data Manager...")
    manager = CoffeeDataManager()
    
    try:
        # Generate 400 coffee examples
        generate_coffee_examples(manager)
        
        # Display sample of coffees (first 10)
        print("\n=== Sample of Coffees in Database (First 10) ===")
        all_coffees = manager.get_all_coffees()
        for i, coffee in enumerate(all_coffees[:10], 1):
            print(f"{i}. {coffee['coffee_name']}")
            print(f"   Roasting Level: {coffee['roasting_level']}")
            print(f"   Grinding Level: {coffee['grinding_level']}")
            print(f"   Brewing Ratio: {coffee['brewing_ratio']}")
            print(f"   Tasting Notes: {coffee['tasting_notes']}")
            print()
        
        # Search for medium roast coffees
        print("=== Medium Roast Coffees (Sample) ===")
        medium_coffees = manager.search_coffees(roasting_level="Medium")
        for coffee in medium_coffees[:5]:  # Show first 5
            print(f"- {coffee['coffee_name']}: {coffee['tasting_notes'][:100]}...")
        
        # Search for high bitterness coffees
        print("\n=== High Bitterness Coffees (Sample) ===")
        high_bitter_coffees = [coffee for coffee in all_coffees if "Bitterness: High" in coffee['tasting_notes']]
        for coffee in high_bitter_coffees[:5]:  # Show first 5
            print(f"- {coffee['coffee_name']}: {coffee['tasting_notes'][:100]}...")
        
        # Search for high sourness coffees
        print("\n=== High Sourness Coffees (Sample) ===")
        high_sour_coffees = [coffee for coffee in all_coffees if "Sourness: High" in coffee['tasting_notes']]
        for coffee in high_sour_coffees[:5]:  # Show first 5
            print(f"- {coffee['coffee_name']}: {coffee['tasting_notes'][:100]}...")
        
        # Search for low bitterness and low sourness coffees
        print("\n=== Low Bitterness & Low Sourness Coffees (Sample) ===")
        mild_coffees = [coffee for coffee in all_coffees if "Bitterness: Low" in coffee['tasting_notes'] and "Sourness: Low" in coffee['tasting_notes']]
        for coffee in mild_coffees[:5]:  # Show first 5
            print(f"- {coffee['coffee_name']}: {coffee['tasting_notes'][:100]}...")
        
        # Get a specific coffee by name
        print("\n=== Getting Specific Coffee ===")
        sample_coffee = manager.get_coffee_by_name("Ethiopian Yirgacheffe - Batch 001")
        if sample_coffee:
            print(f"Found: {sample_coffee['coffee_name']}")
            print(f"ID: {sample_coffee['_id']}")
            print(f"Roasting Level: {sample_coffee['roasting_level']}")
            print(f"Full Tasting Notes: {sample_coffee['tasting_notes']}")
        
        # Update a coffee
        print("\n=== Updating Coffee ===")
        if sample_coffee:
            updated = manager.update_coffee(
                sample_coffee['_id'],
                tasting_notes="Updated: Bright acidity with floral notes, citrus, jasmine, and a hint of blueberry. Bitterness: Low. Sourness: High."
            )
            if updated:
                print("Successfully updated coffee tasting notes")
                
                # Show the updated coffee
                updated_coffee = manager.get_coffee_by_id(sample_coffee['_id'])
                print(f"New tasting notes: {updated_coffee['tasting_notes']}")
        
        # Show comprehensive database statistics
        print("\n=== Database Statistics ===")
        stats = manager.get_stats()
        print(f"Total coffees: {stats['total_coffees']}")
        print(f"Available roasting levels: {', '.join(stats['roasting_levels'])}")
        print(f"Available grinding levels: {', '.join(stats['grinding_levels'])}")
        
        # Additional statistics about bitterness and sourness
        print("\n=== Bitterness & Sourness Analysis ===")
        bitterness_counts = {}
        sourness_counts = {}
        
        for coffee in all_coffees:
            # Extract bitterness level
            if "Bitterness: Very Low" in coffee['tasting_notes']:
                bitterness_counts["Very Low"] = bitterness_counts.get("Very Low", 0) + 1
            elif "Bitterness: Low" in coffee['tasting_notes']:
                bitterness_counts["Low"] = bitterness_counts.get("Low", 0) + 1
            elif "Bitterness: Medium-Low" in coffee['tasting_notes']:
                bitterness_counts["Medium-Low"] = bitterness_counts.get("Medium-Low", 0) + 1
            elif "Bitterness: Medium" in coffee['tasting_notes']:
                bitterness_counts["Medium"] = bitterness_counts.get("Medium", 0) + 1
            elif "Bitterness: High" in coffee['tasting_notes']:
                bitterness_counts["High"] = bitterness_counts.get("High", 0) + 1
            
            # Extract sourness level
            if "Sourness: Low" in coffee['tasting_notes']:
                sourness_counts["Low"] = sourness_counts.get("Low", 0) + 1
            elif "Sourness: Medium" in coffee['tasting_notes']:
                sourness_counts["Medium"] = sourness_counts.get("Medium", 0) + 1
            elif "Sourness: Medium-High" in coffee['tasting_notes']:
                sourness_counts["Medium-High"] = sourness_counts.get("Medium-High", 0) + 1
            elif "Sourness: High" in coffee['tasting_notes']:
                sourness_counts["High"] = sourness_counts.get("High", 0) + 1
        
        print("Bitterness distribution:")
        for level, count in sorted(bitterness_counts.items()):
            print(f"  {level}: {count} coffees")
        
        print("\nSourness distribution:")
        for level, count in sorted(sourness_counts.items()):
            print(f"  {level}: {count} coffees")
        
        # Demonstrate deletion (optional - uncomment to test)
        # print("\n=== Deleting Sample Coffee ===")
        # if sample_coffee:
        #     deleted = manager.delete_coffee(sample_coffee['_id'])
        #     if deleted:
        #         print(f"Successfully deleted coffee with ID: {sample_coffee['_id']}")
        #         print(f"Remaining coffees: {manager.get_stats()['total_coffees']}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Always close the connection
        manager.close()
        print("\nConnection closed.")


if __name__ == "__main__":
    main()
