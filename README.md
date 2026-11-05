# CareerCanvas - AI Career Coaching Agent

**CareerCanvas** is an automated AI Career Coaching Agent built using **n8n** workflows, **Telegram Bot**, and **Google Gemini AI**. The agent assists job seekers with career guidance, resume review suggestions, and professional interview preparation.

---

## 🔗 Project Links & Endpoints

| Resource | URL / Access | Description |
| :--- | :--- | :--- |
| **Telegram Bot** | [t.me/CareerCanvasAI_bot](https://t.me/CareerCanvasAI_bot) | Interactive user interface to test and chat with the AI Agent in real time. |
| **n8n Webhook Endpoint** |https://solely-burner-geology-equipped.trycloudflare.com/webhook/8ec12ab6-199f-458e-a01f-a96b1f1437bd | Production Webhook endpoint connecting Telegram requests to the n8n execution pipeline. | to the n8n execution pipeline. |
| **GitHub Repository** | [CareerCanvas-n8n-Agent](https://github.com/GumanaAbdullah31/CareerCanvas-n8n-Agent) | Central repository housing workflow JSON schema and project documentation. |

---

## 🛠 Architecture & Tech Stack

* **Workflow Automation Engine:** n8n
* **Interactive Frontend:** Telegram Bot API
* **AI Model Engine:** Google Gemini AI API (`models/gemini-2.5-flash` / `models/gemini-3.5-flash-lite`)
* **Tunneling & Security:** Cloudflare Tunnel

---

## ⚙️ Environment Variables & Credentials Required

To run and deploy this n8n workflow locally or on a server, configure the following environment credentials inside your n8n workspace:

1. `TELEGRAM_BOT_TOKEN`: The API Token obtained from `@BotFather`.
2. `GEMINI_API_KEY`: Google Generative AI API Key for executing model prompts.

---

## 📁 Repository Structure

```text
├── CareerCanvas.json    # Exported n8n workflow JSON file
└── README.md            # System architecture and deployment documentation# CareerCanvas-n8n-Agent
