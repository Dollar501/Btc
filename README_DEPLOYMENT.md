# 🚀 BTC-CloudX Deployment Guide

## 📋 Overview
BTC-CloudX is a comprehensive Bitcoin cloud mining platform featuring both a Telegram bot and a modern web application with multi-language support (Arabic, English, Chinese).

## 🌟 Features
- 🤖 Telegram Bot Integration
- 🌐 Modern Web Application
- 🎨 3D Bitcoin Animation
- 💰 Investment Calculator
- 🎫 Monthly Rewards System
- 🌍 Multi-language Support (AR/EN/ZH)
- 📱 Responsive Design

## 🚀 Deployment Options

### 1. Hostinger (Web Files Only)
Upload the following files to your Hostinger hosting:
```
index.html
styles.css
script.js
languages.js
img/ (folder)
```

### 2. GitHub Repository
1. Create a new repository on GitHub
2. Upload all project files
3. Set repository to public for GitHub Pages (optional)

### 3. Render (Python Bot)
1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set environment variables:
   - `BOT_TOKEN`: Your Telegram bot token
   - `WEBHOOK_URL`: Your Render app URL
   - `PORT`: 10000 (default)

## ⚙️ Environment Variables
Create a `.env` file with:
```
BOT_TOKEN=your_telegram_bot_token_here
WEBHOOK_URL=your_render_app_url_here
PORT=10000
```

## 📦 Installation

### Local Development
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies (for Tailwind)
npm install

# Build CSS
npx tailwindcss -i ./input.css -o ./styles.css --watch

# Run the bot
python main.py
```

### Production Deployment
The project includes:
- `Procfile` for Render deployment
- `render.yaml` for Render configuration
- `netlify.toml` for Netlify deployment
- `.htaccess` for Apache servers

## 🔧 Configuration

### Telegram Bot Setup
1. Create a bot with @BotFather
2. Get your bot token
3. Set webhook URL to your Render deployment
4. Configure Web App URL in bot settings

### Web App Setup
1. Upload web files to Hostinger
2. Ensure all paths are correct
3. Test responsive design
4. Verify multi-language functionality

## 📁 Project Structure
```
BTC-CloudX/
├── Frontend/
│   ├── index.html
│   ├── styles.css
│   ├── script.js
│   └── languages.js
├── Backend/
│   ├── main.py
│   ├── localization.py
│   ├── data_store.py
│   └── helpers.py
├── Config/
│   ├── requirements.txt
│   ├── Procfile
│   ├── render.yaml
│   └── .env
└── Documentation/
    └── README.md
```

## 🔒 Security Notes
- Never commit `.env` files to GitHub
- Use environment variables for sensitive data
- Enable HTTPS in production
- Regularly update dependencies

## 🆘 Troubleshooting

### Common Issues
1. **Bot not responding**: Check BOT_TOKEN and webhook URL
2. **CSS not loading**: Verify Tailwind CSS build process
3. **Language switching**: Ensure all translation files are uploaded
4. **Mobile layout**: Test responsive design on different devices

### Support
For issues or questions, check the documentation or create an issue on GitHub.

## 📄 License
This project is licensed under the MIT License.

---
**BTC-CloudX** - The Leading Cloud Mining Platform 🚀
