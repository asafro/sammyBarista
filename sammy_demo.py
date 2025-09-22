"""
Demo script for SammyTheSpartanBarista AI agent.
"""

import os
from sammy_agent import SammyTheSpartanBarista


def main():
    """Demo the SammyTheSpartanBarista agent functionality."""
    
    print("🤖 Welcome to SammyTheSpartanBarista Demo! ☕")
    print("=" * 50)
    
    # API key is now loaded from config.py
    print("🔑 Using API key from config.py")
    
    try:
        # Initialize Sammy
        print("Initializing SammyTheSpartanBarista...")
        sammy = SammyTheSpartanBarista()
        print("✅ Sammy is ready to help with your coffee needs!\n")
        
        # Demo 1: Coffee recommendations
        print("📋 Demo 1: Coffee Recommendations")
        print("-" * 30)
        preferences = {
            "roasting_level": "Medium",
            "grinding_level": "Medium"
        }
        print(f"Getting recommendations for: {preferences}")
        recommendations = sammy.get_coffee_recommendation(preferences)
        print(f"Sammy's recommendations:\n{recommendations}\n")
        
        # Demo 2: Coffee analysis
        print("🔍 Demo 2: Coffee Profile Analysis")
        print("-" * 30)
        coffee_name = "Ethiopian Yirgacheffe - Batch 001"
        print(f"Analyzing: {coffee_name}")
        analysis = sammy.analyze_coffee_profile(coffee_name)
        print(f"Sammy's analysis:\n{analysis}\n")
        
        # Demo 3: Brewing guide
        print("📚 Demo 3: Brewing Guide")
        print("-" * 30)
        brewing_method = "V60"
        print(f"Getting brewing guide for: {brewing_method}")
        guide = sammy.get_brewing_guide(brewing_method, "Ethiopian")
        print(f"Sammy's brewing guide:\n{guide}\n")
        
        # Demo 4: Chat with Sammy
        print("💬 Demo 4: Chat with Sammy")
        print("-" * 30)
        questions = [
            "What's the difference between light and dark roast coffee?",
            "How do I choose the right grind size for my brewing method?",
            "What makes Ethiopian coffee special?"
        ]
        
        for question in questions:
            print(f"Question: {question}")
            response = sammy.chat_with_sammy(question)
            print(f"Sammy: {response}\n")
            print("-" * 40)
        
        print("🎉 Demo completed! Sammy is ready for your coffee adventures!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure your OPENROUTER_API_KEY is set correctly")
    
    finally:
        if 'sammy' in locals():
            sammy.close()
            print("👋 Sammy says goodbye!")


if __name__ == "__main__":
    main()
