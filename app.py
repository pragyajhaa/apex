import os
import streamlit as st
from basic_bot import BasicBot
from dotenv import load_dotenv

st.set_page_config(
    page_title="APEX Trading Bot",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main {
        max-width: 900px;
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .success-box {
        background-color: #e8f5e9;
        border-left: 5px solid #4CAF50;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
    }
    .error-box {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
    }
    .info-box {
        background-color: #e3f2fd;
        border-left: 5px solid #2196F3;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("📊 APEX Trading Bot")
    st.markdown("---")
    
    if 'order_result' not in st.session_state:
        st.session_state.order_result = None
    if 'error_message' not in st.session_state:
        st.session_state.error_message = None

    with st.sidebar:
        st.header("🔑 API Configuration")
        use_env = st.checkbox("Use .env file", value=True, 
                            help="Uncheck to manually enter API keys")
        
        if not use_env:
            api_key = st.text_input("API Key", type="password", 
                                  help="Leave empty to use .env")
            api_secret = st.text_input("API Secret", type="password", 
                                     help="Leave empty to use .env")
        else:
            api_key = None
            api_secret = None

    with st.form("order_form"):
        st.header("📝 Place New Order")
        col1, col2 = st.columns(2)
        
        with col1:
            symbol = st.text_input("Symbol", "BTCUSDT", 
                                 help="Trading pair, e.g., BTCUSDT, ETHUSDT").upper()
            order_type = st.selectbox(
                "Order Type",
                ["MARKET", "LIMIT", "STOP_LIMIT"],
                index=0,
                help="Select order type"
            )
            side = st.radio("Side", ["BUY", "SELL"], horizontal=True,
                          help="Buy to go long, Sell to go short")
        
        with col2:
            quantity = st.number_input(
                "Quantity",
                min_value=0.001,
                step=0.001,
                format="%.6f",
                help="Amount to trade"
            )
            price = st.number_input(
                "Price (USDT)",
                min_value=0.0,
                step=0.1,
                format="%.2f",
                disabled=(order_type == "MARKET"),
                help="Limit price for the order"
            )
            if order_type == "STOP_LIMIT":
                stop_price = st.number_input(
                    "Stop Price (USDT)",
                    min_value=0.0,
                    step=0.1,
                    format="%.2f",
                    help="Stop price to trigger the limit order"
                )
            else:
                stop_price = None

        submitted = st.form_submit_button("🚀 Place Order", use_container_width=True)

        if submitted:
            try:
                bot = BasicBot(api_key=api_key, api_secret=api_secret) if not use_env else BasicBot()
                if order_type == "MARKET":
                    result = bot.market_order(symbol, side, quantity)
                elif order_type == "LIMIT":
                    result = bot.limit_order(symbol, side, quantity, price)
                else:  # STOP_LIMIT
                    result = bot.stop_limit_order(symbol, side, quantity, price, stop_price)
                st.session_state.order_result = result
                st.session_state.error_message = None
                bot.logger.info(f"Web UI Order Success: {result}")
            except Exception as e:
                st.session_state.error_message = str(e)
                st.session_state.order_result = None
                if 'bot' in locals():
                    bot.logger.error(f"Web UI Order Error: {str(e)}")

    if st.session_state.error_message:
        st.markdown(f"""
        <div class="error-box">
            <h4>❌ Error</h4>
            <p>{st.session_state.error_message}</p>
        </div>
        """, unsafe_allow_html=True)
    
    if st.session_state.order_result:
        result = st.session_state.order_result
        st.markdown("""
        <div class="success-box">
            <h4>✅ Order Placed Successfully!</h4>
        </div>
        """, unsafe_allow_html=True)
        with st.expander("📋 Order Details", expanded=True):
            st.json(result)
        st.markdown("### 📊 Order Summary")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Symbol", result.get('symbol', 'N/A'))
            st.metric("Side", result.get('side', 'N/A').upper())
        with col2:
            st.metric("Type", result.get('type', 'N/A'))
            st.metric("Status", result.get('status', 'N/A'))
        with col3:
            st.metric("Quantity", f"{float(result.get('origQty', 0)):g}")
            if 'price' in result:
                st.metric("Price", f"${float(result.get('price', 0)):,.2f}")
        if st.button("🔄 Place Another Order"):
            st.session_state.order_result = None
            st.experimental_rerun()

if __name__ == "__main__":
    main()
