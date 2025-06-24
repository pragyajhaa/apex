import os
import sys
import logging
import argparse
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv


class BasicBot:
    def __init__(self, api_key=None, api_secret=None, testnet=True):
        """Initialize the trading bot with API credentials and set up logging."""
        if not testnet:
            raise ValueError("Only testnet mode is supported. Set testnet=True.")

        # Load from environment variables or use provided values
        # Try to get testnet-specific keys first, fall back to main keys
        load_dotenv()
        env_api_key = os.getenv("BINANCE_TESTNET_API_KEY") or os.getenv("BINANCE_API_KEY")
        env_api_secret = os.getenv("BINANCE_TESTNET_API_SECRET") or os.getenv("BINANCE_API_SECRET")

        self.api_key = env_api_key or api_key
        self.api_secret = env_api_secret or api_secret

        if not self.api_key or not self.api_secret:
            raise ValueError("API keys must be provided via .env or constructor")

        self.client = Client(self.api_key, self.api_secret, testnet=True)
        self._setup_logging()
        self._validate_connection()

    def _setup_logging(self):
        """Configure logging to both file and console."""
        self.logger = logging.getLogger("BasicBot")
        self.logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s - %(message)s', 
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler = logging.FileHandler('bot.log')
        file_handler.setFormatter(formatter)
        
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        
        if not self.logger.hasHandlers():
            self.logger.addHandler(file_handler)
            self.logger.addHandler(stream_handler)

    def _validate_connection(self):
        """Validate connection to Binance Futures Testnet."""
        try:
            self.client.futures_account_balance()
        except BinanceAPIException as e:
            error_msg = f"API Error: {getattr(e, 'status_code', '?')} - {getattr(e, 'message', str(e))}"
            self.logger.error(f"Connection failed: {error_msg}")
            raise RuntimeError("Failed to connect to Binance Futures Testnet. Check your API keys.")
        except Exception as e:
            self.logger.error(f"Connection error: {type(e).__name__}: {e}")
            raise RuntimeError("Failed to connect to Binance Futures Testnet. Check your internet connection.")

    def market_order(self, symbol, side, quantity):
        """Place a market order.
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
            side: 'BUY' or 'SELL'
            quantity: Amount to trade
            
        Returns:
            dict: Order response from Binance
        """
        try:
            side = side.upper()
            if side not in ("BUY", "SELL"):
                raise ValueError("Side must be 'BUY' or 'SELL'")
                
            qty = float(quantity)
            if qty <= 0:
                raise ValueError("Quantity must be positive")
                
            self.logger.info(f"[ORDER] MARKET {symbol} {side} qty={qty}")
            order = self.client.futures_create_order(
                symbol=symbol, 
                side=side, 
                type="MARKET", 
                quantity=qty
            )
            
            self.logger.info(f"Response: OrderID={order.get('orderId')}, Status={order.get('status')}")
            return order
            
        except (BinanceAPIException, ValueError) as e:
            self.logger.error(f"Market order failed: {type(e).__name__}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error in market_order: {type(e).__name__}: {e}")
            raise

    def limit_order(self, symbol, side, quantity, price):
        """Place a limit order.
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
            side: 'BUY' or 'SELL'
            quantity: Amount to trade
            price: Limit price
            
        Returns:
            dict: Order response from Binance
        """
        try:
            side = side.upper()
            if side not in ("BUY", "SELL"):
                raise ValueError("Side must be 'BUY' or 'SELL'")
                
            qty = float(quantity)
            price_val = float(price)
            
            if qty <= 0 or price_val <= 0:
                raise ValueError("Quantity and price must be positive")
                
            if not symbol.upper().endswith("USDT"):
                raise ValueError("Only USDT-M futures pairs are supported")
                
            self.logger.info(f"[ORDER] LIMIT {symbol} {side} qty={qty} price={price_val}")
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                quantity=qty,
                price=price_val,
                timeInForce="GTC"
            )
            
            self.logger.info(f"Response: OrderID={order.get('orderId')}, Status={order.get('status')}")
            return order
            
        except (BinanceAPIException, ValueError) as e:
            self.logger.error(f"Limit order failed: {type(e).__name__}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error in limit_order: {type(e).__name__}: {e}")
            raise

    def stop_limit_order(self, symbol, side, quantity, price, stop_price):
        """Place a stop-limit order.
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
            side: 'BUY' or 'SELL'
            quantity: Amount to trade
            price: Limit price when triggered
            stop_price: Trigger price for the stop order
            
        Returns:
            dict: Order response from Binance
        """
        try:
            side = side.upper()
            if side not in ("BUY", "SELL"):
                raise ValueError("Side must be 'BUY' or 'SELL'")
                
            qty = float(quantity)
            price_val = float(price)
            stop_val = float(stop_price)
            
            if qty <= 0 or price_val <= 0 or stop_val <= 0:
                raise ValueError("Quantity, price, and stop_price must be positive")
                
            if side == "SELL" and stop_val <= price_val:
                raise ValueError("For SELL, stop_price must be greater than price")
            if side == "BUY" and stop_val >= price_val:
                raise ValueError("For BUY, stop_price must be less than price")
                
            if not symbol.upper().endswith("USDT"):
                raise ValueError("Only USDT-M futures pairs are supported")
                
            self.logger.info(f"[ORDER] STOP_LIMIT {symbol} {side} qty={qty} price={price_val} stop={stop_val}")
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="STOP_MARKET",
                quantity=qty,
                stopPrice=stop_val,
                price=price_val,
                timeInForce="GTC"
            )
            
            self.logger.info(f"Response: OrderID={order.get('orderId')}, Status={order.get('status')}")
            return order
            
        except (BinanceAPIException, ValueError) as e:
            self.logger.error(f"Stop-limit order failed: {type(e).__name__}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error in stop_limit_order: {type(e).__name__}: {e}")
            raise

    def get_symbol_info(self, symbol):
        """Get the minimum order size and notional value for a symbol."""
        try:
            exchange_info = self.client.futures_exchange_info()
            for s in exchange_info['symbols']:
                if s['symbol'] == symbol and s['status'] == 'TRADING':
                    # Extract lot size filter (minQty, stepSize)
                    lot_size = next(
                        (f for f in s['filters'] if f['filterType'] == 'LOT_SIZE'),
                        None
                    )
                    # Extract min notional filter (minNotional)
                    min_notional = next(
                        (f for f in s['filters'] if f['filterType'] == 'MIN_NOTIONAL'),
                        None
                    )
                    return {
                        'min_qty': float(lot_size['minQty']) if lot_size else 0.001,
                        'step_size': float(lot_size['stepSize']) if lot_size else 0.001,
                        'min_notional': float(min_notional['notional']) if min_notional else 5.0  # Default $5 if not found
                    }
            return None
        except Exception as e:
            self.logger.error(f"Failed to fetch symbol info: {e}")
            return None

    def _print_order_summary(self, order_type, symbol, side, quantity, price=None, stop_price=None):
        """Print a summary of the order details with validation."""
        print("\n=== Order Summary ===")
        print(f"Symbol:    {symbol}")
        print(f"Side:      {side}")
        print(f"Type:      {order_type}")
        print(f"Quantity:  {quantity}")
        if price is not None:
            print(f"Price:     {price}")
        if stop_price is not None:
            print(f"Stop Price: {stop_price}")
        
        # Validate order size against symbol limits
        symbol_info = self.get_symbol_info(symbol)
        if symbol_info:
            min_qty = symbol_info['min_qty']
            min_notional = symbol_info['min_notional']
            estimated_notional = float(quantity) * (float(price) if price else 1.0)
            
            if float(quantity) < min_qty:
                print(f"\n[WARNING] Quantity is below minimum: {min_qty} {symbol}")
            if price and estimated_notional < min_notional:
                print(f"[WARNING] Order value (${estimated_notional:.2f}) is below minimum: ${min_notional:.2f}")
        else:
            print("\n[WARNING] Could not validate order size limits.")
        
        print("====================\n")

    def cli(self):
        import shlex
        print("\n==============================")
        print(" Welcome to BasicBot – Binance Testnet Trader")
        print("==============================\n")
        # If no CLI args (other than script name), use interactive mode
        if len(sys.argv) == 1:
            # Interactive prompt
            def prompt_symbol():
                while True:
                    symbol = input("Enter symbol (e.g. BTCUSDT): ").strip().upper()
                    if symbol.endswith("USDT") and len(symbol) >= 6:
                        return symbol
                    print("Invalid symbol. Must end with 'USDT'.")
            def prompt_side():
                while True:
                    side = input("Enter side (BUY/SELL): ").strip().upper()
                    if side in ("BUY", "SELL"):
                        return side
                    print("Invalid side. Enter BUY or SELL.")
            def prompt_type():
                while True:
                    otype = input("Enter order type (MARKET/LIMIT/STOP_LIMIT): ").strip().upper()
                    if otype in ("MARKET", "LIMIT", "STOP_LIMIT"):
                        return otype
                    print("Invalid type. Enter MARKET, LIMIT, or STOP_LIMIT.")
            def prompt_float(prompt, required=True, minval=0.0, symbol=None, is_price=False):
                while True:
                    val = input(prompt).strip()
                    if not val:
                        if not required:
                            return None
                        print("This field is required.")
                        continue
                    try:
                        fval = float(val)
                    except Exception:
                        print("Enter a valid number (e.g., 0.001).")
                        continue
                    if fval <= minval:
                        print(f"Value must be greater than {minval}.")
                        continue
                    # Additional validation for symbol-specific limits
                    if symbol and not is_price and fval > 0:
                        symbol_info = self.get_symbol_info(symbol)
                        if symbol_info:
                            min_qty = symbol_info['min_qty']
                            step_size = symbol_info['step_size']
                            # Check if quantity is a multiple of step size
                            if (fval % step_size) != 0:
                                print(f"Quantity must be a multiple of {step_size} for {symbol}.")
                                continue
                            if fval < min_qty:
                                print(f"Minimum quantity for {symbol} is {min_qty}.")
                                continue
                    return fval
            symbol = prompt_symbol()
            side = prompt_side()
            otype = prompt_type()
            
            # Get symbol info to show min/max values
            symbol_info = self.get_symbol_info(symbol)
            if symbol_info:
                print(f"\nSymbol Info for {symbol}:")
                print(f"- Min quantity: {symbol_info['min_qty']}")
                print(f"- Step size: {symbol_info['step_size']}")
                print(f"- Min notional: ${symbol_info['min_notional']:.2f}\n")
            
            # Prompt for quantity with symbol-specific validation
            quantity = prompt_float(
                f"Enter quantity (min: {symbol_info['min_qty'] if symbol_info else '?'}): ",
                symbol=symbol
            )
            
            price = None
            stop_price = None
            if otype in ("LIMIT", "STOP_LIMIT"):
                price = prompt_float("Enter price: ", symbol=symbol, is_price=True)
                # Validate min notional if we have price and quantity
                if symbol_info and price:
                    min_notional = symbol_info['min_notional']
                    estimated_notional = float(quantity) * float(price)
                    if estimated_notional < min_notional:
                        print(f"[WARNING] Order value (${estimated_notional:.2f}) is below minimum: ${min_notional:.2f}")
                        if input("Continue anyway? (y/n): ").lower() != 'y':
                            print("Order canceled by user.")
                            sys.exit(0)
            
            if otype == "STOP_LIMIT":
                stop_price = prompt_float("Enter stop price: ", symbol=symbol, is_price=True)
            # Validate stop/limit logic
            if otype == "STOP_LIMIT":
                if side == "SELL" and stop_price <= price:
                    print("For SELL, stop_price must be greater than price.")
                    sys.exit(1)
                if side == "BUY" and stop_price >= price:
                    print("For BUY, stop_price must be less than price.")
                    sys.exit(1)
            # Print summary and execute
            self._print_order_summary(otype, symbol, side, quantity, price, stop_price)
            try:
                if otype == "MARKET":
                    result = self.market_order(symbol, side, quantity)
                elif otype == "LIMIT":
                    result = self.limit_order(symbol, side, quantity, price)
                elif otype == "STOP_LIMIT":
                    result = self.stop_limit_order(symbol, side, quantity, price, stop_price)
                else:
                    print(f"Unsupported order type: {otype}")
                    sys.exit(1)
                print(f"✅ Order placed successfully! Order ID: {result.get('orderId')}")
            except Exception as e:
                print(f"Order failed: {e}")
                sys.exit(1)
            return
        # Otherwise, use argparse as before
        """Handle command line interface for placing orders."""
        parser = argparse.ArgumentParser(
            description="BasicBot - A command-line interface for Binance Futures Testnet trading",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        
        # Required arguments
        required = parser.add_argument_group('required arguments')
        required.add_argument("--symbol", required=True, 
                            help="Trading pair symbol (e.g., BTCUSDT, ETHUSDT). Must be a USDT-margined futures pair.")
        required.add_argument("--side", required=True, choices=["BUY", "SELL"], 
                            help="Order side: BUY to go long, SELL to go short")
        required.add_argument("--type", required=True, choices=["MARKET", "LIMIT", "STOP_LIMIT"], 
                            help="Order type: MARKET for immediate execution, LIMIT for limit order, STOP_LIMIT for stop-limit order")
        required.add_argument("--quantity", required=True, type=float, 
                            help="Order quantity in base asset (must be greater than 0)")
        
        # Optional arguments
        parser.add_argument("--price", type=float, 
                          help="[REQUIRED for LIMIT/STOP_LIMIT] Order price in quote asset (must be greater than 0)")
        parser.add_argument("--stop_price", type=float, 
                          help="[REQUIRED for STOP_LIMIT] Stop price in quote asset (must be greater than 0)")
        
        # Parse arguments
        args = parser.parse_args()
        
        try:
            # Convert to uppercase for consistency
            side = args.side.upper()
            order_type = args.type.upper()
            
            # Common validations
            if args.quantity <= 0:
                raise ValueError("--quantity must be positive")
                
            if not args.symbol.upper().endswith("USDT"):
                raise ValueError("Only USDT-M futures are supported (symbol must end with 'USDT')")
            
            # Type-specific validations and order execution
            result = None
            if order_type == "MARKET":
                self._print_order_summary(order_type, args.symbol, side, args.quantity)
                result = self.market_order(args.symbol, side, args.quantity)
                
            elif order_type == "LIMIT":
                if args.price is None:
                    raise ValueError("--price is required for LIMIT orders")
                if args.price <= 0:
                    raise ValueError("--price must be positive")
                self._print_order_summary(order_type, args.symbol, side, args.quantity, price=args.price)
                result = self.limit_order(args.symbol, side, args.quantity, args.price)
                
            elif order_type == "STOP_LIMIT":
                if args.price is None or args.stop_price is None:
                    raise ValueError("--price and --stop_price are required for STOP_LIMIT orders")
                if args.price <= 0 or args.stop_price <= 0:
                    raise ValueError("--price and --stop_price must be positive")
                self._print_order_summary(order_type, args.symbol, side, args.quantity, 
                                        price=args.price, stop_price=args.stop_price)
                result = self.stop_limit_order(args.symbol, side, args.quantity, args.price, args.stop_price)
            
            # Print success message with order details
            if result:
                print(f"✅ Order placed successfully! Order ID: {result.get('orderId')}")
                return result
                
            else:
                raise ValueError(f"Unsupported order type: {order_type}")
                
        except ValueError as e:
            self.logger.error(f"Validation error: {e}")
            sys.exit(1)
        except Exception as e:
            self.logger.error(f"Order failed: {str(e)}")
            sys.exit(1)

if __name__ == "__main__":
    bot = BasicBot()
    bot.cli()