"""
Examples demonstrating the new get_coffee_with_query function.
"""

from coffee_manager import CoffeeDataManager


def demonstrate_query_functionality():
    """Demonstrate the flexible query functionality."""
    
    # Initialize the coffee manager
    print("Connecting to coffee database...")
    manager = CoffeeDataManager()
    
    try:
        print("\n" + "="*60)
        print("DEMONSTRATING get_coffee_with_query FUNCTIONALITY")
        print("="*60)
        
        # Example 1: Single field query
        print("\n1. Find all medium roast coffees:")
        medium_coffees = manager.get_coffee_with_query({"roasting_level": "Medium"})
        print(f"   Found {len(medium_coffees)} medium roast coffees")
        for coffee in medium_coffees[:3]:  # Show first 3
            print(f"   - {coffee['coffee_name']}")
        
        # Example 2: Multiple field query
        print("\n2. Find Ethiopian coffees with fine grinding:")
        ethiopian_fine = manager.get_coffee_with_query({
            "coffee_name": "Ethiopian", 
            "grinding_level": "Fine"
        })
        print(f"   Found {len(ethiopian_fine)} Ethiopian fine ground coffees")
        for coffee in ethiopian_fine[:3]:  # Show first 3
            print(f"   - {coffee['coffee_name']} ({coffee['grinding_level']})")
        
        # Example 3: Query by brewing ratio
        print("\n3. Find coffees with 1:15 brewing ratio:")
        ratio_coffees = manager.get_coffee_with_query({"brewing_ratio": "1:15"})
        print(f"   Found {len(ratio_coffees)} coffees with 1:15 ratio")
        for coffee in ratio_coffees[:3]:  # Show first 3
            print(f"   - {coffee['coffee_name']} ({coffee['brewing_ratio']})")
        
        # Example 4: Query by tasting notes (bitterness)
        print("\n4. Find coffees with high bitterness:")
        high_bitter = manager.get_coffee_with_query({"tasting_notes": "Bitterness: High"})
        print(f"   Found {len(high_bitter)} high bitterness coffees")
        for coffee in high_bitter[:3]:  # Show first 3
            print(f"   - {coffee['coffee_name']}")
        
        # Example 5: Query by tasting notes (sourness)
        print("\n5. Find coffees with high sourness:")
        high_sour = manager.get_coffee_with_query({"tasting_notes": "Sourness: High"})
        print(f"   Found {len(high_sour)} high sourness coffees")
        for coffee in high_sour[:3]:  # Show first 3
            print(f"   - {coffee['coffee_name']}")
        
        # Example 6: Complex query - Colombian medium roast with specific ratio
        print("\n6. Find Colombian coffees that are medium roasted with 1:16 ratio:")
        complex_query = manager.get_coffee_with_query({
            "coffee_name": "Colombian",
            "roasting_level": "Medium", 
            "brewing_ratio": "1:16"
        })
        print(f"   Found {len(complex_query)} matching coffees")
        for coffee in complex_query:
            print(f"   - {coffee['coffee_name']} ({coffee['roasting_level']}, {coffee['brewing_ratio']})")
        
        # Example 7: Case sensitive vs case insensitive
        print("\n7. Case sensitive vs case insensitive search:")
        case_insensitive = manager.get_coffee_with_query({"roasting_level": "medium"}, case_sensitive=False)
        case_sensitive = manager.get_coffee_with_query({"roasting_level": "medium"}, case_sensitive=True)
        print(f"   Case insensitive 'medium': {len(case_insensitive)} results")
        print(f"   Case sensitive 'medium': {len(case_sensitive)} results")
        
        # Example 8: Query with multiple grinding levels
        print("\n8. Find coffees with fine or medium-fine grinding:")
        fine_coffees = manager.get_coffee_with_query({"grinding_level": "Fine"})
        medium_fine_coffees = manager.get_coffee_with_query({"grinding_level": "Medium-Fine"})
        print(f"   Fine grinding: {len(fine_coffees)} coffees")
        print(f"   Medium-Fine grinding: {len(medium_fine_coffees)} coffees")
        
        print("\n" + "="*60)
        print("QUERY DEMONSTRATION COMPLETE")
        print("="*60)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        manager.close()
        print("\nConnection closed.")


def main():
    """Main function to run the query examples."""
    demonstrate_query_functionality()


if __name__ == "__main__":
    main()
