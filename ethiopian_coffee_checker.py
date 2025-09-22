"""
Ethiopian Coffee Checker - Counts Ethiopian medium roast coffee entries in the database.
"""

from coffee_manager import CoffeeDataManager


def check_ethiopian_medium_roast():
    """
    Check how many Ethiopian coffee entries are medium roasted in the database.
    
    Returns:
        dict: Dictionary containing count and details of Ethiopian medium roast coffees
    """
    
    # Initialize the coffee manager
    print("Connecting to coffee database...")
    manager = CoffeeDataManager()
    
    try:
        # Get all coffees from the database
        print("Retrieving all coffee entries...")
        all_coffees = manager.get_all_coffees()
        
        # Filter for Ethiopian coffees
        print("Filtering for Ethiopian coffees...")
        ethiopian_coffees = [
            coffee for coffee in all_coffees 
            if "Ethiopian" in coffee['coffee_name']
        ]
        
        # Filter for medium roast Ethiopian coffees
        print("Filtering for medium roast Ethiopian coffees...")
        ethiopian_medium_roast = [
            coffee for coffee in ethiopian_coffees 
            if coffee['roasting_level'] == "Medium"
        ]
        
        # Display results
        print("\n" + "="*60)
        print("ETHIOPIAN COFFEE ANALYSIS")
        print("="*60)
        
        print(f"Total coffees in database: {len(all_coffees)}")
        print(f"Total Ethiopian coffees: {len(ethiopian_coffees)}")
        print(f"Ethiopian medium roast coffees: {len(ethiopian_medium_roast)}")
        
        if ethiopian_medium_roast:
            print(f"\nPercentage of Ethiopian coffees that are medium roasted: "
                  f"{(len(ethiopian_medium_roast) / len(ethiopian_coffees) * 100):.1f}%")
        
        # Show details of Ethiopian medium roast coffees
        if ethiopian_medium_roast:
            print(f"\nDETAILS OF ETHIOPIAN MEDIUM ROAST COFFEES:")
            print("-" * 50)
            
            for i, coffee in enumerate(ethiopian_medium_roast, 1):
                print(f"{i}. {coffee['coffee_name']}")
                print(f"   ID: {coffee['_id']}")
                print(f"   Roasting Level: {coffee['roasting_level']}")
                print(f"   Grinding Level: {coffee['grinding_level']}")
                print(f"   Brewing Ratio: {coffee['brewing_ratio']}")
                print(f"   Tasting Notes: {coffee['tasting_notes']}")
                print()
        else:
            print("\nNo Ethiopian medium roast coffees found in the database.")
        
        # Show roasting level distribution for Ethiopian coffees
        if ethiopian_coffees:
            print("ROASTING LEVEL DISTRIBUTION FOR ETHIOPIAN COFFEES:")
            print("-" * 50)
            
            roasting_levels = {}
            for coffee in ethiopian_coffees:
                level = coffee['roasting_level']
                roasting_levels[level] = roasting_levels.get(level, 0) + 1
            
            for level, count in sorted(roasting_levels.items()):
                percentage = (count / len(ethiopian_coffees)) * 100
                print(f"{level}: {count} coffees ({percentage:.1f}%)")
        
        # Return summary data
        return {
            "total_coffees": len(all_coffees),
            "ethiopian_coffees": len(ethiopian_coffees),
            "ethiopian_medium_roast": len(ethiopian_medium_roast),
            "ethiopian_medium_roast_percentage": (len(ethiopian_medium_roast) / len(ethiopian_coffees) * 100) if ethiopian_coffees else 0,
            "roasting_distribution": roasting_levels if ethiopian_coffees else {},
            "ethiopian_medium_roast_details": ethiopian_medium_roast
        }
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
        
    finally:
        # Close the connection
        manager.close()
        print("\nDatabase connection closed.")


def main():
    """Main function to run the Ethiopian coffee checker."""
    
    print("Ethiopian Coffee Database Checker")
    print("Checking for Ethiopian medium roast coffee entries...\n")
    
    # Run the check
    results = check_ethiopian_medium_roast()
    
    if results:
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"Ethiopian medium roast coffees found: {results['ethiopian_medium_roast']}")
        print(f"Out of {results['ethiopian_coffees']} total Ethiopian coffees")
        print(f"Percentage: {results['ethiopian_medium_roast_percentage']:.1f}%")
        
        if results['ethiopian_medium_roast'] > 0:
            print(f"\nAll Ethiopian medium roast coffee names:")
            for coffee in results['ethiopian_medium_roast_details']:
                print(f"  - {coffee['coffee_name']}")
    else:
        print("Failed to retrieve data from the database.")


if __name__ == "__main__":
    main()
