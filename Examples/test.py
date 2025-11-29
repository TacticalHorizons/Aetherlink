#!/usr/bin/env python3
"""
Basic AetherLink Usage Example - DeepSeek Edition
Simple chat interface demonstrating the core functionality
"""

from aetherlink.aetherlink import AetherLink

def simple_chat():
    """Basic interactive chat example"""
    print("🚀 AetherLink Basic Chat Example")
    print("=" * 40)
    
    # Initialize the bot
    bot = AetherLink(
        headless=False,  # Show browser for first-time setup
        instructions="You are a helpful and friendly AI assistant by the name Orion",
        verbose=True     # Show status messages
    )
    
    try:
        # Check if we're already logged in
        print("\n🔐 Checking for existing session...")
        if not bot.load_session_data() or not bot.is_logged_in():
            print("No valid session found. Starting setup...")
            if not bot.setup():
                print("Setup failed. Please try again.")
                return
        else:
            print("✅ Session loaded successfully!")
        
        print("\n💬 Chat session started! Type 'quit' to exit.")
        print("Type 'clear' to start new conversation")
        print("Type 'history' to see chat history")
        print("=" * 40)
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'clear':
                bot.clear_chat_history()
                print("🆕 New conversation started")
                continue
            elif user_input.lower() == 'history':
                history = bot.get_chat_history()
                print(f"\n📜 Chat History ({len(history)} messages):")
                for i, msg in enumerate(history, 1):
                    role = "You" if msg["role"] == "user" else "Assistant"
                    preview = msg['content'][:80] + "..." if len(msg['content']) > 80 else msg['content']
                    print(f"  {i}. {role}: {preview}")
                continue
            elif not user_input:
                continue
                
            # Send message and get response
            response = bot.send_message(user_input)
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Chat interrupted by user")
        bot.close()
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        bot.close()
        print("👋 Goodbye!")

if __name__ == "__main__":
    simple_chat()