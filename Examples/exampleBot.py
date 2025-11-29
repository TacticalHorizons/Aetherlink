#!/usr/bin/env python3
"""
AetherLink Platform - Example Bot Script
Simple demonstration bot with a random number command
"""

from aetherlink.aetherlink import AetherLink
import random

class ExampleBot:
    def __init__(self):
        self.bot = None
        
    def setup_bot(self):
        """Initialize and setup the example bot"""
        # Initialize the bot
        self.bot = AetherLink(
            headless=False,
            instructions="You are an example bot for the AetherLink Platform. You can generate random numbers and help with basic questions.",
            verbose=True
        )
        
        # Register example custom commands
        self._register_commands()
        
        return self.bot
    
    def _register_commands(self):
        """Register example custom commands"""
        
        def random_number_handler(args):
            """Generate a random number between 1-100 or custom range"""
            if not args:
                return f"🎲 Your random number: {random.randint(1, 100)}"
            
            try:
                if len(args) == 1:
                    max_num = int(args[0])
                    return f"🎲 Your random number (1-{max_num}): {random.randint(1, max_num)}"
                elif len(args) == 2:
                    min_num = int(args[0])
                    max_num = int(args[1])
                    return f"🎲 Your random number ({min_num}-{max_num}): {random.randint(min_num, max_num)}"
                else:
                    return "Error: Usage: <!random> or <!random max> or <!random min max>"
            except ValueError:
                return "Error: Please provide valid numbers"
        
        # Register the random command
        self.bot.register_command(
            "random", 
            random_number_handler,
            "Generate random number: <!random> or <!random 50> or <!random 10 20>"
        )

def example_chat():
    """Example chat session with the bot"""
    print("AetherLink Platform - Example Bot")
    print("=" * 40)
    
    example_bot = ExampleBot()
    
    try:
        # Setup the bot
        bot = example_bot.setup_bot()
        
        # Check for existing session
        print("\nChecking for existing session...")
        if not bot.load_session_data() or not bot.is_logged_in():
            print("No valid session found. Starting setup...")
            if not bot.setup():
                print("Setup failed. Please try again.")
                return
        else:
            print("Session loaded successfully!")
        
        print("\nExample Bot Initialized!")
        print("\nType 'quit' to exit")
        print("=" * 40)
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif not user_input:
                continue
                
            # Send message and get response
            print("\nBot: ", end="", flush=True)
            response = bot.send_message(user_input)
            
    except KeyboardInterrupt:
        if example_bot.bot:
            example_bot.bot.close()
        print("\n\nChat interrupted by user")
    except Exception as e:
        if example_bot.bot:
            example_bot.bot.close()
        print(f"\nError: {e}")
    finally:
        if example_bot.bot:
            example_bot.bot.close()
        print("Thank you for trying the AetherLink Example Bot!")

if __name__ == "__main__":
    example_chat()