import os
import sys
import time
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException, BinanceOrderException
from dotenv import load_dotenv

def print_section(title):
    print(f"\n{'='*50}")
    print(f"{title.upper():^50}")
    print(f"{'='*50}")

def print_step(step):
    print(f"\n🔹 {step}...")

def test_connection():
    print_section("Binance Testnet API Connection Test")
    
    # Load environment variables
    load_dotenv()
    
    # Get API keys from environment variables
    api_key = os.getenv("BINANCE_TESTNET_API_KEY") or os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_TESTNET_API_SECRET") or os.getenv("BINANCE_API_SECRET")
    
    if not api_key or not api_secret:
        print("❌ Error: API keys not found in environment variables")
        print("Please create a .env file with your Binance Testnet API keys")
        print("See .env.example for reference")
        return False
        
    print(f"🔑 Using API Key: {api_key[:8]}...{api_key[-4:]}")
    
    try:
        # Test 1: Initialize client
        print_step("Initializing Binance Client")
        client = Client(api_key, api_secret, testnet=True)
        print("✅ Client initialized successfully")
        
        # Test 2: Check server time
        print_step("Checking server time")
        server_time = client.get_server_time()
        print(f"✅ Server time: {server_time['serverTime']} ({time.ctime(server_time['serverTime']/1000)})")
        
        # Test 3: Get exchange info
        print_step("Fetching exchange info")
        exchange_info = client.futures_exchange_info()
        print(f"✅ Exchange info received. Rate limits:")
        for limit in exchange_info.get('rateLimits', [])[:2]:  # Show first 2 rate limits
            print(f"  - {limit['rateLimitType']}: {limit['limit']} requests per {limit['intervalNum']} {limit['interval']}")
        
        # Test 4: Get account balance
        print_step("Fetching account balance")
        try:
            account = client.futures_account_balance()
            print("✅ Account balance received")
            
            # Filter and print non-zero balances
            non_zero_balances = [b for b in account if float(b['balance']) > 0 or float(b['withdrawAvailable']) > 0]
            if non_zero_balances:
                print("\n💰 Non-zero balances:")
                for balance in non_zero_balances:
                    print(f"  - {balance['asset']}: {balance['balance']} (Available: {balance['withdrawAvailable']})")
            else:
                print("ℹ️ No non-zero balances found")
                
        except Exception as e:
            print(f"⚠️ Could not fetch account balance: {str(e)}")
        
        # Test 5: Get order book
        print_step("Testing order book")
        try:
            symbol = 'BTCUSDT'
            order_book = client.futures_order_book(symbol=symbol, limit=5)
            print(f"✅ {symbol} Order Book (Top 5):")
            print(f"  🔼 Bids: {order_book['bids'][0][0]:>10} (Qty: {order_book['bids'][0][1]:.4f})")
            print(f"  🔽 Asks: {order_book['asks'][0][0]:>10} (Qty: {order_book['asks'][0][1]:.4f})")
        except Exception as e:
            print(f"⚠️ Could not fetch order book: {str(e)}")
        
        return True
        
    except BinanceRequestException as e:
        print("\n❌ Binance Request Exception:")
        print(f"  - Status Code: {e.status_code}")
        print(f"  - Message: {e.message}")
        print(f"  - Request: {e.request}")
    except BinanceAPIException as e:
        print("\n❌ Binance API Exception:")
        print(f"  - Status Code: {e.status_code}")
        print(f"  - Error Code: {e.code}")
        print(f"  - Message: {e.message}")
        if e.status_code == 401:
            print("  🔒 Possible issues:")
            print("    1. Invalid API key/secret")
            print("    2. IP not whitelisted")
            print("    3. Missing required permissions")
        elif e.status_code == 429:
            print("  ⚠️ Rate limit exceeded. Please wait and try again.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {type(e).__name__}")
        print(f"  - {str(e)}")
    
    return False

if __name__ == "__main__":
    test_connection()
