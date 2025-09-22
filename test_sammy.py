"""
Quick test script for SammyTheSpartanBarista - Brazilian coffee sourness issue.
"""

import os
from sammy_agent import SammyTheSpartanBarista


def test_brazilian_sourness():
    """Test Sammy with Brazilian coffee sourness problem."""
    
    # API key is now loaded from config.py
    print("🔑 Using API key from config.py")
    
    try:
        # Initialize Sammy
        sammy = SammyTheSpartanBarista()
        
        # Test message about Brazilian coffee sourness
        message = """
        I'm using Brazilian coffee beans, but my brew is coming out too sour. 
        How can I fix this? I'm using a V60 pour-over method with a 1:16 ratio.
        Can you be very specific and give me few examples from the database of brews that are similar to mine but less sour?
        When sharing these examples please share the experiment id and when it was brewed.
        """
        
        print("🤖 Testing Sammy with Brazilian coffee sourness issue...")
        print(f"User message: {message.strip()}")
        print("\n" + "="*60)
        print("SAMMY'S RESPONSE:")
        print("="*60)
        
        response = sammy.chat_with_sammy(message)
        print(response)
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        if 'sammy' in locals():
            sammy.close()


if __name__ == "__main__":
    test_brazilian_sourness()
