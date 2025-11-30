# **AetherLink v2 — User Documentation**

AetherLink v2 is a high‑level Python wrapper designed to automate and control DeepSeek's chat interface using Selenium. It builds structured system prompts, preserves sessions, supports custom command injection, and provides a fully modular command registry.

---

### Some stuff I've been able to do with AetherLink:
* Group chats where multiple users can interact with the same AI, but like... in a group chat
* Shove multiple AIs into a single group chat and have them panic about their existence- (last part is a joke, but yes, you can)
* Customer support
* Moderation triages (very useful!)

---

# **1. Installation & Requirements**

AetherLink requires:

* Python 3.9+
* DeepSeek account
* Google Chrome/Chromium installed
* Matching ChromeDriver (usually auto‑handled by Selenium 4+)
* Libraries:

  * `selenium`
  * `beautifulsoup4`

### **Install dependencies:**

```sh
pip install selenium beautifulsoup4
```

Install AetherLink:
```sh
pip install git+https://github.com/tacticalhorizons/aetherlink.git
```

AetherLink automatically creates a directory called:

```
AetherLink_Requirements/
```

This stores cookies, localstorage, and user context.

---

# **2. Quick Start**

```python
from aetherlink_v2 import AetherLink

aether = AetherLink(headless=False, verbose=True)
aether.send_message("Hello!")
```

The first time you run this, you must manually log in.

### **Running first‑time setup**

```python
aether.setup()
```

Follow on‑screen instructions to log in. AetherLink will save cookies and future sessions will auto‑login.

---

# **3. Sending Messages**

### **Basic usage:**

```python
response = aether.send_message("Write me a haiku about galaxies.")
print(response)
```

AetherLink automatically:

1. Builds the system prompt
2. Sends it to DeepSeek
3. Streams the response
4. Executes any detected commands
5. Reprompts the model if commands produced results

All visible to you, but invisible to the end user. (Still visible if verbose mode is enabled!)

---

# **4. Headless Mode**

You can run AetherLink without showing Chrome:

```python
aether = AetherLink(headless=True)
```

If a CAPTCHA appears, AetherLink automatically restarts in non‑headless mode.

---

# **5. System Instructions**

You can provide your own deployment instructions:

```python
aether = AetherLink(
    instructions="You are a bot that writes code comments in pirate-speak!"
)
```

These merge with AetherLink’s core instruction set.

---

# **6. User Context**

AetherLink stores context across sessions.

### **Direct control:**

```python
aether.set_user_context_directly("favorite_color", "blue")
```

### **Retrieve context:**

```python
ctx = aether.get_user_context()
```

### **Delete context entry:**

```python
aether.delete_user_context("favorite_color")
```

Context is persistent across runs.

---

# **7. Chat History**

AetherLink saves recent dialogue and includes it in prompts.

### **Get chat history:**

```python
history = aether.get_chat_history()
```

### **Clear chat history:**

```python
aether.clear_chat_history()
```

---

*These are included with AetherLink by default, but may be disabled by default in future versions.
**More wrapper commands will be included in future versions, such as private reasoning and chat context (which doesn't rely on memory), among others.

# **8. Custom Commands System**

AetherLink v2 introduces a complete modular command registry.

Commands follow the format:

```
<!command_name args...>
```

When the model outputs one, AetherLink:

1. Detects it
2. Executes the registered handler
3. Reprompts DeepSeek with the result
4. Produces a final clean answer for the user

### **Register a custom command:**

```python
def greet(args):
    return "Hello, " + " ".join(args)

aether.register_command(
    "greet", greet,
    "Greets someone: <!greet NAME>"
)
```

### **Use it in conversation:**

The model may say:

```
Let me greet you: <!greet Dani>
```

You will then get the final answer after the reprompt.

### **List all commands:**

```python
aether.get_registered_commands()
```

### **Remove a command:**

```python
aether.unregister_command("greet")
```

---

# **9. Example Custom Commands Included**

AetherLink ships with 3 demo commands:

| Command         | Description                  | Example             |
| --------------- | ---------------------------- | ------------------- |
| `<!live_price>` | Fake crypto/stock prices     | `<!live_price BTC>` |
| `<!weather>`    | Fake weather info            | `<!weather Tokyo>`  |
| `<!calc>`       | Simple arithmetic calculator | `<!calc 2 + 2>`     |

These can be removed or replaced.

*In future versions, the demo commands will no longer be included by default. They will be placed in the example script instead.

---

# **10. Browser Reliability Functions**

AetherLink includes stable helpers:

* Automatic input box detection
* Anti‑automation flag removal
* Custom text injection that supports emojis
* Stream reading via DOM scraping

Nothing from the site structure needs changing.

---

# **11. Session Persistence**

AetherLink saves:

* Cookies
* Localstorage
* User context

This ensures DeepSeek stays logged in.

### **Manually save session:**

```python
aether.save_session_data()
```

### **Manually load session:**

```python
aether.load_session_data()
```

---

# **12. Closing the Browser**

Always close sessions when done:

```python
aether.close()
```

Chrome will fully shut down.

---

# **13. Advanced: Overriding System Instructions**

You can fully replace the instruction block:

```python
aether.update_instructions("Only speak in binary.")
```

---

# **14. Full Example**

```python
from aetherlink_v2 import AetherLink

aether = AetherLink(headless=False)

# Register a custom echo command
def echo_handler(args):
    return "Echo: " + " ".join(args)

aether.register_command("echo", echo_handler, "Echo: <!echo text>")

print(aether.send_message("Say hello and run <!echo test>"))

aether.close()
```

---

# **15. Troubleshooting**

### **Input box not found**

DeepSeek may update UI. AetherLink tries multiple selectors. Restarting Chrome often fixes this.

### **CAPTCHA appears in headless**

AetherLink automatically switches to non‑headless mode.

### **Model executing too many commands**

Just unregister the commands you don't want.

### **Chrome fails to launch**

Ensure you have:

* The latest Chrome installed
* Selenium updated

---

# **16. Full Example Bot Script (Recommended Template)**

Below is a full, realistic example bot implementation using AetherLink v2.
This script shows how to:

* Initialize an AetherLink-based bot
* Register commands
* Maintain sessions
* Use a simple command (`<!random>`) that the bot can execute
* Run an interactive chat loop

```python
#!/usr/bin/env python3
"""
AetherLink Platform - Example Bot Script
Simple demonstration bot with a random number command
"""

from aetherlink_v2 import AetherLink
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
        print("
Checking for existing session...")
        if not bot.load_session_data() or not bot.is_logged_in():
            print("No valid session found. Starting setup...")
            if not bot.setup():
                print("Setup failed. Please try again.")
                return
        else:
            print("Session loaded successfully!")
        
        print("
Example Bot Initialized!")
        print("
Type 'quit' to exit")
        print("=" * 40)
        
        while True:
            user_input = input("
You: ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif not user_input:
                continue
                
            # Send message and get response
            print("
Bot: ", end="", flush=True)
            response = bot.send_message(user_input)
        
    except KeyboardInterrupt:
        if example_bot.bot:
            example_bot.bot.close()
        print("

Chat interrupted by user")
    except Exception as e:
        if example_bot.bot:
            example_bot.bot.close()
        print(f"
Error: {e}")
    finally:
        if example_bot.bot:
            example_bot.bot.close()
        print("Thank you for trying the AetherLink Example Bot!")

if __name__ == "__main__":
    example_chat()
```

---

# **17. Conclusion**

AetherLink v2 provides a flexible, high‑level interface for automating DeepSeek with powerful custom command injection, session persistence, and robust browser automation. It is suitable for bots, agents, and advanced automation workflows.

For advanced features, explore:

* Command chaining
* Custom system instructions
* Rich user context management
* Integration with external data sources

Happy building!
