#!/usr/bin/env python3
"""
Potentially outdated, haven't checked. (Written on AetherLink 2.5.X)

Enhanced AetherLink Bakery Example - DeepSeek Edition
Customer service bot with product pricing commands
"""

from aetherlink.aetherlink import AetherLink

class BakeryBot:
    def __init__(self):
        self.bot = None
        self.product_prices = {
            "lemon": 3.50,
            "triple choco": 4.25, 
            "vanilla": 3.75,
            "lemon donut": 3.50,
            "triple choco donut": 4.25,
            "vanilla donut": 3.75,
            "donut": 3.50,  # base price
        }
        
    def setup_bot(self):
        """Initialize and setup the bot with bakery-specific commands"""
        # Initialize the bot
        self.bot = AetherLink(
            headless=False,
            instructions="You are a customer service bot for Digital Bakings - a gluten-free bakery that sells three types of donuts: lemon, triple choco, and vanilla. You can check prices, calculate totals, and help customers with orders.",
            verbose=False
        )
        
        # Register bakery-specific custom commands
        self._register_bakery_commands()
        
        return self.bot
    
    def _register_bakery_commands(self):
        """Register all bakery-specific custom commands"""
        
        def price_check_handler(args):
            """Check prices for bakery products"""
            if not args:
                return "Error: Please specify a product. Usage: <!price_check product_name>"
            
            product = " ".join(args).lower().strip()
            
            # Handle variations and synonyms
            product_mapping = {
                "lemon": "lemon",
                "lemon donut": "lemon",
                "triple choco": "triple choco", 
                "triple chocolate": "triple choco",
                "triple choco donut": "triple choco",
                "vanilla": "vanilla",
                "vanilla donut": "vanilla",
                "donut": "donut"
            }
            
            # Find matching product
            matched_product = None
            for key, value in product_mapping.items():
                if product in key:
                    matched_product = value
                    break
            
            if matched_product and matched_product in self.product_prices:
                price = self.product_prices[matched_product]
                return f"💰 {matched_product.title()} Donut: ${price:.2f} each"
            else:
                available_products = ", ".join([f"{p.title()} (${self.product_prices[p]:.2f})" 
                                              for p in ["lemon", "triple choco", "vanilla"]])
                return f"❌ Product '{product}' not found. Available: {available_products}"
        
        def menu_handler(args):
            """Show the full menu with prices"""
            menu_text = "📋 Digital Bakings Menu (All Gluten-Free):\n"
            menu_text += f"• 🍋 Lemon Donut: ${self.product_prices['lemon']:.2f}\n"
            menu_text += f"• 🍫 Triple Choco Donut: ${self.product_prices['triple choco']:.2f}\n" 
            menu_text += f"• 🍨 Vanilla Donut: ${self.product_prices['vanilla']:.2f}\n"
            menu_text += f"\n💡 Special: Buy 6+ donuts and get 10% off!"
            return menu_text
        
        def calculate_total_handler(args):
            """Calculate total cost for an order"""
            if len(args) < 2:
                return "Error: Usage: <!calculate_total product quantity> or <!calculate_total lemon 3 triple_choco 2>"
            
            # Parse product quantities
            order = {}
            i = 0
            while i < len(args):
                try:
                    product = args[i].lower()
                    quantity = int(args[i + 1])
                    order[product] = order.get(product, 0) + quantity
                    i += 2
                except (ValueError, IndexError):
                    # Try to handle product names with spaces
                    if i + 2 < len(args):
                        try:
                            combined_product = f"{args[i]} {args[i+1]}"
                            quantity = int(args[i + 2])
                            order[combined_product] = order.get(combined_product, 0) + quantity
                            i += 3
                            continue
                        except ValueError:
                            pass
                    return "Error: Invalid format. Use: <!calculate_total product quantity [product quantity ...]>"
            
            # Calculate total
            total = 0
            breakdown = []
            
            for product, quantity in order.items():
                matched_price = None
                for price_product, price in self.product_prices.items():
                    if product in price_product:
                        matched_price = price
                        break
                
                if matched_price:
                    subtotal = matched_price * quantity
                    total += subtotal
                    breakdown.append(f"  {product.title()} x{quantity}: ${subtotal:.2f}")
                else:
                    return f"Error: Product '{product}' not found"
            
            # Apply bulk discount
            total_items = sum(order.values())
            discount = 0
            if total_items >= 6:
                discount = total * 0.10
                total -= discount
                breakdown.append(f"  Bulk Discount (10%): -${discount:.2f}")
            
            result = "🧾 Order Calculation:\n" + "\n".join(breakdown)
            result += f"\n💰 Total: ${total:.2f}"
            if discount > 0:
                result += f" (after ${discount:.2f} discount)"
            
            return result
        
        def specials_handler(args):
            """Show current specials and promotions"""
            specials = [
                "🎉 CURRENT SPECIALS:",
                "• 10% discount on orders of 6+ donuts",
                "• Mix & match any flavors", 
                "• All donuts are 100% gluten-free",
                "• Fresh baked daily",
                f"• Most popular: Triple Choco (${self.product_prices['triple choco']:.2f})"
            ]
            return "\n".join(specials)
        
        # Register all commands
        self.bot.register_command(
            "price_check", 
            price_check_handler,
            "Check product price: <!price_check lemon> or <!price_check triple choco>"
        )
        
        self.bot.register_command(
            "menu",
            menu_handler, 
            "Show full menu with prices: <!menu>"
        )
        
        self.bot.register_command(
            "calculate_total",
            calculate_total_handler,
            "Calculate order total: <!calculate_total lemon 2 vanilla 3>"
        )
        
        self.bot.register_command(
            "specials", 
            specials_handler,
            "Show current specials: <!specials>"
        )

def enhanced_bakery_chat():
    """Enhanced bakery customer service chat with pricing commands"""
    print("🏪 Digital Bakings - Customer Service Bot")
    print("=" * 50)
    
    bakery_bot = BakeryBot()
    
    try:
        # Setup the bot with bakery commands
        bot = bakery_bot.setup_bot()
        
        # Check if we're already logged in
        print("\n🔐 Checking for existing session...")
        if not bot.load_session_data() or not bot.is_logged_in():
            print("No valid session found. Starting setup...")
            if not bot.setup():
                print("Setup failed. Please try again.")
                return
        else:
            print("✅ Session loaded successfully!")
        
        print("\n💬 Welcome to Digital Bakings!")
        print("We sell gluten-free donuts in 3 flavors:")
        print("  🍋 Lemon | 🍫 Triple Choco | 🍨 Vanilla")
        print("\n💡 I can help with:")
        print("  • Product prices and menu")
        print("  • Order calculations") 
        print("  • Current specials")
        print("  • General questions")
        print("\nType 'quit' to exit, 'clear' for new conversation")
        print("=" * 50)
        
        # Show initial menu
        print("\n" + bakery_bot.bot.execute_custom_command("menu"))
        
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
                    preview = msg['content'][:60] + "..." if len(msg['content']) > 60 else msg['content']
                    print(f"  {i}. {role}: {preview}")
                continue
            elif user_input.lower() == 'help':
                print("\n🆘 Available commands:")
                print("  • 'menu' - Show product menu")
                print("  • 'specials' - Show current promotions") 
                print("  • 'clear' - Start new conversation")
                print("  • 'history' - View chat history")
                print("  • 'quit' - Exit the chat")
                print("\n💡 Just ask naturally! I'll handle:")
                print("  • 'How much for lemon donuts?'")
                print("  • 'What's the price of triple choco?'")
                print("  • 'Can you calculate 2 lemon and 3 vanilla?'")
                continue
            elif not user_input:
                continue
                
            # Send message and get response
            print("\nAssistant: ", end="", flush=True)
            response = bot.send_message(user_input)
            
    except KeyboardInterrupt:
        if bakery_bot.bot:
            bakery_bot.bot.close()
        print("\n\n⏹️  Chat interrupted by user")
    except Exception as e:
        if bakery_bot.bot:
            bakery_bot.bot.close()
        print(f"\n❌ Error: {e}")
    finally:
        if bakery_bot.bot:
            bakery_bot.bot.close()
        print("👋 Thank you for visiting Digital Bakings!")

if __name__ == "__main__":
    enhanced_bakery_chat()
