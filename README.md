# 🚀 APEX: Binance Futures Testnet Trading Bot

<div align="center">
  <p>
    <a href="https://github.com/pragyajhaa/apex/actions">
      <img alt="GitHub Workflow Status" src="https://img.shields.io/github/actions/workflow/status/pragyajhaa/apex/python-package.yml?style=for-the-badge">
    </a>
    <a href="https://github.com/pragyajhaa/apex">
      <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/pragyajhaa/apex?style=for-the-badge">
    </a>
    <a href="https://github.com/pragyajhaa/apex/blob/main/LICENSE">
      <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge" />
    </a>
  </p>
</div>

A professional Python trading bot for Binance USDT-M Futures Testnet, featuring both CLI and Web interfaces with robust error handling. Perfect for testing trading strategies risk-free.

## ✨ Features

### 📊 Trading Features
- **Multiple Order Types**
  - MARKET, LIMIT, and STOP_LIMIT orders
  - USDT-margined futures only
  - Real-time order status updates
  - Symbol-specific validation

### 🖥️ User Interfaces
- **Web Interface**
  - Modern, responsive dashboard
  - Real-time order status
  - Interactive order placement
  - Clean, intuitive design

- **Command Line Interface**
  - Interactive mode with guided prompts
  - Scriptable command-line arguments
  - Detailed order validation

### 🔒 Security & Reliability
  - Testnet-only operation (no real funds)
  - Secure API key management with `.env`
  - Comprehensive error handling
  - Detailed logging to `bot.log`
  - No persistent storage of sensitive data

## 🛠️ Prerequisites

- Python 3.8 or higher
- Binance Futures Testnet account
- Testnet API key with trading permissions

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/pragyajhaa/apex-trading-bot.git
cd apex-trading-bot
```

### 2. Set Up Virtual Environment

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

1. Create a `.env` file in the project root
2. Add your testnet API credentials:

```ini
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
```

> 🔒 **Security Note**: Never commit your `.env` file. It's already in `.gitignore`.

## 🎮 Usage

### 🌐 Web Interface (Recommended)

1. Start the web server:
   ```bash
   streamlit run app.py
   ```
2. Open your browser to `http://localhost:8501`
3. Configure your API keys in the sidebar
4. Place orders using the intuitive interface

### 💻 Command Line Interface

#### Interactive Mode
```bash
python basic_bot.py
```
Follow the on-screen prompts to place orders.

#### Direct Commands

**Market Order**
```bash
python basic_bot.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

**Limit Order**
```bash
python basic_bot.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.1 --price 3500
```

**Stop-Limit Order**
```bash
python basic_bot.py --symbol SOLUSDT --side BUY --type STOP_LIMIT --quantity 5 --price 150 --stop_price 155
```

## 📁 Project Structure

```
├── .github/           # GitHub workflows and templates
│   └── workflows/     # CI/CD workflows
├── docs/              # Documentation files
├── app.py           # Streamlit web interface
├── basic_bot.py     # Core trading bot implementation
├── .env.example     # Example environment variables
├── requirements.txt # Python dependencies
├── README.md        # This file
└── .gitignore       # Git ignore rules
```

## 📦 Dependencies

- Python 3.8+
- `python-binance` - Binance API client
- `streamlit` - Web interface
- `python-dotenv` - Environment variable management
- `argparse` - Command-line argument parsing
- `Logging` - Built-in Python logging module

Install all dependencies:
```bash
pip install -r requirements.txt
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## Important Notes

- The bot only works with Binance Futures Testnet
- All trades are executed in test mode (no real funds)
- Never commit your `.env` file with real API keys
- Monitor the `bot.log` file for detailed execution logs
- Use at your own risk - always test thoroughly with small amounts first

## Acknowledgments

- [Binance API](https://binance-docs.github.io/apidocs/futures/en/) for their excellent documentation
- [python-binance](https://github.com/sammchardy/python-binance) for the Binance API client
- [Streamlit](https://streamlit.io/) for the web interface framework

## License

```
MIT License

Copyright (c) 2025 Pragya Jha

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
