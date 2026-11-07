# CareerCanvas: An Agentic AI Career and CV Assistant

CareerCanvas is a Telegram chatbot built with n8n and Google Gemini. It offers three services in one chat: **Create a New CV**, **Improve My CV**, and **Find Opportunities**. After the user confirms, the final CV is generated as a Word file (`CareerCanvas.docx`) and sent back in Telegram.

Course: CT017-3-1 Introduction to Artificial Intelligence (Group Assignment 13)
Telegram bot: https://t.me/CareerCanvasAI_bot

> **Note:** The bot runs on a local computer. It replies only while n8n, the Flask service and the Cloudflare Tunnel are running.

## Repository Contents

| File | Purpose |
|------|---------|
| `CareerCanvas.json` | Exported n8n workflow (trigger, routing, four AI agents, Word file delivery) |
| `novacv_service.py` | Flask service that creates the Word file with python-docx |
| `requirements.txt` | Python libraries needed by the service |

## Requirements

- Node.js and npm
- n8n (self-hosted Community Edition)
- Python 3.10 or later
- Cloudflared (Cloudflare Tunnel)
- A Telegram bot token from BotFather
- A Google Gemini API key

## Setup

1. **Install n8n**
   ```bash
   npm install -g n8n
   ```

2. **Install the Python libraries**
   ```bash
   pip install -r requirements.txt
   ```

3. **Import the workflow.** In n8n, choose *Import from File* and select `CareerCanvas.json`.

4. **Add your own credentials in n8n.** No secret values are stored in this repository.
   - Telegram: the bot token from BotFather
   - Google Gemini: your API key

5. **Check the HTTP Request node.** It should send a POST request to `http://127.0.0.1:5001/create-cv`.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `WEBHOOK_URL` | Public HTTPS address of the Cloudflare Tunnel, set before n8n starts |

## Startup Order

Start the components in this order:

1. **Cloudflare Tunnel**
   ```bash
   cloudflared tunnel --url http://localhost:5678 --protocol http2
   ```
   Copy the `https://...trycloudflare.com` address it prints.

2. **n8n** (with the tunnel address as `WEBHOOK_URL`)
   ```powershell
   $env:WEBHOOK_URL="https://your-tunnel-addres
