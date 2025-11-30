#!/usr/bin/env python3
"""
Potentially outdated, haven't checked. (Written on AetherLink 2.4.X)

AetherLink Quick Start
This has been updated to the latest version of AetherLink which is easier to use!
"""

from aetherlink.aetherlink import AetherLink

# Create instance with auto-setup
bot = AetherLink(
    instructions="You are a helpful assistant.",
    auto_setup=True,  # Automatically handles login
    verbose=True
)

# Quick chat example
response = bot.quick_chat("Hello! What can you help me with?")
print(f"🤖: {response}")

# Check session status
info = bot.get_session_info()
print(f"📊 Session: {info}")

# Add custom commands easily
def fake_price(args):
    return f"💰 Price for {args[0] if args else 'BTC'}: $42,000 (example)"

bot.register_command("price", fake_price, "Get fake price data")
bot.register_command("status", lambda args: "✅ All systems operational", "Check status")

# Use custom commands
print(bot.execute_custom_command("price BTC"))
print(bot.list_commands())

bot.close()
