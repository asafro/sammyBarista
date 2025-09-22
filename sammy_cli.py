#!/usr/bin/env python3
"""
SammyTheSpartanBarista CLI - Interactive coffee expert agent
Usage: python3 sammy_cli.py --coffee-question "Your coffee question here"
"""

import argparse
import sys
from sammy_agent import SammyTheSpartanBarista


def main():
    """Main CLI function for SammyTheSpartanBarista."""
    
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="SammyTheSpartanBarista - Your AI Coffee Expert",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 sammy_cli.py --coffee-question "I want medium roast coffee recommendations"
  python3 sammy_cli.py --coffee-question "What's the best brewing method for Colombian coffee?"
  python3 sammy_cli.py --coffee-question "My coffee is too sour, how can I fix it?"
  python3 sammy_cli.py --coffee-question "Analyze the profile of Ethiopian Yirgacheffe"
        """
    )
    
    parser.add_argument(
        '--coffee-question',
        required=True,
        help='Your coffee question or request for Sammy to answer'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed execution logs'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    print("🤖 SammyTheSpartanBarista - AI Coffee Expert")
    print("=" * 60)
    print(f"📝 Your Question: {args.coffee_question}")
    print("=" * 60)
    
    try:
        # Initialize Sammy
        print("🔧 Initializing Sammy...")
        sammy = SammyTheSpartanBarista()
        
        if args.verbose:
            print("✅ Sammy initialized successfully!")
            print(f"📊 Database contains {sammy.coffee_manager.get_stats()['total_coffees']} coffee experiments")
        
        print("\n🤔 Processing your question...")
        
        # Process the question using chat_with_sammy
        response = sammy.chat_with_sammy(args.coffee_question)
        
        print("\n" + "=" * 60)
        print("☕ SAMMY'S RESPONSE:")
        print("=" * 60)
        print(response)
        print("=" * 60)
        
        if args.verbose:
            print(f"\n📁 Log saved to: {sammy.log_filename}")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Interrupted by user")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)
        
    finally:
        if 'sammy' in locals():
            sammy.close()
            print("\n👋 Sammy session ended. Thanks for chatting!")


if __name__ == "__main__":
    main()
