import os
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv

def main():
    print("🔍 Testing Binance Testnet API connection...")
    
    # Load environment variables
    load_dotenv()
    
    # Get API keys from environment variables
    api_key = os.getenv("BINANCE_TESTNET_API_KEY") or os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_TESTNET_API_SECRET") or os.getenv("BINANCE_API_SECRET")
    
    if not api_key or not api_secret:
        print("❌ Error: API keys not found in environment variables")
        print("Please create a .env file with your Binance Testnet API keys")
        print("See .env.example for reference")
        return
    
    print(f"🔑 Using API Key: {api_key[:8]}...{api_key[-4:]}")
    
    try:
        # Initialize client
        print("🚀 Initializing client...")
        client = Client(api_key, api_secret, testnet=True)
        
        # Test server time
        print("🕒 Getting server time...")
        time = client.get_server_time()
        print(f"✅ Server time: {time['serverTime']}")
        
        # Test futures exchange info
        print("📊 Getting exchange info...")
        info = client.futures_exchange_info()
        print(f"✅ Exchange info received. Rate limits:")
        for limit in info['rateLimits'][:2]:
            print(f"  - {limit['rateLimitType']}: {limit['limit']} requests per {limit['intervalNum']} {limit['interval']}")
        
        # Test account balance
        print("💰 Getting account balance...")
        balance = client.futures_account_balance()
        print("✅ Account balance received")
        for asset in balance:
            if float(asset['balance']) > 0:
                print(f"  - {asset['asset']}: {asset['balance']}")
        
        # Test order book
        print("📈 Getting order book...")
        orderbook = client.futures_order_book(symbol='BTCUSDT', limit=5)
        print(f"✅ Order book received. Best bid: {orderbook['bids'][0][0]}, Best ask: {orderbook['asks'][0][0]}")
        
        print("\n🎉 All tests passed successfully!")
        
    except BinanceAPIException as e:
        print(f"❌ Binance API Error ({e.status_code}): {e.message}")
        if e.status_code == 401:
            print("  - Invalid API key/secret or permissions")
        elif e.status_code == 403:
            print("  - IP address not whitelisted")
        elif e.status_code == 429:
            print("  - Rate limit exceeded")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
