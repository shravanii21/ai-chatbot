# AI Chatbot

A simple AI chatbot web application built with **FastAPI** and powered by the **Google Gemini API**.

---

## Project Structure

```
AI AGENT/
├── main.py              # FastAPI backend
├── static/
│   └── index.html       # Chat frontend
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment variables
├── .gitignore
└── README.md
```

---

## Prerequisites

- Python 3.10 or higher
- A [Google Gemini API key](https://aistudio.google.com/app/apikey)

---

## Local Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd "AI AGENT"
```

### 2. Create and activate a virtual environment

```bash
# Create
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS / Linux)
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

Copy the example file and add your Gemini API key:

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Open `.env` and replace `your_gemini_api_key_here` with your actual key:

```
GEMINI_API_KEY=AIza...your_real_key...
```

### 5. Run the application

```bash
python main.py
```

Then open your browser at **http://localhost:8000**.

---

## API Reference

### `POST /chat`

Send a message and receive a Gemini-generated reply.

**Request body (JSON):**

```json
{
  "message": "What is the capital of France?"
}
```

**Response (JSON):**

```json
{
  "reply": "The capital of France is Paris."
}
```

### `GET /health`

Returns `{ "status": "ok" }` — used as a health-check endpoint.

---

## Deployment on Render

1. Push your code to a GitHub repository (make sure `.env` is in `.gitignore`).
2. Go to [render.com](https://render.com) and create a new **Web Service**.
3. Connect your GitHub repository.
4. Set the following in the Render dashboard:

   | Setting | Value |
   |---|---|
   | **Runtime** | Python 3 |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `python main.py` |

5. Add an **Environment Variable** in the Render dashboard:

   | Key | Value |
   |---|---|
   | `GEMINI_API_KEY` | your actual Gemini API key |

6. Click **Deploy**. Render automatically injects the `PORT` variable — the app reads it and binds correctly.

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` | ✅ Yes | Your Google Gemini API key |
| `PORT` | No | Port to listen on (default: `8000`). Set automatically by Render. |
